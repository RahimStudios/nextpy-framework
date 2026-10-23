"""Tests for generic fullstack helpers: DB, cache, tasks, actions, assets."""

import asyncio
from pathlib import Path

import pytest
from fastapi import HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from nextpy.build.assets import AssetBundler
from nextpy.cache import MemoryCache, cached
from nextpy.core.streaming import chunk_html
from nextpy.db import (
    Application,
    Job,
    User,
    count_by,
    get_session,
    init_db,
    paginate,
    serialize_model,
)
from nextpy.server_actions import ServerAction, server_action
from nextpy.tasks import BackgroundQueue


@pytest.fixture()
def db(tmp_path):
    init_db(f"sqlite:///{tmp_path / 'test.db'}")
    session = get_session()
    try:
        yield session
    finally:
        session.close()


def _request(headers=None):
    return Request({
        "type": "http",
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/",
        "raw_path": b"/",
        "query_string": b"",
        "headers": headers or [],
        "client": ("testclient", 123),
        "server": ("testserver", 80),
        "root_path": "",
    })


def test_pagination_and_batch_counts(db):
    employer = User(email="e@example.com", username="e", hashed_password="x", role="employer")
    seeker = User(email="s@example.com", username="s", hashed_password="x")
    db.add_all([employer, seeker])
    db.commit()
    for index in range(5):
        db.add(Job(title=f"Job {index}", company="Acme", description="d", employer_id=employer.id))
    db.commit()
    jobs = db.query(Job).order_by(Job.id).all()
    for job in jobs[:3]:
        db.add(Application(job_id=job.id, applicant_id=seeker.id, status="pending"))
    db.commit()

    page = paginate(db.query(Job).order_by(Job.id), page=2, per_page=2)
    assert page.total == 5
    assert page.page == 2
    assert page.pages == 3
    assert page.has_next and page.has_prev
    assert len(page.items) == 2
    page_meta = page.to_dict()
    assert "items" not in page_meta
    assert page_meta["pages"] == 3

    counts = count_by(db, Application, "job_id", {"job_id": [jobs[0].id, jobs[1].id]})
    assert counts[jobs[0].id] == 1
    assert counts[jobs[1].id] == 1
    assert counts.get(jobs[4].id, 0) == 0


def test_application_relationships_avoid_n_plus_one(db):
    user = User(email="r@example.com", username="r", hashed_password="x")
    db.add(user)
    db.commit()
    job = Job(title="Role", company="Co", description="d", employer_id=user.id)
    db.add(job)
    db.commit()
    app = Application(job_id=job.id, applicant_id=user.id)
    db.add(app)
    db.commit()
    db.expire_all()

    loaded = db.query(Application).first()
    assert loaded.job.title == "Role"
    assert loaded.applicant.email == "r@example.com"
    payload = serialize_model(loaded)
    assert payload["status"] == "pending"


def test_memory_cache_ttl_and_async_decorator():
    cache = MemoryCache(maxsize=8)
    cache.set("k", "v", ttl=0.01)
    assert cache.get("k") == "v"
    import time
    time.sleep(0.02)
    assert cache.get("k") is None

    calls = {"n": 0}

    @cached(ttl=30, cache=cache, namespace="test")
    async def load(value):
        calls["n"] += 1
        return value * 2

    assert asyncio.run(load(2)) == 4
    assert asyncio.run(load(2)) == 4
    assert calls["n"] == 1


def test_background_queue_runs_and_retries():
    queue = BackgroundQueue(workers=1, max_retries=1, retry_delay=0)
    attempts = {"n": 0}

    def flaky():
        attempts["n"] += 1
        if attempts["n"] == 1:
            raise RuntimeError("once")
        return "ok"

    try:
        assert queue.submit(flaky).result(timeout=2) == "ok"
        assert attempts["n"] == 2
        assert queue.stats.completed == 1
        assert queue.stats.retried == 1
    finally:
        queue.stop()


def test_server_action_schema_filters_unknown_params(db):
    class Payload(BaseModel):
        name: str

    @server_action(name="test_schema_echo", schema=Payload)
    async def echo(name: str = ""):
        return {"name": name}

    result = asyncio.run(
        ServerAction.execute(
            "test_schema_echo",
            _request(),
            params={"name": "Ada", "unexpected": "ignored"},
        )
    )
    assert result["success"] is True
    assert result["data"] == {"name": "Ada"}


def test_server_action_requires_auth(db):
    @server_action(name="test_requires_auth", auth=True)
    async def secure():
        return {"ok": True}

    with pytest.raises(HTTPException) as exc:
        asyncio.run(ServerAction.execute("test_requires_auth", _request()))
    assert exc.value.status_code == 401


def test_asset_bundler_deduplicates_inline_scripts(tmp_path):
    page_a = tmp_path / "a.html"
    page_b = tmp_path / "b.html"
    page_a.write_text(
        "<html><body><script>var pageA=1;</script><script>var shared=1;</script></body></html>",
        encoding="utf-8",
    )
    page_b.write_text(
        "<html><body><script>var pageB=1;</script><script>var shared=1;</script></body></html>",
        encoding="utf-8",
    )

    result = AssetBundler(tmp_path).bundle()
    assert result["chunk_count"] == 3
    assert result["shared_chunk_count"] == 1
    assert "_nextpy/chunks/shared-" in page_a.read_text()
    assert "_nextpy/chunks/page-" in page_b.read_text()
    assert (tmp_path / "_nextpy" / "asset-manifest.json").exists()


def test_streaming_chunks_preserve_html():
    text = "".join(f"<p>line {i}</p>\n" for i in range(2000))
    chunks = list(chunk_html(text, 1024))
    assert len(chunks) > 1
    assert "".join(chunks) == text
