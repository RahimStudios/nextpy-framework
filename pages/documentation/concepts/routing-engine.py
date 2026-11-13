"""Routing Engine — NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def RoutingEngine():
    tree_example = """pages/
├── layout.psx          → wraps every page
├── index.py            → /
├── about.py            → /about
├── blog/
│   ├── index.py        → /blog
│   ├── layout.psx      → wraps /blog/*
│   └── [slug].py       → /blog/:slug
├── users/
│   └── [...slug].py    → /users/* (catch-all)
└── api/
    └── posts.py        → /api/posts (JSON endpoint)"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-12 w-full max-w-6xl mx-auto">
                <DocsScrollSpy />

            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-16 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-6">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Core Concepts</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Routing Engine</span>
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
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">Routing Engine</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        NextPy's router has two halves: a server-side scanner that turns the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code> directory into a route table, and a client-side router that swaps pages without reloads.
                    </p>
                </header>

                <div id="route-table" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Building the route table</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        At startup the server walks <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code> recursively. Every <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.py</code>/<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.psx</code> file becomes a route; <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">index.py</code> maps to its folder's path; brackets declare dynamic segments:
                    </p>
                    <EnhancedCodeBlock lang="text" filename="pages/ tree" snippet={tree_example} />
                </div>

                <div id="matching" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Matching &amp; layouts</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Static segments beat dynamic ones; dynamic beats catch-all. For a matched route the server walks <em>up</em> the directory tree collecting <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">layout.psx</code> files into a chain — root layout outermost, page innermost. Layouts are cached by file mtime, so edits hot-reload without a restart.
                    </p>
                </div>

                <div id="client-router" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The client router</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        The server injects a small router runtime into every page. Internal links are auto-marked with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">data-nextpy-link</code>; clicks are intercepted, the target HTML is fetched and swapped into the layout chain, and the URL updates via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">history.pushState</code>. Layouts above the changed segment are preserved — their state and event listeners survive navigation.
                    </p>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">window.navigateTo(path)</code> / <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">window.__nextpyRouter.navigate(path)</code> — programmatic navigation.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy:navigate</code> DOM event — fires after every client-side navigation.</li>
                        <li>Back/forward restores scroll position from the history entry.</li>
                    </ul>
                </div>

                <div id="dynamic-segments" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Dynamic segments</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">[param].py</code> captures one segment, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">[...slug].py</code> captures the rest. Values arrive in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">context["params"]</code> inside data-fetching functions and as props/handler params elsewhere.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/concepts/psx-internals" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                PSX Core Internals
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/concepts/rendering" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Rendering
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
                        <li><a href="#route-table" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Building the route table</a></li>
                        <li><a href="#matching" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Matching &amp; layouts</a></li>
                        <li><a href="#client-router" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The client router</a></li>
                        <li><a href="#dynamic-segments" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Dynamic segments</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )





def getServerSideProps(context):
    return {"props": {"title": "Routing Engine - NextPy Docs"}}


default = RoutingEngine

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
