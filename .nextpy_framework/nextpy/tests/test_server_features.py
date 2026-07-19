import os
import subprocess
import shutil
from pathlib import Path

from fastapi.testclient import TestClient

from nextpy.server.app import create_app


def test_security_headers_set():
    app = create_app(debug=True)
    client = TestClient(app)
    resp = client.get("/")
    # check handful of headers
    assert resp.headers.get("X-Content-Type-Options") == "nosniff"
    assert resp.headers.get("X-Frame-Options") == "DENY"
    assert "Content-Security-Policy" in resp.headers
    assert resp.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


def test_auto_tailwind_build(monkeypatch, tmp_path, capsys):
    # simulate absence of tailwind.css
    os.environ["NEXTPY_AUTO_BUILD_TAILWIND"] = "true"
    # create dummy public directory
    public = tmp_path / "public"
    public.mkdir()
    # change cwd to tmp
    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        # monkeypatch npm presence and subprocess.run
        monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/npm" if name == "npm" else None)
        calls = []
        def fake_run(cmd, check=False):
            calls.append(cmd)
            class R:
                returncode = 0
            return R()
        monkeypatch.setattr(subprocess, "run", fake_run)
        # create app which should trigger build
        app = create_app(debug=True)
        # ensure our fake_run was invoked
        assert any("build:tailwind" in str(cmd) for cmd in calls)
    finally:
        os.chdir(cwd)
        os.environ.pop("NEXTPY_AUTO_BUILD_TAILWIND", None)
