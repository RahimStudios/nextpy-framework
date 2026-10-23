"""Logout endpoint used by the JobHub nav form.

A normal HTML form POST (instead of an SPA link) guarantees the browser
follows the redirect and stores the cleared session cookie.
"""

from fastapi import Request
from fastapi.responses import RedirectResponse

from nextpy.auth import COOKIE_NAME, clear_session_cookie


async def post(request: Request, params):
    response = RedirectResponse("/jobs", status_code=303)
    session_id = request.cookies.get(COOKIE_NAME, "")
    if session_id:
        clear_session_cookie(response, session_id, secure=request.url.scheme == "https")
    else:
        response.delete_cookie(COOKIE_NAME, path="/")
    return response
