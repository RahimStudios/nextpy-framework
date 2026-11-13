"""Components API - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def ComponentsAPI():
    builtins_example = """from nextpy.psx import (
    component, Link, Head, Meta, Title, Script, Image,
    Motion, AnimatePresence, Form, Input, Button, Card,
)

@component
def Example():
    return (
        &lt;div&gt;
            &lt;Head&gt;
                &lt;Title&gt;My Page&lt;/Title&gt;
                &lt;Meta name="description" content="..." /&gt;
            &lt;/Head&gt;
            &lt;Link href="/about"&gt;About&lt;/Link&gt;
            &lt;Motion initial={{"opacity": 0}} animate={{"opacity": 1}}&gt;
                &lt;Card&gt;Hello&lt;/Card&gt;
            &lt;/Motion&gt;
        &lt;/div&gt;
    )"""

    custom_example = """from nextpy.psx import component, register_component, Props

@component
def Badge(props):
    return &lt;span class="badge"&gt;{props.get("label", "")} &lt;/span&gt;

register_component("Badge", Badge)"""

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
                        <span class="text-white">Components API</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">Components API</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Reference for NextPy built-in components, custom components, and the hooks they expose.
                    </p>
                </header>

                <div id="builtins" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Built-in components</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Import everything from <code class="font-mono text-xs">nextpy.psx</code>. All HTML elements are available as tags; these are the framework-provided components:
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Component</th>
                                    <th class="text-left px-4 py-3 font-semibold">Purpose</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Link</td><td class="px-4 py-3">Client-side navigation with prefetching and SPA routing.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Head / Title / Meta</td><td class="px-4 py-3">Per-page metadata injected into the document head.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Script / Image</td><td class="px-4 py-3">Script tags and optimized image rendering.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Motion / AnimatePresence</td><td class="px-4 py-3">Declarative animations and exit transitions.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Form / Input / Button</td><td class="px-4 py-3">Form primitives wired to the event system.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Card / Navbar / NavItem</td><td class="px-4 py-3">Layout and navigation helpers.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Conditional / Loop / ErrorBoundary / Suspense</td><td class="px-4 py-3">Control-flow and resilience primitives.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/example.py" snippet={builtins_example} />
                </div>

                <div id="custom-components" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Custom components</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Define components with <code class="font-mono text-xs">@component</code>, receive props as a dict, and register them for use in JSX:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/badge.py" snippet={custom_example} />
                </div>

                <div id="hooks" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Hooks</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        React-style hooks are exported from <code class="font-mono text-xs">nextpy.psx</code>:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-400">
                        <li><strong class="text-zinc-200">Core:</strong> <code class="font-mono text-xs">useState</code>, <code class="font-mono text-xs">useEffect</code>, <code class="font-mono text-xs">useRef</code>, <code class="font-mono text-xs">useMemo</code>, <code class="font-mono text-xs">useCallback</code>, <code class="font-mono text-xs">useReducer</code>, <code class="font-mono text-xs">useContext</code></li>
                        <li><strong class="text-zinc-200">Custom:</strong> <code class="font-mono text-xs">useCounter</code>, <code class="font-mono text-xs">useToggle</code>, <code class="font-mono text-xs">useLocalStorage</code>, <code class="font-mono text-xs">useFetch</code>, <code class="font-mono text-xs">useAction</code>, <code class="font-mono text-xs">useDebounce</code>, <code class="font-mono text-xs">useInterval</code>, <code class="font-mono text-xs">usePrevious</code>, <code class="font-mono text-xs">useAsync</code>, <code class="font-mono text-xs">useMediaQuery</code>, <code class="font-mono text-xs">useGeolocation</code>, <code class="font-mono text-xs">usePerformance</code></li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-400">
                        See the <Link href="/documentation/reference/hooks" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">Hooks API</Link> page for details.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/config" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Configuration
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/hooks" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Hooks API
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
                        <li><a href="#builtins" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Built-in components</a></li>
                        <li><a href="#custom-components" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Custom components</a></li>
                        <li><a href="#hooks" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Hooks</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )





def getServerSideProps(context):
    return {"props": {"title": "Components API - NextPy Docs"}}


default = ComponentsAPI

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
