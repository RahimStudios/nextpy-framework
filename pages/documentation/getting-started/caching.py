"""Caching & Revalidation — NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def CachingGuide():
    ssr_ttl_example = """from nextpy.psx import component
from nextpy import get_server_side_props
from nextpy.core.data_fetching import PropsResult

@component
def Page(props):
    return &lt;p&gt;{props.get("generated_at", "")}&lt;/p&gt;

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
    return &lt;article&gt;&lt;h1&gt;{props.get("post", {}).get("title", "")}&lt;/h1&gt;&lt;/article&gt;

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
        <div class="flex flex-col xl:flex-row items-start justify-between gap-12 w-full max-w-6xl mx-auto">
                <DocsScrollSpy />

            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-16 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-6">
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
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">Caching & Revalidation</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        NextPy caches rendered pages and revalidates them on a timer — Incremental Static Regeneration. A stale page is served instantly while a fresh copy is generated in the background.
                    </p>
                </header>

                <div id="how-it-works" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">How it works</h2>
                    <p class="text-base leading-7 text-zinc-400">
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
                    <p class="text-base leading-7 text-zinc-400">
                        Three ways to control revalidation, checked in order — return value first, then module attribute:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/posts.py" snippet={ssr_ttl_example} />
                    <EnhancedCodeBlock lang="python" filename="pages/posts/[slug].py" snippet={isr_example} />
                </div>

                <div id="guidelines" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Guidelines</h2>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
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

            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-6 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
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

@interactive_component
def DocsScrollSpy():
    [scroll_progress, set_scroll_progress] = useState(0)

    def SetupScroll():
        def OnScroll():
            doc_height = document.documentElement.scrollHeight - window.innerHeight
            if doc_height > 0:
                set_scroll_progress((window.scrollY / doc_height) * 100)

            current = ""
            sections = document.querySelectorAll("article div[id], article header[id], section[id]")
            for sec in sections:
                rect = sec.getBoundingClientRect()
                if rect.top <= 160:
                    current = sec.id
                in_view = rect.top < window.innerHeight * 0.92 and rect.bottom > 0
                if in_view:
                    sec.setAttribute("data-docs-revealed", "")
                else:
                    sec.removeAttribute("data-docs-revealed")

            links = document.querySelectorAll("aside a[href^='#'], nav a[href^='#']")
            for a in links:
                if a.getAttribute("href") == "#" + current:
                    a.setAttribute("data-docs-toc-active", "")
                else:
                    a.removeAttribute("data-docs-toc-active")

            path = window.location.pathname
            nav_links = document.querySelectorAll("aside a[href^='/']")
            for a in nav_links:
                if a.getAttribute("href") == path:
                    a.setAttribute("data-docs-nav-active", "")
                    parent = a.closest("details")
                    if parent:
                        parent.setAttribute("open", "")
                else:
                    a.removeAttribute("data-docs-nav-active")

        sections = document.querySelectorAll("article div[id], article header[id], section[id]")
        for sec in sections:
            sec.setAttribute("data-docs-reveal", "")

        window.addEventListener("scroll", OnScroll)
        document.addEventListener("nextpy:navigate", OnScroll)
        OnScroll()
        return lambda: window.removeEventListener("scroll", OnScroll)

    useEffect(SetupScroll, [])

    progress_style = f"width: {scroll_progress}%"

    return (
        <div class="fixed top-0 left-0 right-0 z-[70] h-[3px] pointer-events-none">
            <div style={progress_style} class="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 transition-[width] duration-100"></div>
        </div>
    )

register_component("DocsScrollSpy", DocsScrollSpy)
