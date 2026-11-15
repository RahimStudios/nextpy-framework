"""API Router & fetch_api - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def ApiRouterReference():
    router_example = """from fastapi import Request
from nextpy.api import api


# api routes are mounted under /api automatically
@api.get("/health")
async def health():
    return {"status": "ok"}


@api.post("/echo")
async def echo(request: Request):
    body = await request.json()
    return {"received": body}


# GET /api/health
# POST /api/echo"""

    fetch_example = """from nextpy.api import fetch_api


def getServerSideProps(context):
    # Server-side JSON call; returns decoded data or None
    data = fetch_api("https://api.example.com/posts?page=1")
    return {"props": {"posts": data}}


def submit_to_service(payload):
    # dict/list data is JSON-encoded automatically
    return fetch_api(
        "https://api.example.com/events",
        method="POST",
        data={"type": "signup"},
        headers={"Authorization": "Bearer ..."},
        timeout=5,
    )"""

    files_example = """# pages/api/users.py — file-based route, no decorator needed
def get(request):
    return {"users": [...]}

# pages/api/posts/[id].py — dynamic segment
def get(request, id):
    return {"id": id}

# Both are mounted under /api/users and /api/posts/<id>"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>API Reference</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">API Router</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">API Router &amp; fetch_api</h1>
                    <p class="leading-relaxed text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.api</code> exposes a FastAPI <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">APIRouter</code> for registering routes in Python code, plus <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">fetch_api</code>, a small helper for calling JSON APIs from server-side code. Both are re-exported at the top level of the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy</code> package.
                    </p>
                </header>

                <div id="router" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The api APIRouter</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">api = APIRouter(prefix="/api")</code> is a standard FastAPI router. It is mounted automatically by <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">create_app()</code> (<code class="font-mono text-xs">self.app.include_router(api)</code>), so any route you register on it is served under the <code class="font-mono text-xs">/api</code> prefix.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        At startup the server also loads <code class="font-mono text-xs">api.py</code> and <code class="font-mono text-xs">pages/api.py</code> from your project root before mounting the router (<code class="font-mono text-xs">_load_project_api</code>). Importing <code class="font-mono text-xs">api</code> from <code class="font-mono text-xs">nextpy.api</code> in either file — or anywhere else — lets those modules attach routes to the same router.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="api.py" snippet={router_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li>Supports all FastAPI route decorators: <code class="font-mono text-xs">@api.get</code>, <code class="font-mono text-xs">@api.post</code>, <code class="font-mono text-xs">@api.put</code>, <code class="font-mono text-xs">@api.delete</code>, <code class="font-mono text-xs">@api.patch</code>, etc.</li>
                        <li>Path parameters, query params, and dependency injection work as in FastAPI — e.g. inject <code class="font-mono text-xs">Request</code> to read the JSON body.</li>
                        <li>Routes go through the same middleware stack as the rest of the app, including the security headers, CSRF origin check, and the <code class="font-mono text-xs">RATE_LIMIT_ENABLED</code> rate limiter.</li>
                    </ul>
                </div>

                <div id="fetch-api" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">fetch_api()</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">fetch_api(url, method="GET", data=None, headers=None, timeout=10) -&gt; Any</code> performs a synchronous HTTP call and returns the decoded JSON body (<code class="font-mono text-xs">None</code> for an empty response). It is intended for <code class="font-mono text-xs">getServerSideProps</code> and other server-only code — do not call it from client-side components.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">url</code> &mdash; absolute URL of the endpoint to call.</li>
                        <li><code class="font-mono text-xs">method</code> &mdash; HTTP method; normalized to upper case (default <code class="font-mono text-xs">GET</code>).</li>
                        <li><code class="font-mono text-xs">data</code> &mdash; request body. Dicts and lists are JSON-encoded automatically and get <code class="font-mono text-xs">Content-Type: application/json</code>; other values are sent as-is.</li>
                        <li><code class="font-mono text-xs">headers</code> &mdash; extra headers merged over the default <code class="font-mono text-xs">Accept: application/json</code>.</li>
                        <li><code class="font-mono text-xs">timeout</code> &mdash; seconds before the request times out (default <code class="font-mono text-xs">10</code>).</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={fetch_example} />
                </div>

                <div id="when-to-use" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">When to use what</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><strong class="text-white">api router (<code class="font-mono text-xs">@api.get(...)</code>)</strong> &mdash; when you want several related endpoints defined in code, sharing dependencies and the <code class="font-mono text-xs">/api</code> prefix. Best in a top-level <code class="font-mono text-xs">api.py</code> or <code class="font-mono text-xs">pages/api.py</code>.</li>
                        <li><strong class="text-white">pages/api/ files</strong> &mdash; the file-based convention: each file under <code class="font-mono text-xs">pages/api/</code> maps to a route (dynamic segments via <code class="font-mono text-xs">[param].py</code>) and exports HTTP-method functions (<code class="font-mono text-xs">get</code>, <code class="font-mono text-xs">post</code>, ...). Prefer this when routes are simple and you like the filesystem layout.</li>
                        <li><strong class="text-white">fetch_api</strong> &mdash; for outbound calls to external JSON APIs from server-side code only.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/api/users.py" snippet={files_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/security-api" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Security API
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/caching" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                In-Memory Cache
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
                        <li><a href="#router" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The api APIRouter</a></li>
                        <li><a href="#fetch-api" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">fetch_api()</a></li>
                        <li><a href="#when-to-use" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">When to use what</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "API Router - NextPy Docs"}}


default = ApiRouterReference
