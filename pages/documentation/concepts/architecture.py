"""Architecture Overview - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def Architecture():
    tree_example = """myapp/
├── pages/                  # file-based routes
│   ├── layout.py           # root layout (wraps every page)
│   ├── index.py            # → /
│   ├── posts/
│   │   ├── layout.py       # → wraps /posts/*
│   │   ├── index.py        # → /posts
│   │   ├── [id].py         # → /posts/:id  (dynamic segment)
│   │   └── [...slug].py    # → /posts/a/b/c (catch-all)
│   ├── loading.py          # Suspense fallback UI
│   ├── error.py            # error boundary
│   └── not-found.py        # 404 UI
├── components/             # reusable PSX components
├── api/                    # optional REST endpoints
└── nextpy.config.py        # app config"""

    page_example = """# pages/posts/[id].py — rendered per request (SSR)
revalidate = 60          # ISR: serve cached HTML, refresh in background
streaming = True         # stream the HTML response in chunks


@getServerSideProps
def getServerSideProps(context):
    post = load_post(context["params"]["id"])
    if not post:
        raise PageNotFoundError()
    return {"props": {"post": post}}


@getStaticPaths
def getStaticPaths():
    return StaticPathsResult(
        paths=[{"params": {"id": str(p.id)}} for p in recent_posts()],
        fallback="blocking",
    )"""

    hydration_example = """<!-- What the server emits for an interactive island -->
<div id="psx_component_3" data-component-id="psx_component_3"
     data-psx-hydrate="visible" class="nextpy-component">
    <!-- fully rendered SSR HTML — usable before JS loads -->
    <button onclick="...">Increment</button>
</div>

<!-- CSP-friendly JSON bootstrap read by the hydration script -->
<script type="application/json" id="__PSX_DATA__-psx_component_3">
    {"count": 0, "title": "Hello"}
</script>
<script>/* generated hydration script: state, handlers, bindings */</script>"""

    queue_example = """from nextpy import get_queue, enqueue, task, BackgroundQueue

# Named queues — each gets its own ThreadPoolExecutor
emails = get_queue("emails")
reports = BackgroundQueue("reports", workers=4, max_retries=3, retry_delay=5.0)


@task                      # decorator on the default queue
def send_receipt(order_id: str):
    ...


@emails.task
def send_welcome(user_id: str):
    ...


# submit() / enqueue() return a concurrent.futures.Future immediately
future = enqueue(render_invoice, "inv_123")
future.result(timeout=30)  # optional: block for the result

queue = get_queue("reports")
queue.stats.to_dict()      # submitted / completed / failed / retried / running"""

    realtime_example = """from nextpy import get_queue, enqueue, task
from nextpy.state_sync import set_state
from nextpy.websocket import manager


@task
def fan_out_score(user_id: str, score: int):
    # 1. update shared server state -> broadcasts STATE_CHANGE to /ws clients
    import asyncio
    asyncio.run(set_state(f"score:{user_id}", score))

    # 2. publish to a named channel for targeted subscribers
    import asyncio
    asyncio.run(manager.publish("leaderboard", {
        "type": "SCORE",
        "user": user_id,
        "score": score,
    }))


# From a request handler — returns immediately, work runs in background
future = enqueue(fan_out_score, "u_42", 9000)"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Core Concepts</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Architecture Overview</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Architecture Overview
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy is a single-process Python web framework: a Starlette/FastAPI ASGI app serves file-based routes, renders PSX components to HTML on the server, ships a JSON bootstrap plus generated hydration scripts to the browser, and keeps clients in sync over a WebSocket channel. This page maps every layer of that system and follows one request end-to-end.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The big picture</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        A NextPy app is one ASGI application built by <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">create_app()</code> in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy/server/app.py</code>. The <code class="font-mono text-xs">NextPyApp</code> class wires together the middleware stack, static mounts, the WebSocket endpoint, server actions, and a <code class="font-mono text-xs">ComponentRouter</code> that scans <code class="font-mono text-xs">pages/</code> into routes. Everything a page needs — routing, rendering, caching, hydration, realtime — lives inside that one process.
                    </p>

                    <div class="rounded-xl border border-zinc-800 bg-zinc-950/40 p-6 space-y-3 font-mono text-xs">
                        <div class="flex flex-wrap items-center justify-center gap-2">
                            <div class="px-4 py-2 rounded-lg border border-sky-500/40 bg-sky-500/10 text-sky-300">Browser</div>
                            <div class="text-zinc-500 text-base">→</div>
                            <div class="px-4 py-2 rounded-lg border border-violet-500/40 bg-violet-500/10 text-violet-300">/ws WebSocket + /__nextpy/hmr SSE</div>
                            <div class="text-zinc-500 text-base">→</div>
                            <div class="px-4 py-2 rounded-lg border border-emerald-500/40 bg-emerald-500/10 text-emerald-300">GET /posts/&#123;id&#125; → HTML</div>
                        </div>
                        <div class="text-center text-zinc-500">↓ request enters the ASGI app (create_app → NextPyApp)</div>
                        <div class="grid sm:grid-cols-2 gap-2">
                            <div class="p-3 rounded-lg border border-zinc-700 bg-zinc-900/60">
                                <div class="text-amber-400 font-semibold mb-1">Middleware stack</div>
                                <div class="text-zinc-400">CORS → security headers → rate limit → CSRF → gzip → cache → core timing</div>
                            </div>
                            <div class="p-3 rounded-lg border border-zinc-700 bg-zinc-900/60">
                                <div class="text-blue-400 font-semibold mb-1">ComponentRouter</div>
                                <div class="text-zinc-400">match route → data fetching → SSR/SSG/ISR/stream → HTML + hydration payload</div>
                            </div>
                            <div class="p-3 rounded-lg border border-zinc-700 bg-zinc-900/60">
                                <div class="text-emerald-400 font-semibold mb-1">PSX runtime (client)</div>
                                <div class="text-zinc-400">__PSX_DATA__ bootstrap → per-key signals → rAF-batched DOM updates → SPA navigation</div>
                            </div>
                            <div class="p-3 rounded-lg border border-zinc-700 bg-zinc-900/60">
                                <div class="text-rose-400 font-semibold mb-1">Side channels</div>
                                <div class="text-zinc-400">/ws state sync · BackgroundQueue tasks · MemoryCache + ISR page cache</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div id="request-lifecycle" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Request lifecycle, end to end</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Here is the exact path a page request takes through <code class="font-mono text-xs">NextPyApp._handle_request</code>. The same pipeline serves every render strategy — the strategy only changes <em>when</em> and <em>whether</em> the HTML is cached.
                    </p>
                    <div class="rounded-xl border border-zinc-800 bg-zinc-950/40 p-6 space-y-1 font-mono text-xs">
                        <div class="px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-900 text-zinc-200">1 · Browser sends GET /posts/42</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-amber-500/30 bg-amber-500/5 text-amber-300">2 · Middleware stack (security headers → rate limit → CSRF → gzip → cache headers → timing/HTMX)</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-blue-500/30 bg-blue-500/5 text-blue-300">3 · router.match(path) → Route + params (dynamic segments, layout chain resolved)</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-blue-500/30 bg-blue-500/5 text-blue-300">4 · execute_data_fetching — getServerSideProps / getStaticProps run, props merged into context</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-emerald-500/30 bg-emerald-500/5 text-emerald-300">5 · render_route — layouts wrap the page; components render to HTML; hydration islands wrapped</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-violet-500/30 bg-violet-500/5 text-violet-300">6 · inject client router script + HMR + __PSX_DATA__ bootstrap → HTMLResponse (or StreamingResponse)</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-sky-500/30 bg-sky-500/5 text-sky-300">7 · Browser parses HTML → hydration scripts activate islands → signals bind → SPA nav takes over</div>
                    </div>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li>SSR rendering is synchronous CPU work, so <code class="font-mono text-xs">_handle_request</code> offloads it with <code class="font-mono text-xs">asyncio.to_thread</code> — one expensive page can't stall concurrent requests.</li>
                        <li>If the module sets <code class="font-mono text-xs">streaming = True</code> or defines a <code class="font-mono text-xs">stream()</code> function, the response becomes a <code class="font-mono text-xs">StreamingResponse</code> with <code class="font-mono text-xs">X-NextPy-Streaming: true</code>.</li>
                        <li>Client-side navigations send <code class="font-mono text-xs">x-nextpy-fragment</code> + <code class="font-mono text-xs">x-nextpy-layout-sig</code> headers; when the layout signature matches, the server returns only the page fragment (<code class="font-mono text-xs">X-NextPy-Fragment: true</code>) instead of the full document.</li>
                        <li>API routes (<code class="font-mono text-xs">pages/api/*</code>) short-circuit at step 3 into <code class="font-mono text-xs">_handle_api_request</code> and never touch the HTML pipeline.</li>
                    </ul>
                </div>

                <div id="file-routing" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">File-based routing</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">ComponentRouter.scan_pages()</code> walks <code class="font-mono text-xs">pages/</code> for <code class="font-mono text-xs">*.py</code>, <code class="font-mono text-xs">*.py.jsx</code>, and <code class="font-mono text-xs">*.psx</code> files and turns the directory tree into routes. Folder names become path segments; special filenames get framework meaning.
                    </p>
                    <EnhancedCodeBlock lang="text" filename="pages/ tree" snippet={tree_example} />
                    <div class="grid sm:grid-cols-2 gap-4 mt-2">
                        <div class="p-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
                            <div class="text-sm font-semibold text-white mb-2">Special files</div>
                            <ul class="text-sm leading-6 text-zinc-400 space-y-1">
                                <li><code class="font-mono text-xs">layout.py</code> — wraps child routes; chains nest inside-out from root to leaf</li>
                                <li><code class="font-mono text-xs">loading.py</code> — Suspense fallback while data loads</li>
                                <li><code class="font-mono text-xs">error.py</code> — error boundary for the segment</li>
                                <li><code class="font-mono text-xs">not-found.py</code> — custom 404 UI</li>
                                <li><code class="font-mono text-xs">template.py</code> — re-mounts on navigation (vs. layouts which persist)</li>
                            </ul>
                        </div>
                        <div class="p-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
                            <div class="text-sm font-semibold text-white mb-2">Dynamic segments</div>
                            <ul class="text-sm leading-6 text-zinc-400 space-y-1">
                                <li><code class="font-mono text-xs">[id].py</code> — one segment → <code class="font-mono text-xs">/posts/&#123;id&#125;</code>, exposed via <code class="font-mono text-xs">context["params"]</code></li>
                                <li><code class="font-mono text-xs">[...slug].py</code> — catch-all → <code class="font-mono text-xs">/docs/a/b/c</code></li>
                                <li><code class="font-mono text-xs">api/*.py</code> — routed as API endpoints, not pages</li>
                                <li>Matched values arrive as regex named groups (<code class="font-mono text-xs">(?P&lt;id&gt;[^/]+)</code>)</li>
                            </ul>
                        </div>
                    </div>
                    <p class="text-base leading-7 text-zinc-300">
                        Layouts are cached by file mtime (<code class="font-mono text-xs">_layout_cache</code>), and each route carries a <code class="font-mono text-xs">layout_chain</code> built inside-out — root <code class="font-mono text-xs">layout.py</code> first, leaf layout last — so nested layouts compose like React's app router.
                    </p>
                </div>

                <div id="compile-pipeline" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The compile pipeline</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Pages are ordinary Python files with JSX syntax. Two loaders handle them: <code class="font-mono text-xs">.py</code> files go through <code class="font-mono text-xs">jsx_preprocessor.preprocess_content</code>, which finds <code class="font-mono text-xs">return (&lt;...&gt;)</code> blocks and rewrites them as <code class="font-mono text-xs">psx()</code> calls wrapping the JSX in a triple-quoted string (auto-injecting <code class="font-mono text-xs">from nextpy.psx import component, psx</code> when needed). <code class="font-mono text-xs">.jsx</code>/<code class="font-mono text-xs">.psx</code> files are loaded through <code class="font-mono text-xs">jsx_transformer</code>'s custom import hook instead.
                    </p>
                    <div class="rounded-xl border border-zinc-800 bg-zinc-950/40 p-6 space-y-1 font-mono text-xs">
                        <div class="px-3 py-2 rounded-lg border border-zinc-700 bg-zinc-900 text-zinc-200">pages/posts/[id].py on disk (JSX inside Python)</div>
                        <div class="text-center text-zinc-500">↓ preprocess_content — find_jsx_blocks → transform_jsx_to_psx_call</div>
                        <div class="px-3 py-2 rounded-lg border border-blue-500/30 bg-blue-500/5 text-blue-300">Valid Python: return psx(triple-quoted JSX)</div>
                        <div class="text-center text-zinc-500">↓ module executes — psx() builds a VNode tree (expressions evaluated lazily)</div>
                        <div class="px-3 py-2 rounded-lg border border-emerald-500/30 bg-emerald-500/5 text-emerald-300">render_psx_component / PSXRenderer → HTML string (+ hydration wrappers for islands)</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-violet-500/30 bg-violet-500/5 text-violet-300">Browser receives HTML + inline hydration scripts</div>
                    </div>
                    <p class="text-base leading-7 text-zinc-300">
                        For interactive pages, <code class="font-mono text-xs">@interactive_component</code> wraps the render so the output becomes a hydration island: a <code class="font-mono text-xs">&lt;div id="psx_component_N" data-psx-hydrate="..."&gt;</code> wrapper plus a JSON bootstrap and a generated script. See <a href="/documentation/concepts/psx-internals" class="text-blue-400 hover:text-blue-300">PSX Core Internals</a> for the parser/evaluator details.
                    </p>
                </div>

                <div id="middleware" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Middleware stack</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Starlette middleware is onion-style: each layer can short-circuit or decorate the request/response. <code class="font-mono text-xs">NextPyApp._setup_middleware</code> registers them in a fixed order — because Starlette wraps last-added outermost, the effective request path is:
                    </p>
                    <div class="rounded-xl border border-zinc-800 bg-zinc-950/40 p-6 space-y-1 font-mono text-xs">
                        <div class="px-3 py-2 rounded-lg border border-rose-500/30 bg-rose-500/5 text-rose-300">outermost · Security headers — CSP, X-Frame-Options DENY, HSTS, Permissions-Policy</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-amber-500/30 bg-amber-500/5 text-amber-300">RateLimitMiddleware — 429 + Retry-After; 60/min on auth paths, 240/min on /api and /__nextpy</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-amber-500/30 bg-amber-500/5 text-amber-300">CSRFMiddleware — Origin/Referer check for cookie-authenticated unsafe methods (403 on failure)</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-zinc-600 bg-zinc-900 text-zinc-300">GZipMiddleware — compresses responses ≥ 1 KB (hydration scripts are large)</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-zinc-600 bg-zinc-900 text-zinc-300">CacheMiddleware — Cache-Control: immutable on assets and /_nextpy/*</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-blue-500/30 bg-blue-500/5 text-blue-300">NextPyMiddleware — X-Process-Time, nosniff/SAMEORIGIN, HTMX detection (HX-Request, HX-Target)</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-zinc-600 bg-zinc-900 text-zinc-300">innermost · CORSMiddleware — CORS_ORIGINS env (defaults to *)</div>
                        <div class="text-center text-zinc-500">↓</div>
                        <div class="px-3 py-2 rounded-lg border border-emerald-500/30 bg-emerald-500/5 text-emerald-300">router / endpoint</div>
                    </div>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">AuthMiddleware</code> exists in <code class="font-mono text-xs">server/middleware.py</code> but is opt-in — wrap protected paths yourself or use route-level guards.</li>
                        <li>Responses unwind in reverse: CORS headers are added first, security headers last, so every layer sees the final response.</li>
                        <li>All security middleware can be tuned or disabled via env vars (<code class="font-mono text-xs">CSRF_PROTECTION</code>, <code class="font-mono text-xs">RATE_LIMIT_ENABLED</code>, <code class="font-mono text-xs">CORS_ORIGINS</code>, <code class="font-mono text-xs">CSRF_TRUSTED_ORIGINS</code>).</li>
                    </ul>
                </div>

                <div id="render-strategies" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Render strategies compared</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The same <code class="font-mono text-xs">_handle_request</code> pipeline produces five different delivery modes depending on page module attributes and request headers:
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800">
                        <table class="w-full text-sm">
                            <thead>
                                <tr class="border-b border-zinc-800 bg-zinc-900/60 text-left">
                                    <th class="px-4 py-3 font-semibold text-white">Strategy</th>
                                    <th class="px-4 py-3 font-semibold text-white">When HTML is generated</th>
                                    <th class="px-4 py-3 font-semibold text-white">Use case</th>
                                    <th class="px-4 py-3 font-semibold text-white">Caching</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr>
                                    <td class="px-4 py-3 font-medium text-blue-400">SSR</td>
                                    <td class="px-4 py-3">Every request, fresh</td>
                                    <td class="px-4 py-3">Personalized pages, dashboards, live data</td>
                                    <td class="px-4 py-3">no-store / no-cache</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-medium text-emerald-400">SSG</td>
                                    <td class="px-4 py-3">Once per path via getStaticPaths + getStaticProps</td>
                                    <td class="px-4 py-3">Docs, marketing pages, product catalogs</td>
                                    <td class="px-4 py-3">Immutable page cache, ETag/304</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-medium text-amber-400">ISR</td>
                                    <td class="px-4 py-3">First request, then revalidated in background</td>
                                    <td class="px-4 py-3">Blog posts, listings — fresh-ish without per-request cost</td>
                                    <td class="px-4 py-3">TTL via <code class="font-mono text-xs">revalidate</code>; stale-while-revalidate</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-medium text-violet-400">Streaming</td>
                                    <td class="px-4 py-3">Per request, chunked as it renders</td>
                                    <td class="px-4 py-3">Slow data fetches, large pages — early first paint</td>
                                    <td class="px-4 py-3">StreamingResponse; ISR headers if cacheable</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-3 font-medium text-sky-400">SPA navigation</td>
                                    <td class="px-4 py-3">Client fetches fragment after hydration</td>
                                    <td class="px-4 py-3">In-app page transitions, no full reload</td>
                                    <td class="px-4 py-3">Fragment responses skip unchanged layouts (layout signature)</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/posts/[id].py" snippet={page_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li>Pages with <code class="font-mono text-xs">getServerSideProps</code> are never cached — <code class="font-mono text-xs">is_cacheable()</code> explicitly excludes them.</li>
                        <li>ISR entries are stored in an in-process OrderedDict keyed by route + context; mtime checks on the page and every layout file invalidate stale entries, and a background thread refreshes expired pages (stale-while-revalidate).</li>
                        <li>Errors are never cached — HTML containing the error overlay forces <code class="font-mono text-xs">Cache-Control: no-store</code> and status 500.</li>
                        <li>Conditional requests are honored: matching <code class="font-mono text-xs">If-None-Match</code> gets a 304.</li>
                    </ul>
                </div>

                <div id="hydration" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Hydration &amp; selective activation</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Server-rendered HTML is fully usable before any JavaScript runs. Interactivity is layered on afterwards by the hydration engine (<code class="font-mono text-xs">psx/hydration/engine.py</code>), which wraps each interactive component and emits three things: the island wrapper, a JSON bootstrap, and a generated script.
                    </p>
                    <EnhancedCodeBlock lang="html" filename="rendered output" snippet={hydration_example} />
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300">
                        <li><strong class="text-white">__PSX_DATA__ bootstrap</strong> — initial state (useState values plus JSON-safe props) is serialized into <code class="font-mono text-xs">&lt;script type="application/json" id="__PSX_DATA__-&#123;id&#125;"&gt;</code>. CSP-friendly and lazily parsed; non-JSON-safe props are filtered out server-side so request objects never reach the client.</li>
                        <li><strong class="text-white">Selective hydration</strong> — <code class="font-mono text-xs">data-psx-hydrate</code> picks a strategy: <code class="font-mono text-xs">eager</code> (hydrate on DOMContentLoaded), <code class="font-mono text-xs">visible</code> (IntersectionObserver, 200px margin), <code class="font-mono text-xs">interaction</code> (first pointerdown/focusin/keydown inside the island), or <code class="font-mono text-xs">idle</code> (requestIdleCallback). The SSR DOM is never rebuilt — hydration only binds listeners and state to existing nodes.</li>
                        <li><strong class="text-white">Signals &amp; fine-grained updates</strong> — the client runtime (<code class="font-mono text-xs">NextPyActionRuntime</code>) keeps a per-component, per-key <code class="font-mono text-xs">PSXSignal</code>. JSX expressions like &#123;count + 1&#125; compile to bindings that subscribe to exactly the keys they read, so a setter re-evaluates only dependent expressions — not the whole component.</li>
                        <li><strong class="text-white">requestAnimationFrame batching</strong> — state writes coalesce DOM mutations into a single rAF flush (with a setTimeout fallback for hidden tabs), so rapid updates can't trigger layout thrash.</li>
                        <li><strong class="text-white">SPA retry</strong> — hydration scripts poll for their island element (up to 10 × 50ms) so components injected by client-side navigation still activate.</li>
                    </ul>
                </div>

                <div id="realtime" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Realtime &amp; state sync</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy exposes one WebSocket endpoint, <code class="font-mono text-xs">/ws</code> (<code class="font-mono text-xs">websocket.py</code>), guarded by the same trusted-origin check as CSRF. A global <code class="font-mono text-xs">ConnectionManager</code> tracks clients by ID and supports named channels plus structured events.
                    </p>
                    <div class="grid sm:grid-cols-2 gap-4">
                        <div class="p-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
                            <div class="text-sm font-semibold text-white mb-2">Wire protocol</div>
                            <ul class="text-sm leading-6 text-zinc-400 space-y-1">
                                <li>Client → server JSON messages: <code class="font-mono text-xs">subscribe</code>, <code class="font-mono text-xs">publish</code>, <code class="font-mono text-xs">broadcast</code>, <code class="font-mono text-xs">state_update</code>, <code class="font-mono text-xs">component_event</code>, <code class="font-mono text-xs">sync_request</code>, <code class="font-mono text-xs">ping</code></li>
                                <li>Server → client events: <code class="font-mono text-xs">CONNECTION_ESTABLISHED</code>, <code class="font-mono text-xs">SUBSCRIPTION_CONFIRMED</code>, <code class="font-mono text-xs">STATE_UPDATE</code>, <code class="font-mono text-xs">COMPONENT_EVENT</code>, <code class="font-mono text-xs">UI_UPDATE</code>, <code class="font-mono text-xs">SYNC_RESPONSE</code></li>
                                <li><code class="font-mono text-xs">emit_state_update</code> stores per-component state (capped at 5000) so late joiners can sync</li>
                            </ul>
                        </div>
                        <div class="p-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
                            <div class="text-sm font-semibold text-white mb-2">State sync layer</div>
                            <ul class="text-sm leading-6 text-zinc-400 space-y-1">
                                <li><code class="font-mono text-xs">StateManager</code> (<code class="font-mono text-xs">state_sync.py</code>) — keyed async state with per-key locks, version counter, and 100-snapshot history</li>
                                <li><code class="font-mono text-xs">set()</code> broadcasts a <code class="font-mono text-xs">STATE_CHANGE</code> event to every connected client</li>
                                <li><code class="font-mono text-xs">ServerState</code> — React-style useState hook over shared keys; <code class="font-mono text-xs">DatabaseState</code> — same API persisted to a SQL table with in-memory cache</li>
                                <li>Module helpers: <code class="font-mono text-xs">get_state</code>, <code class="font-mono text-xs">set_state</code>, <code class="font-mono text-xs">update_state</code>, <code class="font-mono text-xs">delete_state</code>, <code class="font-mono text-xs">get_state_manager</code></li>
                            </ul>
                        </div>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="tasks/realtime.py" snippet={realtime_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        A second realtime channel exists for development only: <code class="font-mono text-xs">GET /__nextpy/hmr</code> is a Server-Sent Events stream that pushes a reload event to every open tab when watched files change (<code class="font-mono text-xs">broadcast_hot_reload()</code> can trigger it manually).
                    </p>
                </div>

                <div id="background-caching" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Background work &amp; caching layers</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Two in-process facilities keep request handling fast: a retrying thread-pool queue for deferred work, and three nested cache layers for rendered output and data.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="tasks/queue.py" snippet={queue_example} />
                    <div class="grid sm:grid-cols-3 gap-4 mt-2">
                        <div class="p-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
                            <div class="text-sm font-semibold text-emerald-400 mb-2">ISR page cache</div>
                            <p class="text-sm leading-6 text-zinc-400">In-process OrderedDict of rendered HTML per route+context; TTL from <code class="font-mono text-xs">revalidate</code>, invalidated by file mtime, refreshed by background threads.</p>
                        </div>
                        <div class="p-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
                            <div class="text-sm font-semibold text-amber-400 mb-2">MemoryCache</div>
                            <p class="text-sm leading-6 text-zinc-400"><code class="font-mono text-xs">nextpy.cache</code> — thread-safe TTL store (maxsize 2048) for arbitrary keys; <code class="font-mono text-xs">@cached</code> decorator for functions.</p>
                        </div>
                        <div class="p-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
                            <div class="text-sm font-semibold text-blue-400 mb-2">HTTP caches</div>
                            <p class="text-sm leading-6 text-zinc-400">CacheMiddleware sets immutable headers on assets; ETag/304 handling on pages; browser fragment cache via layout signatures.</p>
                        </div>
                    </div>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">BackgroundQueue</code> is process-local and dependency-free — swap in Celery/RQ behind the same <code class="font-mono text-xs">submit</code> API for multi-worker deployments.</li>
                        <li>Coroutines are supported: async functions submitted to a queue run via <code class="font-mono text-xs">asyncio.run</code> inside the worker thread.</li>
                        <li>Caches are per-process — with multiple workers, each maintains its own ISR entries and MemoryCache.</li>
                    </ul>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/concepts/why-nextpy" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Why NextPy?
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/concepts/psx-internals" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                PSX Core Internals
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
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The big picture</a></li>
                        <li><a href="#request-lifecycle" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Request lifecycle</a></li>
                        <li><a href="#file-routing" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">File-based routing</a></li>
                        <li><a href="#compile-pipeline" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Compile pipeline</a></li>
                        <li><a href="#middleware" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Middleware stack</a></li>
                        <li><a href="#render-strategies" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Render strategies</a></li>
                        <li><a href="#hydration" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Hydration</a></li>
                        <li><a href="#realtime" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Realtime &amp; state sync</a></li>
                        <li><a href="#background-caching" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Background work &amp; caching</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Architecture Overview - NextPy Docs"}}


default = Architecture
