"""API Reference hub - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect


@component
def ApiReferenceHub():
    refs = [
        ("/documentation/reference/cli", "CLI Engine Commands", "nextpy dev, build, start, create, and friends.", "M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"),
        ("/documentation/reference/config", "Configuration", "nextpy.config options: app name, port, tailwind, debug.", "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"),
        ("/documentation/reference/components", "Built-in Elements", "psx, Link, Motion, AnimatePresence, and core tags.", "M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"),
        ("/documentation/reference/hooks", "State & Hooks", "useState, useEffect, useFetch, and custom hooks.", "M13 10V3L4 14h7v7l9-11h-7z"),
        ("/documentation/reference/router", "Router API", "Link props, navigateTo, dynamic segments, redirects.", "M13 7l5 5m0 0l-5 5m5-5H6"),
        ("/documentation/reference/events", "Event System", "on* attributes, handlers, server actions, loading state.", "M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"),
        ("/documentation/reference/data-fetching", "Data Fetching", "getServerSideProps, getStaticProps, and client fetch.", "M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"),
        ("/documentation/reference/metadata", "Metadata & SEO", "Page titles, meta tags, sitemap, robots.", "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"),
        ("/documentation/reference/performance", "Performance", "SSR/SSG/ISR, caching, and bundle notes.", "M13 10V3L4 14h7v7l9-11h-7z"),
        ("/documentation/reference/server-actions", "Server Actions", "callServerAction, _server_result, _server_loading.", "M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"),
        ("/documentation/reference/utils", "Utilities", "nextpy.db, cache, server_actions, security helpers.", "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"),
        ("/documentation/reference/typescript", "TypeScript", "tsconfig generation and typed client runtime.", "M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"),
    ]

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-12 w-full max-w-6xl mx-auto">
                <DocsScrollSpy />

            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-16 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-6">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">API Reference</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">API Reference</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Complete reference for every NextPy API surface &mdash; CLI, config, components, hooks, routing, events, data, and utilities.
                    </p>
                </header>

                <div id="all-reference" class="grid grid-cols-1 md:grid-cols-2 gap-5">
                    {for ref in refs:
                        <Link href={ref[0]} className="group block p-6 rounded-xl border border-zinc-800/60 bg-zinc-950/40 hover:bg-zinc-900/60 hover:border-zinc-700 transition-all">
                            <div class="flex items-start gap-4">
                                <div class="flex items-center justify-center w-10 h-10 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400 shrink-0">
                                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d={ref[3]}/></svg>
                                </div>
                                <div>
                                    <h3 class="text-base font-semibold text-white group-hover:text-purple-400 transition-colors">{ref[1]}</h3>
                                    <p class="mt-1.5 text-sm leading-relaxed text-zinc-500 group-hover:text-zinc-400 transition-colors">{ref[2]}</p>
                                </div>
                            </div>
                        </Link>
                    }
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/guides" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Guides
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <span class="block p-5 rounded-xl border border-zinc-800/30 bg-zinc-950/20 opacity-50 select-none">
                            <span class="block text-xs font-medium text-zinc-600 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-zinc-600 flex items-center justify-end gap-1">&mdash;</span>
                        </span>
                    </div>
                </footer>
            </article>

            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-6 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
                <div class="text-sm">
                    <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                    <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#all-reference" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">All reference</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )





def getServerSideProps(context):
    return {"props": {"title": "API Reference - NextPy Docs"}}


default = ApiReferenceHub

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
