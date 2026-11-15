"""Adopting Partial Fetching - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def PartialFetchingGuide():
    gssp_example = """# Server-side fetching — data is in the HTML on first paint
def getServerSideProps(context):
    data = await fetch_dashboard_data()
    return {"props": {"data": data}}

# Cached variant — regenerate at most once per `revalidate` seconds
def getStaticProps(context):
    return {"props": {"data": data}, "revalidate": 60}"""

    client_example = """# Client-side fetching — post-hydration loads
from nextpy.psx import interactive_component, useState, useEffect, callServerAction

@interactive_component
def LiveSearch():
    [query, set_query] = useState("")
    [items, set_items] = useState([])
    [_server_result, _setServerResult] = useState(None)

    def Fetch():
        callServerAction("search", {"q": query})

    def HandleResult():
        if _server_result:
            set_items(_server_result.get("items", []))

    useEffect(Fetch, [query])
    useEffect(HandleResult, [_server_result])"""

    snippet_0 = """from nextpy.psx import component, Suspense

@component
def UserProfile():
    return (
        <Suspense fallback="Loading...">
            <UserData />
        </Suspense>
    )"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Adopting Partial Fetching</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Adopting Partial Fetching
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        Learn how to use Suspense and Streaming for partial data fetching.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy supports Suspense boundaries and streaming for progressive loading of content.
                    </p>
                </div>

                <div id="suspense" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Suspense</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Use Suspense to show loading states:
                    </p>
                    
                    <EnhancedCodeBlock lang="python" filename="example.py" snippet={snippet_0} />
                </div>

                <div id="server-fetching" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Server-side fetching</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Most data loads on the server via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code> / <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getStaticProps</code> — the page arrives with data already in the HTML:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/dashboard.py" snippet={gssp_example} />
                </div>

                <div id="client-fetching" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Client-side fetching</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        For post-hydration loads — search-as-you-type, infinite scroll — call a server action or an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/api/</code> route and update state in the result handler:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/live_search.py" snippet={client_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/forms" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Forms & Validation
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/full-stack" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Full Stack Paradigms
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
                        <li><a href="#suspense" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Suspense</a></li>
                        <li><a href="#server-fetching" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server fetching</a></li>
                        <li><a href="#client-fetching" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Client fetching</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Adopting Partial Fetching - NextPy Docs"}}

default = PartialFetchingGuide

