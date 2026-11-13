"""Linking and Navigation - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def LinkingGuide():
    basic_example = """from nextpy.psx import component, Link

@component
def Navigation():
    return (
        &lt;nav class="flex gap-4"&gt;
            &lt;Link href="/"&gt;Home&lt;/Link&gt;
            &lt;Link href="/about"&gt;About&lt;/Link&gt;
            &lt;Link href="/contact"&gt;Contact&lt;/Link&gt;
        &lt;/nav&gt;
    )"""

    dynamic_example = """from nextpy.psx import component, Link

@component
def UserList(props):
    users = props.get("users", [])
    return (
        &lt;div class="space-y-2"&gt;
            {for user in users:
                &lt;Link href={"/users/" + str(user["id"])} class="block p-2 hover:bg-zinc-800 rounded"&gt;
                    {user["name"]}
                &lt;/Link&gt;
            }
        &lt;/div&gt;
    )"""

    programmatic_example = """from nextpy.psx import interactive_component, useState, useEffect, callServerAction

@interactive_component
def LoginForm():
    [email, setEmail] = useState("")
    [password, setPassword] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def submit(e):
        e.preventDefault()
        callServerAction("login", {"email": email, "password": password})

    def handle_result():
        if _server_result and _server_result.get("success"):
            window.navigateTo("/dashboard")

    useEffect(handle_result, [_server_result])

    return (
        &lt;form onsubmit={submit}&gt;
            &lt;input value={email} oninput={lambda e: setEmail(e.target.value)} /&gt;
            &lt;input type="password" value={password} oninput={lambda e: setPassword(e.target.value)} /&gt;
            &lt;button type="submit" disabled={_server_loading}&gt;Login&lt;/button&gt;
        &lt;/form&gt;
    )"""

    active_example = """from nextpy.psx import interactive_component, useState, useEffect

@interactive_component
def Navigation():
    [path, setPath] = useState(window.location.pathname)

    def setup():
        def on_nav():
            setPath(window.location.pathname)
        document.addEventListener("nextpy:navigate", on_nav)
        return lambda: document.removeEventListener("nextpy:navigate", on_nav)

    useEffect(setup, [])

    def link_class(href):
        base = "px-3 py-2 rounded transition-colors"
        if path == href or path.startswith(href + "/"):
            return base + " bg-blue-600 text-white"
        return base + " text-zinc-400 hover:text-white"

    return (
        &lt;nav class="flex gap-2"&gt;
            &lt;Link href="/" class={link_class("/")}&gt;Home&lt;/Link&gt;
            &lt;Link href="/docs" class={link_class("/docs")}&gt;Docs&lt;/Link&gt;
        &lt;/nav&gt;
    )"""

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
                        <span class="text-white">Linking and Navigation</span>
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
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">
                        Linking and Navigation
                    </h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        NextPy uses file-system routing: every file under <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code> becomes a URL. This page covers the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Link</code> component, dynamic hrefs, programmatic navigation, and active-link states.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Clicking a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Link</code> does not reload the page. The client router prefetches the target, swaps the content inside your layouts, updates the URL with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">history.pushState</code>, and restores scroll position on back/forward navigation.
                    </p>
                </div>

                <div id="link-component" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The Link Component</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Import <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Link</code> from <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.psx</code>. It renders a real anchor tag — SEO-friendly and middle-clickable — while intercepting internal navigations for SPA transitions. External URLs and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">target="_blank"</code> links fall through to normal browser behavior.
                    </p>

                    <div class="p-8 rounded-xl border border-zinc-800/60 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 mt-6">
                        <div class="w-56 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                            <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                            <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>about.py</div>
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>contact.py</div>
                            </div>
                        </div>
                        <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                        <div class="space-y-2 shrink-0">
                            <div class="bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-blue-400">/</div>
                            <div class="bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-blue-400">/about</div>
                            <div class="bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-blue-400">/contact</div>
                        </div>
                    </div>

                    <EnhancedCodeBlock lang="python" filename="components/navbar.py" snippet={basic_example} />
                </div>

                <div id="dynamic-links" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Dynamic Links</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Build hrefs from data with f-strings or concatenation inside a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">{'{for ...}'}</code> loop. Dynamic segments like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/users/[id].py</code> receive their values through the same URL shape:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/users.py" snippet={dynamic_example} />
                </div>

                <div id="programmatic-navigation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Programmatic Navigation</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        After a server action succeeds — login, form submit, delete — navigate with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">window.navigateTo(path)</code>. The alias <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">window.__nextpyRouter.navigate(path)</code> does the same. Both go through the client router: history entry, scroll reset, and layout-preserving page swap.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/login.py" snippet={programmatic_example} />
                </div>

                <div id="active-links" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Active Link States</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Read the current path from <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">window.location.pathname</code> and listen for the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy:navigate</code> DOM event to re-evaluate after every client-side navigation:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/navbar.py" snippet={active_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/getting-started/layouts-pages" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Layouts and Pages
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/fetching-data" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Fetching Data
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
                        <li><a href="#link-component" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Link Component</a></li>
                        <li><a href="#dynamic-links" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Dynamic Links</a></li>
                        <li><a href="#programmatic-navigation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Programmatic Navigation</a></li>
                        <li><a href="#active-links" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Active Link States</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )





def getServerSideProps(context):
    return {"props": {"title": "Linking and Navigation - NextPy Docs"}}


default = LinkingGuide

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
