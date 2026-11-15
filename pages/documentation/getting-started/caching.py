"""Caching & Revalidation — NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def CachingGuide():
    ssr_ttl_example = """from nextpy.psx import component
from nextpy import get_server_side_props
from nextpy.core.data_fetching import PropsResult

@component
def Page(props):
    return <p>{props.get("generated_at", "")}</p>

@get_server_side_props
async def getServerSideProps(context):
    # Runs on every request — revalidate=0 means never cache
    return PropsResult(
        props={"generated_at": "fresh every request"},
        revalidate=0,
    )"""

    isr_example = """from nextpy.psx import component
from nextpy import get_static_props, get_static_paths
from nextpy.core.data_fetching import PropsResult, StaticPathsResult

revalidate = 3600  # module-level ISR default: 1 hour

@component
def Page(props):
    return <article><h1>{props.get("post", {}).get("title", "")}</h1></article>

@get_static_paths
def getStaticPaths():
    return StaticPathsResult(
        paths=[{"params": {"slug": "hello-world"}}],
        fallback="blocking",
    )

@get_static_props
async def getStaticProps(context):
    # context.params / context.query / context.req are available here.
    # Re-render at most once per `revalidate` seconds per path.
    post = await fetch_post(context.params["slug"])
    return PropsResult(props={"post": post}, revalidate=60)"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Getting Started</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Caching & Revalidation</span>
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
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Caching & Revalidation</h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy caches rendered pages and revalidates them on a timer — Incremental Static Regeneration. A stale page is served instantly while a fresh copy is generated in the background.
                    </p>
                </header>

                <div id="how-it-works" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">How it works</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        When a page's data functions return a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">revalidate</code> value (in seconds), the renderer stores the result and serves it from cache until the TTL expires. Responses carry <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">stale-while-revalidate</code> cache headers so browsers and CDNs cooperate.
                    </p>
                    <div class="p-8 rounded-xl border border-zinc-800/60 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-6 mt-6">
                        <div class="flex flex-col items-center gap-2">
                            <div class="bg-zinc-800/50 border border-zinc-700/50 rounded-lg px-4 py-3 text-sm font-mono text-zinc-300">Request</div>
                            <svg class="w-5 h-5 text-zinc-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 14l-7 7m0 0l-7-7m7 7V3"/></svg>
                        </div>
                        <div class="bg-zinc-800/50 border border-zinc-700/50 rounded-lg px-4 py-3 text-sm font-mono text-emerald-400">Cache hit<br/><span class="text-xs text-zinc-500">serve instantly</span></div>
                        <div class="text-zinc-600 font-mono">/</div>
                        <div class="bg-zinc-800/50 border border-zinc-700/50 rounded-lg px-4 py-3 text-sm font-mono text-amber-400">TTL expired<br/><span class="text-xs text-zinc-500">stale + revalidate</span></div>
                        <div class="text-zinc-600 font-mono">/</div>
                        <div class="bg-zinc-800/50 border border-zinc-700/50 rounded-lg px-4 py-3 text-sm font-mono text-blue-400">Fresh render<br/><span class="text-xs text-zinc-500">update cache</span></div>
                    </div>
                </div>

                <div id="setting-ttl" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Setting the TTL</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Three ways to control revalidation, checked in order — return value first, then module attribute:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/posts.py" snippet={ssr_ttl_example} />
                    <EnhancedCodeBlock lang="python" filename="pages/posts/[slug].py" snippet={isr_example} />
                </div>

                <div id="guidelines" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Guidelines</h2>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300">
                        <li><strong>User-specific data</strong> — never cache; use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">revalidate=0</code> or fetch client-side.</li>
                        <li><strong>Public content</strong> (posts, docs, products) — cache for minutes to hours.</li>
                        <li><strong>API routes</strong> — caching applies to page renders; API responses are not ISR-cached.</li>
                        <li>Combine with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">fallback="blocking"</code> so unlisted paths render on demand and then cache.</li>
                    </ul>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/getting-started/fetching-data" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Fetching Data
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/error-handling" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Error Handling
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
                        <li><a href="#how-it-works" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">How it works</a></li>
                        <li><a href="#setting-ttl" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Setting the TTL</a></li>
                        <li><a href="#guidelines" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Guidelines</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Caching & Revalidation - NextPy Docs"}}


default = CachingGuide

