"""GitHub star count for the NextPy repo, fetched server-side and cached."""

import json
import time
import urllib.request

_REPO = "RAHIMSTUDIOS/nextpy-framework"
_API_URL = f"https://api.github.com/repos/{_REPO}"
_TTL_SECONDS = 3600

_cache = {"count": None, "fetched_at": 0.0}


def get_github_stars():
    """Return the repo's star count, or None when unavailable."""
    now = time.time()
    if _cache["count"] is not None and now - _cache["fetched_at"] < _TTL_SECONDS:
        return _cache["count"]
    try:
        req = urllib.request.Request(
            _API_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "NextPy-Docs",
            },
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            count = json.loads(resp.read()).get("stargazers_count")
        if isinstance(count, int):
            _cache["count"] = count
            _cache["fetched_at"] = now
    except Exception:
        pass
    return _cache["count"]


def format_stars(count):
    """Format a star count for display ('7', '1.2k'); '' when unknown."""
    if not count:
        return ""
    if count >= 1000:
        value = count / 1000
        return f"{value:.1f}".rstrip("0").rstrip(".") + "k"
    return str(count)
