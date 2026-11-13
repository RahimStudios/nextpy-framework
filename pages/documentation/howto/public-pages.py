"""Public & Static Pages - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def PublicPagesGuide():
    tree_example = '''my-app/
├── public/                  # static assets — served verbatim
│   ├── css/                 #   → /static/css/...
│   ├── images/              #   → /static/images/...
│   ├── favicon.ico          #   → /static/favicon.ico
│   └── robots.txt           #   → /static/robots.txt
└── pages/                   # routes — rendered by NextPy'''

    usage_example = '''# In markup or CSS, reference assets under /static
<img src="/static/images/logo.png" alt="Logo" />
<link rel="stylesheet" href="/static/css/docs.css" />'''

    ssg_example = '''# pages/blog/[slug].py — build-time data + enumerated paths

def getStaticProps(context):
    post = fetch_post(context.params.get("slug"))
    if post is None:
        return {"not_found": True}
    # revalidate=3600 → ISR: serve cached, regenerate hourly
    return {"props": {"post": post}, "revalidate": 3600}

def getStaticPaths():
    posts = fetch_all_slugs()
    return {
        "paths": [{"params": {"slug": p.slug}} for p in posts],
        "fallback": "blocking",   # unknown slugs render on-demand, then cache
    }'''

    ssr_example = '''def getServerSideProps(context):
    # Runs per request (or per revalidate window) — fresh data every time
    user = get_user_from_request(context.request)
    return {"props": {"user": user}}'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-12 w-full max-w-6xl mx-auto">
                <DocsScrollSpy />

            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-16 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-6">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Public & Static Pages</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">
                        Public & Static Pages
                    </h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Learn how to serve static assets and generate static pages in NextPy.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-400">
        Two mechanisms cover "static" content: the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">public/</code> folder serves assets verbatim, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getStaticProps</code> / <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getStaticPaths</code> pre-render pages with build-time data.
                    </p>
                </div>

                <div id="public-folder" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The public folder</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Anything in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">public/</code> is mounted under <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/static</code> and served as-is — no processing, no caching headers managed by the framework:
                    </p>
                    <EnhancedCodeBlock lang="text" filename="project tree" snippet={tree_example} />
                    <EnhancedCodeBlock lang="html" filename="usage" snippet={usage_example} />
                </div>

                <div id="static-generation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Static generation (SSG)</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getStaticProps</code> fetches data once at build time (or per revalidation window); <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getStaticPaths</code> enumerates the dynamic routes to pre-render:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/blog/[slug].py" snippet={ssg_example} />
                </div>

                <div id="when-ssr" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">When to use SSR instead</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Pages that depend on the request — cookies, auth, per-user data — belong in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code>, which runs on every request:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/dashboard.py" snippet={ssr_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/building" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Production Building
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/redirecting" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Redirecting & Rewrites
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
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Overview</a></li>
                        <li><a href="#public-folder" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Public folder</a></li>
                        <li><a href="#static-generation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Static generation</a></li>
                        <li><a href="#when-ssr" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">When to use SSR</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )




def getServerSideProps(context):
    return {"props": {"title": "Public & Static Pages - NextPy Docs"}}

default = PublicPagesGuide

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
