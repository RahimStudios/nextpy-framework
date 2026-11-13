"""Hooks API - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def HooksAPI():
    usestate_example = """from nextpy.psx import component, useState

@component
def Counter():
    [count, set_count] = useState(0)

    def increment():
        set_count(count + 1)

    return (
        &lt;div&gt;
            &lt;p&gt;Count: {count}&lt;/p&gt;
            &lt;button onclick={increment}&gt;+1&lt;/button&gt;
        &lt;/div&gt;
    )"""

    useeffect_example = """from nextpy.psx import component, useState, useEffect

@component
def ScrollSpy():
    [progress, set_progress] = useState(0)

    def setup():
        def on_scroll():
            doc_height = document.documentElement.scrollHeight - window.innerHeight
            if doc_height &gt; 0:
                set_progress((window.scrollY / doc_height) * 100)

        window.addEventListener("scroll", on_scroll)
        on_scroll()
        return lambda: window.removeEventListener("scroll", on_scroll)

    useEffect(setup, [])

    return &lt;div style={{"width": progress + "%", "height": "4px", "background": "blue"}}&gt;&lt;/div&gt;"""

    server_effect_example = """useEffect(handle_result, [_server_result])"""

    usefetch_example = """from nextpy.psx import component, useFetch

@component
def UserList():
    fetch = useFetch("/api/users")
    data = fetch["data"]

    return (
        &lt;div&gt;
            {fetch["loading"] and &lt;p&gt;Loading...&lt;/p&gt;}
            {fetch["error"] and &lt;p&gt;{fetch["error"]}&lt;/p&gt;}
            &lt;ul&gt;
                {for user in (data or []):
                    &lt;li&gt;{user["name"]}&lt;/li&gt;
                }
            &lt;/ul&gt;
        &lt;/div&gt;
    )"""

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
                        <span class="text-white">Hooks API</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">Hooks API</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Reference for NextPy hooks: <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useState</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useEffect</code>, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useFetch</code>.
                    </p>
                </header>

                <div id="usestate" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">useState</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Declares reactive state. Destructure into a value and a setter &mdash; updates re-render only the bound DOM nodes, not the whole page.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/counter.py" snippet={usestate_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-400">
                        <li>Initial value can be any JSON-serializable Python value.</li>
                        <li>Setters accept a value or an updater function: <code class="font-mono text-xs">set_count(lambda c: c + 1)</code>.</li>
                        <li>Multiple <code class="font-mono text-xs">useState</code> calls per component are fine &mdash; each is tracked independently.</li>
                    </ul>
                </div>

                <div id="useeffect" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">useEffect</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Runs side effects after render. Pass a dependency list to control re-runs; return a cleanup function to unsubscribe.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/clock.py" snippet={useeffect_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-400">
                        <li><code class="font-mono text-xs">useEffect(fn, [])</code> &mdash; run once on mount.</li>
                        <li><code class="font-mono text-xs">useEffect(fn, [dep])</code> &mdash; re-run when <code class="font-mono text-xs">dep</code> changes.</li>
                        <li>Great for timers, scroll listeners, WebSockets, and DOM measurements.</li>
                    </ul>
                </div>

                <div id="usefetch" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">useFetch</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Fetches JSON from an API route on mount and stores the response in component state. Returns a dict with <code class="font-mono text-xs">data</code>, <code class="font-mono text-xs">loading</code>, <code class="font-mono text-xs">error</code>, and a <code class="font-mono text-xs">refetch</code> action.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/users.py" snippet={usefetch_example} />
                </div>

                <div id="server-state" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Server state keys</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Server actions write results into reserved state keys you can bind directly:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-400">
                        <li><code class="font-mono text-xs">_server_result</code> &mdash; the JSON payload returned by the last <code class="font-mono text-xs">callServerAction</code>.</li>
                        <li><code class="font-mono text-xs">_server_loading</code> &mdash; boolean, true while the request is in flight.</li>
                    </ul>
                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/login.py"
                        snippet={server_effect_example}
                    />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/components" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Components API
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/data-fetching" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Data Fetching
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
                        <li><a href="#usestate" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">useState</a></li>
                        <li><a href="#useeffect" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">useEffect</a></li>
                        <li><a href="#usefetch" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">useFetch</a></li>
                        <li><a href="#server-state" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server state keys</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )





def getServerSideProps(context):
    return {"props": {"title": "Hooks API - NextPy Docs"}}


default = HooksAPI

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
