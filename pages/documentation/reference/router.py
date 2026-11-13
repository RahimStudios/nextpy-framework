"""Router API - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def RouterAPI():
    link_example = """from nextpy.psx import component, Link

@component
def Page():
    return (
        &lt;Link href="/about"&gt;About&lt;/Link&gt;
    )"""

    router_example = """from nextpy.psx import component, Link

@component
def Page():
    def go_home():
        # Client-side navigation without a full reload
        window.navigateTo("/")

    return (
        &lt;button onclick={go_home}&gt;Go home&lt;/button&gt;
    )"""

    params_example = """from nextpy.psx import component




def getServerSideProps(context):
    # context.params holds dynamic route segments
    # context.query holds query-string parameters
    # context.request holds the raw request object
    return {
        "props": {
            "id": context.params.get("id"),
            "search": context.query.get("search", ""),
        }
    }"""

    redirect_example = """def getServerSideProps(context):
    user = get_current_user(context)
    if not user:
        return {"redirect": {"destination": "/login", "permanent": False}}
    return {"props": {"user": user}}"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-12 w-full max-w-6xl mx-auto">
                <DocsScrollSpy />

            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-16 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-6">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Reference API</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Router API</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">Router API</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Reference for NextPy routing: the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Link</code> component, programmatic navigation, dynamic segments, and the request context.
                    </p>
                </header>

                <div id="link" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Link</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Link</code> renders an anchor tag with client-side navigation, prefetching, and layout preservation. External URLs automatically fall back to full page loads.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={link_example} />
                    <table class="w-full text-sm mt-4">
                        <thead class="text-zinc-500 border-b border-zinc-800">
                            <tr><th class="text-left py-2 font-medium">Prop</th><th class="text-left py-2 font-medium">Type</th><th class="text-left py-2 font-medium">Default</th><th class="text-left py-2 font-medium">Description</th></tr>
                        </thead>
                        <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                            <tr><td class="py-2 font-mono text-xs text-blue-400">href</td><td class="py-2 font-mono text-xs">string</td><td class="py-2 font-mono text-xs">-</td><td class="py-2">Destination path or URL.</td></tr>
                            <tr><td class="py-2 font-mono text-xs text-blue-400">prefetch</td><td class="py-2 font-mono text-xs">boolean</td><td class="py-2 font-mono text-xs">true</td><td class="py-2">Prefetch the route on hover/viewport.</td></tr>
                            <tr><td class="py-2 font-mono text-xs text-blue-400">replace</td><td class="py-2 font-mono text-xs">boolean</td><td class="py-2 font-mono text-xs">false</td><td class="py-2">Replace history entry instead of pushing.</td></tr>
                            <tr><td class="py-2 font-mono text-xs text-blue-400">scroll</td><td class="py-2 font-mono text-xs">boolean</td><td class="py-2 font-mono text-xs">true</td><td class="py-2">Scroll to top after navigation.</td></tr>
                            <tr><td class="py-2 font-mono text-xs text-blue-400">target</td><td class="py-2 font-mono text-xs">string</td><td class="py-2 font-mono text-xs">-</td><td class="py-2">Set <code class="font-mono text-xs">_blank</code> for new tab.</td></tr>
                        </tbody>
                    </table>
                </div>

                <div id="programmatic" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Programmatic navigation</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Call <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">window.navigateTo(url)</code> inside a handler for client-side navigation that preserves the layout. Pass <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">true</code> as the second argument to replace the history entry, or use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">window.__nextpyRouter.navigate(url, replace, scroll)</code> for finer control:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/dashboard.py" snippet={router_example} />
                </div>

                <div id="dynamic-segments" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Dynamic segments & context</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        File names like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/blog/[slug].py</code> create dynamic routes. Read params and query strings in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code>:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/blog/[slug].py" snippet={params_example} />
                </div>

                <div id="redirects" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Redirects</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Return a redirect from <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code> to send users elsewhere &mdash; useful for auth guards and moved pages:
                    </p>
                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/dashboard.py"
                        snippet={redirect_example}
                    />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/hooks" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Hooks API
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/events" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Events API
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
                        <li><a href="#link" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Link</a></li>
                        <li><a href="#programmatic" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Programmatic navigation</a></li>
                        <li><a href="#dynamic-segments" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Dynamic segments & context</a></li>
                        <li><a href="#redirects" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Redirects</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Router API - NextPy Docs"}}


default = RouterAPI

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
