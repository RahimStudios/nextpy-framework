"""
NextPy Middleware - Request/Response middleware for the server
"""

import time
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class NextPyMiddleware(BaseHTTPMiddleware):
    """
    Core middleware for NextPy applications
    Handles:
    - Request timing
    - Cache headers
    - Security headers
    - HTMX detection
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        request.state.is_htmx = request.headers.get("HX-Request") == "true"
        request.state.htmx_target = request.headers.get("HX-Target")
        request.state.htmx_trigger = request.headers.get("HX-Trigger")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        if request.state.is_htmx:
            response.headers["HX-Push-Url"] = str(request.url.path)
            
        return response


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Optional authentication middleware
    Can be added to protect routes
    """
    
    def __init__(self, app, protected_paths: list = None, login_path: str = "/login"):
        super().__init__(app)
        self.protected_paths = protected_paths or []
        self.login_path = login_path
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path
        
        for protected in self.protected_paths:
            if path.startswith(protected):
                session = request.cookies.get("session")
                if not session:
                    from starlette.responses import RedirectResponse
                    return RedirectResponse(
                        url=f"{self.login_path}?next={path}",
                        status_code=302,
                    )
                    
        return await call_next(request)


class CacheMiddleware(BaseHTTPMiddleware):
    """
    Caching middleware for static content
    """
    
    CACHE_EXTENSIONS = {".js", ".css", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff", ".woff2"}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        path = request.url.path
        
        if any(path.endswith(ext) for ext in self.CACHE_EXTENSIONS):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        elif path.startswith("/_nextpy/"):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
            
        return response


class CSRFMiddleware(BaseHTTPMiddleware):
    """Origin-based CSRF protection for cookie-authenticated requests.

    SameSite=Lax already blocks most cross-site form posts, but Origin/Referer
    validation adds defence in depth for older browsers and misconfigured
    cookies.  Bearer-token API clients are exempt because they do not rely on
    ambient cookies.
    """

    SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}
    SESSION_COOKIE = "nextpy_session"

    def __init__(self, app, allowed_origins=None, enabled: bool = True):
        super().__init__(app)
        self.allowed_origins = list(allowed_origins or [])
        self.enabled = enabled

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self.enabled or request.method.upper() in self.SAFE_METHODS:
            return await call_next(request)

        # Token-authenticated API clients do not use ambient cookies.
        if request.headers.get("authorization", "").lower().startswith("bearer "):
            return await call_next(request)

        if self.SESSION_COOKIE not in request.cookies:
            return await call_next(request)

        from nextpy.security import security_manager

        origin = request.headers.get("origin") or request.headers.get("referer")
        if not security_manager.is_trusted_origin(
            origin, request.url.netloc, self.allowed_origins
        ):
            from starlette.responses import JSONResponse

            return JSONResponse(
                {"error": "CSRF validation failed"},
                status_code=403,
            )

        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Small in-process rate limiter for API and authentication endpoints.

    This is intentionally dependency-free.  For multi-worker deployments use a
    shared store (Redis) instead; the in-process limiter still protects each
    worker from trivial request floods.
    """

    def __init__(
        self,
        app,
        limit_per_minute: int = 240,
        auth_limit_per_minute: int = 60,
        enabled: bool = True,
    ):
        super().__init__(app)
        self.limit = max(1, int(limit_per_minute))
        self.auth_limit = max(1, int(auth_limit_per_minute))
        self.enabled = enabled
        self._hits = {}
        self._lock = __import__("threading").Lock()

    def _bucket(self, request: Request):
        path = request.url.path
        auth_paths = (
            "/login", "/register", "/jobs/login", "/jobs/register",
            "/api/login", "/__nextpy/actions/execute",
        )
        if any(path.startswith(p) for p in auth_paths):
            return "auth", self.auth_limit
        if path.startswith("/api/") or path.startswith("/__nextpy/"):
            return "api", self.limit
        return None, 0

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self.enabled:
            return await call_next(request)

        bucket, limit = self._bucket(request)
        if bucket is None:
            return await call_next(request)

        import time
        from starlette.responses import JSONResponse

        client = request.client.host if request.client else "unknown"
        key = (client, bucket)
        now = time.monotonic()
        window_start = now - 60.0

        with self._lock:
            timestamps = [t for t in self._hits.get(key, []) if t >= window_start]
            if len(timestamps) >= limit:
                retry_after = max(1, int(60 - (now - timestamps[0])))
                return JSONResponse(
                    {"error": "Too many requests"},
                    status_code=429,
                    headers={"Retry-After": str(retry_after)},
                )
            timestamps.append(now)
            self._hits[key] = timestamps

        return await call_next(request)
