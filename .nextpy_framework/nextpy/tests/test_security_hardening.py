"""Security and API method dispatch regression tests."""

import sys
from pathlib import Path

import httpx
import pytest
import pytest_asyncio

sys.path.insert(0, './.nextpy_framework')

from nextpy.security import security_manager
from nextpy.state_sync import DatabaseState


def test_rich_html_sanitizer_removes_xss_vectors():
    payload = (
        '<p onclick="steal()">ok</p>'
        '<script>alert(1)</script>'
        '<a href="javascript:alert(1)">bad</a>'
        '<img src="x" onerror="alert(1)">'
    )
    cleaned = security_manager.sanitize_rich_html(payload)
    assert '<script' not in cleaned.lower()
    assert 'onclick' not in cleaned.lower()
    assert 'onerror' not in cleaned.lower()
    assert 'javascript:' not in cleaned.lower()
    assert '<p>ok</p>' in cleaned


def test_origin_validation():
    assert security_manager.is_trusted_origin(
        "http://127.0.0.1:5000", "127.0.0.1:5000"
    )
    assert security_manager.is_trusted_origin(
        "https://app.example.com", "127.0.0.1:5000",
        ["https://app.example.com"],
    )
    assert not security_manager.is_trusted_origin(
        "https://evil.example.com", "127.0.0.1:5000"
    )
    assert not security_manager.is_trusted_origin(None, "127.0.0.1:5000")


def test_database_state_rejects_sql_identifier_injection():
    with pytest.raises(ValueError):
        DatabaseState("app_state; DROP TABLE users; --")
    DatabaseState("app_state")


@pytest_asyncio.fixture()
async def api_client(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pages" / "api").mkdir(parents=True)
    (tmp_path / "templates").mkdir()
    (tmp_path / "pages" / "api" / "methods.py").write_text(
        '''
from fastapi import HTTPException


async def get(request, params):
    return {"method": "GET", "params": params}


async def post(request, params):
    return {"method": "POST"}


async def put(request, params):
    return {"method": "PUT"}


async def patch(request, params):
    return {"method": "PATCH"}


async def delete(request, params):
    return {"method": "DELETE"}
''',
        encoding="utf-8",
    )
    (tmp_path / "pages" / "api" / "items").mkdir()
    (tmp_path / "pages" / "api" / "items" / "[id].py").write_text(
        '''
from fastapi import HTTPException


async def get(request, id: int):
    return {"id": id, "type": type(id).__name__}


async def post(request, params):
    raise HTTPException(status_code=404, detail="missing")
''',
        encoding="utf-8",
    )
    (tmp_path / "pages" / "api" / "tuple.py").write_text(
        '''
async def get(request):
    return {"error": "not found"}, 404
''',
        encoding="utf-8",
    )

    from nextpy.server.app import create_app

    app = create_app(
        pages_dir=str(tmp_path / "pages"),
        templates_dir=str(tmp_path / "templates"),
        public_dir=str(tmp_path / "public"),
        out_dir=str(tmp_path / "out"),
        debug=False,
    )
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_security_headers_are_present(api_client):
    response = await api_client.get("/api/methods")
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert "default-src 'self'" in response.headers["content-security-policy"]
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"


@pytest.mark.asyncio
async def test_rate_limit_returns_429():
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route

    from nextpy.server.middleware import RateLimitMiddleware

    async def endpoint(request):
        return JSONResponse({"ok": True})

    app = Starlette(routes=[Route("/api/limited", endpoint)])
    app.add_middleware(
        RateLimitMiddleware, limit_per_minute=2, auth_limit_per_minute=2
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        assert (await client.get("/api/limited")).status_code == 200
        assert (await client.get("/api/limited")).status_code == 200
        blocked = await client.get("/api/limited")
        assert blocked.status_code == 429
        assert blocked.headers["retry-after"]


@pytest.mark.asyncio
async def test_api_supports_all_methods(api_client):
    assert (await api_client.get("/api/methods")).json()["method"] == "GET"
    assert (await api_client.post("/api/methods")).json()["method"] == "POST"
    assert (await api_client.put("/api/methods")).json()["method"] == "PUT"
    assert (await api_client.patch("/api/methods")).json()["method"] == "PATCH"
    assert (await api_client.delete("/api/methods")).json()["method"] == "DELETE"
    assert (await api_client.head("/api/methods")).status_code == 200
    options = await api_client.options("/api/methods")
    assert options.status_code == 204
    assert "GET" in options.headers["allow"]


@pytest.mark.asyncio
async def test_api_dynamic_params_and_status_codes(api_client):
    response = await api_client.get("/api/items/7")
    assert response.status_code == 200
    assert response.json() == {"id": 7, "type": "int"}
    assert (await api_client.post("/api/items/7")).status_code == 404
    assert (await api_client.get("/api/tuple")).status_code == 404


@pytest.mark.asyncio
async def test_csrf_blocks_cookie_post_without_origin(api_client):
    blocked = await api_client.post(
        "/api/methods",
        cookies={"nextpy_session": "test-session"},
    )
    assert blocked.status_code == 403
    allowed = await api_client.post(
        "/api/methods",
        cookies={"nextpy_session": "test-session"},
        headers={"Origin": "http://testserver"},
    )
    assert allowed.status_code == 200


@pytest.mark.asyncio
async def test_csrf_bearer_clients_are_exempt(api_client):
    response = await api_client.post(
        "/api/methods",
        cookies={"nextpy_session": "test-session"},
        headers={"Authorization": "Bearer token"},
    )
    assert response.status_code == 200
