"""Dashboard App - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def DashboardApp():
    data_example = '''from nextpy.psx import component

def getServerSideProps(context):
    """Fetch dashboard data on the server before render."""
    stats = {"users": 1284, "revenue": 48200, "orders": 342}
    recent = [{"id": 1, "name": "Acme Corp", "amount": 1200}]
    return {"props": {"stats": stats, "recent": recent}}

default = Dashboard'''

    widget_example = '''from nextpy.psx import interactive_component, useState, useEffect, callServerAction

@interactive_component
def StatCard():
    [period, set_period] = useState("7d")
    [stats, set_stats] = useState(props.get("stats", {}))
    [_server_result, _setServerResult] = useState(None)

    def Refresh():
        callServerAction("dashboard_stats", {"period": period})

    def HandleResult():
        if _server_result:
            set_stats(_server_result.get("stats", {}))

    useEffect(HandleResult, [_server_result])'''

    action_example = '''from nextpy.server_actions import server_action
from nextpy.db import get_session

@server_action()
async def dashboard_stats(request, period: str = "7d"):
    """Aggregate stats for the selected period."""
    db = get_session()
    try:
        # query your tables, aggregate, return plain JSON-safe dicts
        stats = {"users": 0, "revenue": 0, "orders": 0}
        return {"success": True, "stats": stats}
    finally:
        db.close()'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Tutorials</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Dashboard App</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Dashboard App
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        Build a comprehensive dashboard application with NextPy.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        A dashboard is mostly static markup plus a few interactive widgets. Load the initial data with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code> so the first paint already has numbers, then hydrate only the widgets that need live updates.
                    </p>
                </div>

                <div id="data-loading" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Loading initial data</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code> runs on the server per request (or per revalidation window for cached pages). Return JSON-safe values under <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">props</code> — they arrive as the component's initial props:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/dashboard.py" snippet={data_example} />
                </div>

                <div id="interactive-widgets" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Interactive widgets</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Filters, refresh buttons, and live counters belong in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@interactive_component</code> islands. Each widget hydrates independently — the static charts around them never re-render:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/stat_card.py" snippet={widget_example} />
                </div>

                <div id="refresh-action" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Refreshing data</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Period switches and manual refreshes call a server action that re-queries the database. The result lands in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_result</code> — no page reload:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="lib/dashboard_actions.py" snippet={action_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/tutorials/ai-chat" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                AI Chat App
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/installation" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Getting Started
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
                        <li><a href="#data-loading" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Loading data</a></li>
                        <li><a href="#interactive-widgets" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Interactive widgets</a></li>
                        <li><a href="#refresh-action" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Refreshing data</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Dashboard App - NextPy Docs"}}

default = DashboardApp

