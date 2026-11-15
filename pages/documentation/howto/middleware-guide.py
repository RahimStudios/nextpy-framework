"""Middleware: Auth, CSRF, Rate Limiting & Caching - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def MiddlewareGuide():
    stack_example = '''"""The middleware stack (nextpy/server/app.py::_setup_middleware)"""

# Registered in this order — Starlette runs the last-added middleware first,
# so requests flow through the stack roughly as:

#   1. Security headers   — CSP, X-Frame-Options, Referrer-Policy, ...
#   2. RateLimitMiddleware — 429 + Retry-After on API/auth floods
#   3. CSRFMiddleware      — Origin/Referer check on unsafe methods
#   4. GZipMiddleware      — compresses responses >= 1024 bytes
#   5. CacheMiddleware     — immutable Cache-Control for static assets
#   6. NextPyMiddleware    — X-Process-Time, HTMX detection, headers
#   7. CORSMiddleware      — CORS_ORIGINS allowlist'''

    auth_example = '''"""Optional route protection with AuthMiddleware"""

from nextpy.server.middleware import AuthMiddleware

# AuthMiddleware is NOT registered automatically — add it yourself:
#   app.add_middleware(
#       AuthMiddleware,
#       protected_paths=["/dashboard", "/admin", "/account"],
#       login_path="/login",
#   )
#
# Any request whose path starts with a protected prefix and has no
# "session" cookie is redirected (302) to
#   /login?next=<original-path>'''

    csrf_example = '''"""CSRFMiddleware — origin-based CSRF protection"""

# Enabled by default. It validates the Origin (or Referer) header on
# unsafe methods (POST/PUT/PATCH/DELETE) — but only when the request
# carries the "nextpy_session" cookie. There is no token to embed in
# forms; same-origin form posts pass automatically.
#
# Exempt automatically:
#   - GET / HEAD / OPTIONS / TRACE
#   - Requests with an "Authorization: Bearer ..." header
#   - Requests without the session cookie
#
# Failures return 403 {"error": "CSRF validation failed"}.'''

    ratelimit_example = '''"""RateLimitMiddleware — small in-process limiter"""

# Two buckets, keyed by client IP, sliding 60-second window:
#
#   auth bucket (60/min default):
#       /login  /register  /jobs/login  /jobs/register
#       /api/login  /__nextpy/actions/execute
#
#   api bucket (240/min default):
#       anything under /api/ or /__nextpy/
#
# All other paths are not limited. Over-limit requests get
#   429 {"error": "Too many requests"}  +  Retry-After header
#
# In-process only — for multi-worker deploys use a shared store (Redis).'''

    cache_example = '''"""CacheMiddleware — static asset caching"""

# Responses whose path ends in a static extension get:
#   Cache-Control: public, max-age=31536000, immutable
#
# Extensions: .js .css .png .jpg .jpeg .gif .svg .ico .woff .woff2
# Plus anything under /_nextpy/.
#
# Note: this only covers static files. HTML page caching is separate —
# see the in-process page cache / ISR in the router.'''

    custom_example = '''"""middleware/request_id.py — custom middleware"""

import time
import uuid
from typing import Callable

from nextpy.server.middleware import NextPyMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestIdMiddleware(NextPyMiddleware):
    """Attach a unique X-Request-Id to every response."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-Id") or uuid.uuid4().hex[:12]
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        response.headers["X-Request-Duration-Ms"] = str(
            round((time.perf_counter() - started) * 1000, 2)
        )
        return response


# Register on the FastAPI app before the server starts:
#   from nextpy.server import create_app
#   app = create_app()
#   app.add_middleware(RequestIdMiddleware)'''

    config_example = '''""".env — middleware configuration"""

# CSRF_PROTECTION=true            # set "false" to disable CSRF checks
# CSRF_TRUSTED_ORIGINS=https://app.example.com,https://admin.example.com
# CORS_ORIGINS=https://app.example.com   # non-"*" origins also feed
#                                        # the CSRF trusted list
# RATE_LIMIT_ENABLED=true
# RATE_LIMIT_PER_MINUTE=240
# AUTH_RATE_LIMIT_PER_MINUTE=60'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Middleware</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Middleware: Auth, CSRF, Rate Limiting &amp; Caching
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy ships a small Starlette-based middleware stack — request timing, security headers, CSRF origin checks, rate limiting, and immutable caching for static assets — and lets you add your own.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Middleware lives in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy/server/middleware.py</code> and is wired up in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NextPyApp._setup_middleware()</code> (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy/server/app.py</code>). Five middleware classes are provided — <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NextPyMiddleware</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">AuthMiddleware</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CSRFMiddleware</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">RateLimitMiddleware</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CacheMiddleware</code> — plus Starlette's CORS and GZip middleware and a security-headers layer.
                    </p>
                </div>

                <div id="stack" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The middleware stack</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        All middleware is Starlette <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">BaseHTTPMiddleware</code>. Starlette executes the last-registered middleware first, so an incoming request passes through roughly this pipeline before reaching a route:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="nextpy/server/app.py" snippet={stack_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Responses travel back out in reverse order, picking up headers like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">X-Process-Time</code> (from <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NextPyMiddleware</code>) and the CSP/security headers added by the outermost layer.
                    </p>
                </div>

                <div id="auth-middleware" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">AuthMiddleware</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">AuthMiddleware</code> is an opt-in guard for cookie-authenticated areas. It is <strong class="text-white">not</strong> registered by default — you add it to the FastAPI app yourself:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="middleware/auth.py" snippet={auth_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Matching is a simple prefix check: if <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">request.url.path</code> starts with any entry in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">protected_paths</code> and the request has no <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">session</code> cookie, the middleware short-circuits with a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">302</code> redirect to <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&#123;login_path&#125;?next=&#123;path&#125;</code>. For finer-grained control inside pages and actions, the auth how-to guide shows a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">require_auth</code> decorator pattern instead.
                    </p>
                </div>

                <div id="csrf-middleware" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">CSRFMiddleware</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CSRFMiddleware</code> provides origin-based CSRF protection as defence in depth on top of <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">SameSite=Lax</code> cookies. It is enabled by default and validates the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Origin</code> (falling back to <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Referer</code>) header against the request host and an allowlist via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">security_manager.is_trusted_origin</code>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="nextpy/server/middleware.py" snippet={csrf_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Because the check only fires when the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy_session</code> cookie is present, ordinary same-origin HTML forms need no token — the browser sends a matching <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Origin</code> automatically. Cross-origin posts that carry the session cookie are rejected with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">403</code>.
                    </p>
                </div>

                <div id="rate-limiting" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">RateLimitMiddleware</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        A dependency-free, in-process sliding-window limiter keyed by client IP (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">request.client.host</code>). It only limits API and authentication traffic — regular page routes pass through untouched:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="nextpy/server/middleware.py" snippet={ratelimit_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Internally it keeps per-(IP, bucket) timestamp lists under a lock, sweeps idle keys every 60 seconds, and hard-caps the table at 10,000 keys. Because state is per-process, each worker gets its own budget — the docstring recommends a shared store such as Redis for multi-worker deployments.
                    </p>
                </div>

                <div id="caching-middleware" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">CacheMiddleware</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CacheMiddleware</code> marks static assets as immutable so browsers and CDNs cache them for a year:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="nextpy/server/middleware.py" snippet={cache_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        This is distinct from HTML page caching. Rendered pages are cached separately by the component router's in-process page cache with stale-while-revalidate semantics (see the <Link href="/documentation/howto/plugins" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">Streaming SSR</Link> guide for how streaming responses interact with it).
                    </p>
                </div>

                <div id="custom-middleware" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Writing custom middleware</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Subclass <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NextPyMiddleware</code> (itself a Starlette <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">BaseHTTPMiddleware</code>) and implement <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">async def dispatch(request, call_next)</code>. New projects scaffold a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">middleware/</code> directory with a CORS helper showing the same pattern.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="middleware/request_id.py" snippet={custom_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Middleware must be registered before the server starts — call <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">add_middleware</code> on the FastAPI app (the object returned by <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">create_app()</code> or <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy_app.app</code>). Files under <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">middleware/</code> are conventions, not auto-loaded — wire them up explicitly.
                    </p>
                </div>

                <div id="configuration" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Configuration</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The built-in middleware is tuned through environment variables (new projects get these in the generated <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.env</code>):
                    </p>
                    <EnhancedCodeBlock lang="bash" filename=".env" snippet={config_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CSRF_TRUSTED_ORIGINS</code> and non-wildcard <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CORS_ORIGINS</code> entries are merged into the CSRF allowlist; a literal <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">*</code> CORS origin is ignored for CSRF purposes. Toggle flags accept <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">1/true/yes/on</code>.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/admin-panel" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Admin Panel
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/plugins" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Plugin System
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                            </span>
                        </Link>
                    </div>
                </footer>
            </article>

            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-4 pl-8 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
                <div class="text-sm">
                    <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                    <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Overview</a></li>
                        <li><a href="#stack" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The middleware stack</a></li>
                        <li><a href="#auth-middleware" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">AuthMiddleware</a></li>
                        <li><a href="#csrf-middleware" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">CSRFMiddleware</a></li>
                        <li><a href="#rate-limiting" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">RateLimitMiddleware</a></li>
                        <li><a href="#caching-middleware" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">CacheMiddleware</a></li>
                        <li><a href="#custom-middleware" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Writing custom middleware</a></li>
                        <li><a href="#configuration" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Configuration</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Middleware - NextPy Docs"}}


default = MiddlewareGuide
