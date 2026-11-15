"""Debugging & DevTools - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def DevtoolsDebugging():
    env_example = '''# .env — development defaults (all optional)
DEBUG=true                 # detailed errors + debug tooling
NEXTPY_DEBUG=true          # enables the debug panel / overlay
NEXTPY_DEBUG_ICON=true     # show the floating "NP" debug icon
NEXTPY_HOT_RELOAD=true     # browser reloads on file changes
NEXTPY_LOG_LEVEL=info      # trace | debug | info | warning | error'''

    cli_example = '''# Development server
nextpy dev                    # reload + debug on (defaults)
nextpy dev --no-reload        # dev server, single process
nextpy dev --no-debug         # dev server, no debug tooling

# Inspection helpers
nextpy info                   # framework + project status
nextpy routes                 # list every registered route

# Production (see the Deployment guide)
nextpy build                  # static build into out/
nextpy start                  # production server (4 workers, debug off)
nextpy export                 # static export into out/'''

    perf_example = '''from nextpy.psx import get_vdom_metrics
from nextpy.debug.performance import performance_monitor

# Time expensive work
performance_monitor.start_timer("heavy_render")
# ... render / compute ...
performance_monitor.end_timer("heavy_render", unit="ms")

# Counters for things that happen a lot
performance_monitor.increment_counter("api_calls")

# Inspect everything recorded so far
print(performance_monitor.get_all_metrics())
print(get_vdom_metrics())   # vdom render/update metrics'''

    manual_reload = '''from nextpy.websocket import broadcast_hot_reload

def save_and_reload():
    # ... persist data ...
    broadcast_hot_reload()   # every open tab reloads immediately'''

    hmr_flow = '''# What happens when you save a file
#
# 1. uvicorn --reload (watchdog) restarts the worker process
#    - watches pages/, components/, templates/, public/, styles/,
#      scripts/, .nextpy_framework/ for .py/.psx/.jsx/.css/.html/...
# 2. In-process watcher polls pages/ + templates/ mtimes every 0.4s
#    (0.6s debounce) and signals all SSE clients
# 3. Browser EventSource on /__nextpy/hmr receives "reload"
#    and calls window.location.reload()
# 4. Page modules are re-imported; the renderer's mtime cache
#    check invalidates stale compiled output automatically'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Debugging &amp; DevTools</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Debugging &amp; DevTools
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy ships with a development-mode debugging stack: detailed error pages, a live error overlay, a debug panel, hot reload over SSE, and performance instrumentation. This guide covers how it works and how to use it.
                    </p>
                </header>

                <div id="debug-vs-production" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Debug mode vs production</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Behavior is controlled by three environment flags loaded from your project <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.env</code>:
                    </p>
                    <ul class="list-disc list-inside space-y-2 text-zinc-300 ml-4">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">DEBUG</code> — detailed error pages with tracebacks, file paths, and source context.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NEXTPY_DEBUG</code> — the debug panel, overlay scripts, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/debug/*</code> endpoints.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">DEVELOPMENT</code> — enables the file watcher and the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/hmr</code> SSE channel.</li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-300">
                        In production (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy start</code> forces all three to <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">false</code>), error pages are sanitized — visitors see "An internal error occurred" instead of tracebacks, absolute file paths are stripped, and every <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/debug/*</code> route returns 404.
                    </p>
                    <EnhancedCodeBlock lang="bash" filename=".env" snippet={env_example} />
                </div>

                <div id="error-overlay" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The error overlay</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        When a page fails to render in dev mode, the renderer swaps in a dedicated error page instead of a blank screen. With <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">DEBUG=true</code> it shows the exception type, message, traceback, and the offending file with clickable line numbers; the fallback HTML includes buttons to close, highlight, copy, and get quick fix suggestions (e.g. null-reference hints). In production the same failure renders a generic "Internal Server Error" page with none of those internals.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        On top of that, dev mode injects a live client-side overlay: a WebSocket client connects to <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/ws</code>, receives structured events (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">STATE_UPDATE</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">COMPONENT_EVENT</code>, error broadcasts) and pops an overlay the moment something breaks — no console digging required.
                    </p>
                </div>

                <div id="debug-panel" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The debug panel</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        A floating "NP" badge (bottom-right, controlled by <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NEXTPY_DEBUG_ICON</code>) opens the NextPy debug panel. It shows the active debug session, tracked component states, recent events, performance metrics, and WebSocket status, plus tools to start/end a session, export the collected data as JSON, or clear it. The panel talks to the debug API endpoints listed below.
                    </p>
                </div>

                <div id="hot-reload" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Hot reload mechanics</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Two mechanisms work together. First, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy dev</code> runs uvicorn with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">reload=True</code> (watchdog if installed, polling otherwise), watching <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">components/</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">templates/</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">public/</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">styles/</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">scripts/</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.nextpy_framework/</code> for Python, JSX, CSS, HTML, config and env changes — saving a file restarts the worker. Second, a lightweight in-process watcher polls the mtimes of <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">templates/</code> every 0.4s (0.6s debounce) and pushes a reload signal over SSE so every open browser tab refreshes the moment the new server is ready. EventSource auto-reconnects with backoff after restarts.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        You can also trigger a browser reload manually from server code:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={manual_reload} />
                    <EnhancedCodeBlock lang="text" filename="reload-flow.txt" snippet={hmr_flow} />
                    <p class="text-base leading-7 text-zinc-300">
                        On the render side, the component renderer validates its module cache by file mtime — a changed <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.py</code>/<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.psx</code> file is recompiled and re-imported on the next request, and layout modules are cached keyed on their mtime too. Route caches are never reused for error pages, so a fixed bug shows up immediately.
                    </p>
                </div>

                <div id="nextpy-endpoints" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The /__nextpy/* endpoints</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy reserves the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/</code> prefix for framework internals. Most are dev-only; the server-actions routes are always available:
                    </p>
                    <ul class="list-disc list-inside space-y-2 text-zinc-300 ml-4">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/hmr</code> — SSE stream that pushes <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">reload</code> events to browser tabs (404 unless <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">DEVELOPMENT=true</code>).</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/debug/components|events|performance|websocket</code> — GET endpoints feeding the debug panel (debug mode only).</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/debug/start|end|clear</code> — POST session control; <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/debug/export</code> — GET a JSON dump of the session.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/actions</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/actions/execute</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/actions/&#123;name&#125;/schema</code> — list, run, and inspect server actions.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/ws</code> — the WebSocket channel used by the live overlay and realtime features.</li>
                    </ul>
                </div>

                <div id="cli-tools" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">CLI inspection tools</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Beyond <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy dev</code>, two read-only commands help you verify what the framework sees:
                    </p>
                    <EnhancedCodeBlock lang="bash" filename="terminal" snippet={cli_example} />
                    <ul class="list-disc list-inside space-y-2 text-zinc-300 ml-4">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy info</code> — prints the NextPy version, Python version, watchdog availability (hot reload falls back to polling without it), and whether <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">components/</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">templates/</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">public/</code> exist.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy routes</code> — scans <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code> and lists every page and API route with its file path, flagging dynamic routes.</li>
                    </ul>
                </div>

                <div id="performance" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Performance debugging</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The debug performance monitor (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.debug.performance.performance_monitor</code>) records timers, counters, and averages — render hooks, component mount/update counts, and memory samples feed into it automatically, and everything is visible in the debug panel's Performance section and the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/debug/performance</code> endpoint. For client-side VDOM stats, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_vdom_metrics()</code> returns the renderer's render/update counters.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="lib/metrics.py" snippet={perf_example} />
                </div>

                <div id="workflow" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">A typical debugging workflow</h2>
                    <ol class="list-decimal list-inside space-y-2 text-zinc-300 ml-4">
                        <li>Run <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy dev</code> and keep the terminal visible — Python tracebacks print there on server errors.</li>
                        <li>Edit a page or component and save — the browser reloads automatically via the SSE HMR channel; check the console for the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">[NextPy HMR]</code> log line.</li>
                        <li>If something breaks, the error overlay appears in the page with the traceback and file/line; click a location to attempt to open it in your editor.</li>
                        <li>Open the NP badge for component states, events, and performance; use Export to grab a JSON session dump for a bug report.</li>
                        <li>Verify routes with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy routes</code> when a URL doesn't match what you expect.</li>
                    </ol>
                </div>

                <div id="prod-checklist" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Dev vs production checklist</h2>
                    <ul class="list-disc list-inside space-y-2 text-zinc-300 ml-4">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy start</code> sets <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">DEBUG=false</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NEXTPY_DEBUG=false</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">DEVELOPMENT=false</code> — no overlay, no debug panel, sanitized errors.</li>
                        <li>The HMR watcher and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/hmr</code> endpoint are disabled when <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">DEVELOPMENT</code> is not <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">true</code>.</li>
                        <li>Set <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NEXTPY_LOG_LEVEL=warning</code> (or higher) in production to quiet framework logs; uvicorn itself runs at <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">warning</code> level under <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy start</code>.</li>
                        <li>Before shipping, run <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy build</code> (or <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy export</code>) and smoke-test with debug off — see the <Link href="/documentation/howto/deployment" className="text-blue-400 hover:underline">Deployment Guide</Link>.</li>
                    </ul>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/testing" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Testing (Unit &amp; E2E)
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/deployment" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Deployment Guide
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
                        <li><a href="#debug-vs-production" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Debug vs production</a></li>
                        <li><a href="#error-overlay" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The error overlay</a></li>
                        <li><a href="#debug-panel" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The debug panel</a></li>
                        <li><a href="#hot-reload" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Hot reload mechanics</a></li>
                        <li><a href="#nextpy-endpoints" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">/__nextpy/* endpoints</a></li>
                        <li><a href="#cli-tools" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">CLI inspection tools</a></li>
                        <li><a href="#performance" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Performance debugging</a></li>
                        <li><a href="#workflow" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Debugging workflow</a></li>
                        <li><a href="#prod-checklist" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Dev vs prod checklist</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Debugging & DevTools - NextPy Docs"}}

default = DevtoolsDebugging
