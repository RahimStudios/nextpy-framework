"""Fetching Data — NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def FetchingDataGuide():
    ssr_example = """from nextpy.psx import component
from nextpy.db import get_session, Post
from nextpy import getServerSideProps

@component
def Page(props):
    posts = props.get("posts", [])
    return (
        &lt;ul&gt;
            {for post in posts:
                &lt;li key={post["id"]}&gt;{post["title"]}&lt;/li&gt;
            }
        &lt;/ul&gt;
    )

@getServerSideProps



def getServerSideProps(context):
    db = next(get_session())
    posts = db.query(Post).all()
    db.close()
    return {
        "props": {
            "posts": [{"id": p.id, "title": p.title} for p in posts]
        }
    }"""

    ssg_example = """from nextpy.psx import component
from nextpy import getStaticProps, getStaticPaths
from nextpy.db import get_session, Post
from nextpy.utils import PropsResult, StaticPathsResult

@component
def Page(props):
    post = props.get("post", {})
    return &lt;article&gt;&lt;h1&gt;{post.get("title", "")}&lt;/h1&gt;&lt;/article&gt;

@getStaticPaths
def getStaticPaths():
    db = next(get_session())
    posts = db.query(Post.id).all()
    db.close()
    return StaticPathsResult(
        paths=[{"params": {"slug": str(p.id)}} for p in posts],
        fallback="blocking",
    )

@getStaticProps
def getStaticProps(context):
    slug = context["params"]["slug"]
    db = next(get_session())
    post = db.query(Post).filter(Post.id == int(slug)).first()
    db.close()
    if not post:
        return PropsResult(notFound=True)
    return PropsResult(props={"post": {"id": post.id, "title": post.title}})"""

    client_example = """from nextpy.psx import interactive_component, useState, useEffect

@interactive_component
def WeatherWidget():
    [data, setData] = useState(None)
    [loading, setLoading] = useState(True)

    def setup():
        async def load():
            res = await fetch("/api/weather")
            setData(await res.json())
            setLoading(False)
        load()
        return None

    useEffect(setup, [])

    if loading:
        return &lt;p&gt;Loading…&lt;/p&gt;
    return &lt;p&gt;{data.get("temp", "?")}°C&lt;/p&gt;"""

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
                        <span class="text-white">Fetching Data</span>
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
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">Fetching Data</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        NextPy fetches data at three layers: server-side props for page loads, static generation for build-time content, and client-side hooks for interactive updates. Pick the layer that matches how fresh the data must be.
                    </p>
                </header>

                <div id="choosing-a-strategy" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Choosing a strategy</h2>
                    <div class="grid sm:grid-cols-3 gap-4 mt-4">
                        <div class="p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/50">
                            <div class="text-sm font-semibold text-blue-400 mb-2">Server-side</div>
                            <p class="text-sm leading-6 text-zinc-400">Fresh on every request. Best for user-specific or frequently changing data.</p>
                        </div>
                        <div class="p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/50">
                            <div class="text-sm font-semibold text-emerald-400 mb-2">Static</div>
                            <p class="text-sm leading-6 text-zinc-400">Built once, served instantly. Best for content that rarely changes.</p>
                        </div>
                        <div class="p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/50">
                            <div class="text-sm font-semibold text-violet-400 mb-2">Client-side</div>
                            <p class="text-sm leading-6 text-zinc-400">After hydration. Best for live updates without a page reload.</p>
                        </div>
                    </div>
                </div>

                <div id="server-side-props" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Server-side props</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Export <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code> (snake_case <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_server_side_props</code> also works) alongside your page component. It runs on the server for every request, receives a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">PageContext</code>, and returns props that become the component's <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">props</code> argument:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/posts.py" snippet={ssr_example} />
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        The <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">context</code> object exposes <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">params</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">query</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">req</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">res</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">preview</code>, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">locale</code>.
                    </p>
                </div>

                <div id="static-generation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Static generation</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        For dynamic routes that can be pre-rendered, combine <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getStaticPaths</code> with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getStaticProps</code>. Paths are enumerated at build time; unknown params are handled per the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">fallback</code> mode:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/posts/[slug].py" snippet={ssg_example} />
                    <div class="overflow-hidden rounded-xl border border-zinc-800/80 mt-6">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-400">
                                <tr><th class="text-left px-4 py-2.5 font-medium">fallback</th><th class="text-left px-4 py-2.5 font-medium">Behavior for unlisted params</th></tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">false</td><td class="px-4 py-2.5">404 — only listed paths exist</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">true</td><td class="px-4 py-2.5">Serve empty shell, generate on first request</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">blocking</td><td class="px-4 py-2.5">Server-render on demand, then cache</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="client-side" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Client-side fetching</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Inside an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@interactive_component</code>, fetch from your own <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/api</code> routes in a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useEffect</code>. State updates re-render only the component — no page reload:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/weather.py" snippet={client_example} />
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        For declarative fetching use the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useFetch(url)</code> hook, which returns <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">{'{'}data, loading, error, refetch{'}'}</code>.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/getting-started/linking" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Linking and Navigation
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/caching" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Caching & Revalidation
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
                        <li><a href="#choosing-a-strategy" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Choosing a strategy</a></li>
                        <li><a href="#server-side-props" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server-side props</a></li>
                        <li><a href="#static-generation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Static generation</a></li>
                        <li><a href="#client-side" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Client-side fetching</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Fetching Data - NextPy Docs"}}


default = FetchingDataGuide

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
