"""Events API - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def EventsAPI():
    click_example = """from nextpy.psx import component, useState

@component
def Counter():
    [count, set_count] = useState(0)

    def increment():
        set_count(count + 1)

    return (
        &lt;button onclick={increment}&gt;
            Count: {count}
        &lt;/button&gt;
    )"""

    input_example = """from nextpy.psx import component, useState

@component
def Search():
    [query, set_query] = useState("")

    return (
        &lt;input
            value={query}
            oninput={lambda e: set_query(e.target.value)}
            placeholder="Search..."
        /&gt;
    )"""

    submit_example = """from nextpy.psx import component, useState, callServerAction

@component
def LoginForm():
    [email, set_email] = useState("")
    [password, set_password] = useState("")

    def handle_submit(e):
        e.preventDefault()
        callServerAction("login", {"email": email, "password": password})

    return (
        &lt;form onsubmit={handle_submit}&gt;
            &lt;input value={email} oninput={lambda e: set_email(e.target.value)} /&gt;
            &lt;input type="password" value={password} oninput={lambda e: set_password(e.target.value)} /&gt;
            &lt;button type="submit"&gt;Sign in&lt;/button&gt;
        &lt;/form&gt;
    )"""

    loading_example = """&lt;button type="submit" disabled={_server_loading}&gt;
    {"Signing in..." if _server_loading else "Sign in"}
&lt;/button&gt;"""

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
                        <span class="text-white">Events API</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">Events API</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Attach Python handlers to DOM events with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">on*</code> attributes. Handlers run client-side, update state reactively, and can call server actions.
                    </p>
                </header>

                <div id="basics" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Basics</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Any attribute starting with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">on</code> is compiled into a delegated event listener. The handler receives the DOM event as its argument:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/counter.py" snippet={click_example} />
                </div>

                <div id="forms" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Forms & inputs</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Controlled inputs bind <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">value</code> to state and update it via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">oninput</code>. Submit handlers should call <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">e.preventDefault()</code> to avoid a full page reload:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/login.py" snippet={submit_example} />
                    <EnhancedCodeBlock lang="python" filename="pages/search.py" snippet={input_example} />
                </div>

                <div id="supported" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Supported events</h2>
                    <p class="text-base leading-7 text-zinc-400">Common DOM events map directly to attributes:</p>
                    <div class="overflow-hidden rounded-xl border border-zinc-800/80 mt-4">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-400">
                                <tr><th class="text-left px-4 py-2.5 font-medium">Attribute</th><th class="text-left px-4 py-2.5 font-medium">DOM event</th></tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">onclick</td><td class="px-4 py-2.5 font-mono text-xs">click</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">oninput</td><td class="px-4 py-2.5 font-mono text-xs">input</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">onchange</td><td class="px-4 py-2.5 font-mono text-xs">change</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">onsubmit</td><td class="px-4 py-2.5 font-mono text-xs">submit</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">onkeydown / onkeyup / onkeypress</td><td class="px-4 py-2.5 font-mono text-xs">keyboard events</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">onfocus / onblur</td><td class="px-4 py-2.5 font-mono text-xs">focus events</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">onmouseover / onmouseout</td><td class="px-4 py-2.5 font-mono text-xs">mouse hover</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="server-actions" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Calling server actions</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">callServerAction(name, payload)</code> inside a handler to invoke a server-side function. The result lands in the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_result</code> state key, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_loading</code> toggles while the request is in flight &mdash; bind it to disable submit buttons:
                    </p>
                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/login.py"
                        snippet={loading_example}
                    />
                </div>

                <div id="best-practices" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Best practices</h2>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li>Keep handlers small &mdash; they compile to client-side JavaScript.</li>
                        <li>Use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useEffect</code> for subscriptions (scroll, timers, sockets) instead of inline listeners.</li>
                        <li>Prefer state-driven UI via data-state bindings and ternary expressions over manual DOM writes.</li>
                    </ul>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/router" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Router API
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/utils" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Utilities
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
                        <li><a href="#basics" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Basics</a></li>
                        <li><a href="#forms" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Forms & inputs</a></li>
                        <li><a href="#supported" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Supported events</a></li>
                        <li><a href="#server-actions" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server actions</a></li>
                        <li><a href="#best-practices" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Best practices</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )





def getServerSideProps(context):
    return {"props": {"title": "Events API - NextPy Docs"}}


default = EventsAPI

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
