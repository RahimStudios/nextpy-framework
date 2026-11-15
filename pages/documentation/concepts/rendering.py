"""Rendering — NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def Rendering():
    modes_example = """# SSR — fresh HTML on every request
@getServerSideProps


def getServerSideProps(context):
    return {"props": {"user": get_current_user(context)}}

# SSG + ISR — build once, revalidate on a timer
revalidate = 3600

@getStaticPaths
def getStaticPaths():
    return StaticPathsResult(paths=[...], fallback="blocking")

@getStaticProps
def getStaticProps(context):
    return PropsResult(props={"post": load_post(context["params"]["slug"])})"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Core Concepts</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Rendering</span>
                    </div>
                    <div class="relative flex items-center rounded-md border border-zinc-800 bg-zinc-950 overflow-hidden">
                        <button class="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-zinc-300 hover:bg-zinc-900 transition-colors border-r border-zinc-800"
                            onclick="navigator.clipboard.writeText(document.querySelector('article').innerText);var l=this.querySelector('.cp-label');l.textContent='Copied';setTimeout(()=>l.textContent='Copy page',1500)">
                            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                            <span class="cp-label">Copy page</span>
                        </button>
                        <button class="px-2 py-1.5 text-zinc-500 hover:bg-zinc-900 hover:text-zinc-300 transition-colors"
                            onclick="var m=this.parentElement.querySelector('.copy-menu');m.style.display=m.style.display==='none'?'block':'none'">
                            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
                        </button>
                        <div class="copy-menu absolute right-0 top-full mt-1 w-44 rounded-lg border border-zinc-800 bg-zinc-900 shadow-xl z-50 py-1" style="display:none">
                            <button class="w-full text-left px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-800" onclick="navigator.clipboard.writeText(document.querySelector('article').innerText);this.closest('.copy-menu').style.display='none'">Copy page</button>
                            <button class="w-full text-left px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-800" onclick="navigator.clipboard.writeText(window.location.href);this.closest('.copy-menu').style.display='none'">Copy link</button>
                        </div>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Rendering</h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy renders pages on the server by default — real HTML for fast first paint and SEO — then layers client-side reactivity on top through hydration.
                    </p>
                </header>

                <div id="modes" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The four modes</h2>
                    <div class="grid sm:grid-cols-2 gap-4 mt-4">
                        <div class="p-5 rounded-xl border border-blue-500/30 bg-blue-500/5">
                            <div class="text-sm font-semibold text-blue-400 mb-2">SSR — Server-Side Rendering</div>
                            <p class="text-sm leading-6 text-zinc-400">Fresh HTML per request via <code class="text-zinc-200 font-mono text-xs">getServerSideProps</code>. Best for personalized or live data.</p>
                        </div>
                        <div class="p-5 rounded-xl border border-emerald-500/30 bg-emerald-500/5">
                            <div class="text-sm font-semibold text-emerald-400 mb-2">SSG — Static Generation</div>
                            <p class="text-sm leading-6 text-zinc-400">Pre-rendered paths via <code class="text-zinc-200 font-mono text-xs">getStaticPaths</code> + <code class="text-zinc-200 font-mono text-xs">getStaticProps</code>. Fastest possible response.</p>
                        </div>
                        <div class="p-5 rounded-xl border border-amber-500/30 bg-amber-500/5">
                            <div class="text-sm font-semibold text-amber-400 mb-2">ISR — Incremental Static Regeneration</div>
                            <p class="text-sm leading-6 text-zinc-400">Static page + <code class="text-zinc-200 font-mono text-xs">revalidate</code> TTL. Stale-while-revalidate freshness without per-request cost.</p>
                        </div>
                        <div class="p-5 rounded-xl border border-violet-500/30 bg-violet-500/5">
                            <div class="text-sm font-semibold text-violet-400 mb-2">CSR — Client Rendering</div>
                            <p class="text-sm leading-6 text-zinc-400"><code class="text-zinc-200 font-mono text-xs">@interactive_component</code> islands fetch and update in the browser after hydration.</p>
                        </div>
                    </div>
                </div>

                <div id="pipeline" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The render pipeline</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        For each request the server resolves the route, builds the layout chain, runs data-fetching functions, renders components to an HTML string, injects the router/HMR runtime and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">__PSX_DATA__</code>, and streams the result. Interactive components are wrapped with hydration markers so the client knows which islands to activate.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/posts.py" snippet={modes_example} />
                </div>

                <div id="choosing" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Choosing per page</h2>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300">
                        <li><strong>Dashboard / account pages</strong> — SSR with user context; never cache.</li>
                        <li><strong>Blog posts, docs, products</strong> — SSG paths + ISR revalidate.</li>
                        <li><strong>Live feeds, carts</strong> — SSR shell + client-side fetching islands.</li>
                        <li><strong>Landing pages</strong> — full static export via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy export</code>.</li>
                    </ul>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/concepts/routing-engine" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Routing Engine
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/concepts/state-model" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                State Management Model
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
                        <li><a href="#modes" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The four modes</a></li>
                        <li><a href="#pipeline" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The render pipeline</a></li>
                        <li><a href="#choosing" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Choosing per page</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Rendering - NextPy Docs"}}


default = Rendering

