"""PSX Core Internals — NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def PsxInternals():
    pipeline_example = """# pages/index.py — what you write
@component
def Page():
    return psx(\"\"\"
        &lt;div class=\"p-4\"&gt;
            &lt;h1&gt;Hello&lt;/h1&gt;
        &lt;/div&gt;
    \"\"\")"""

    island_example = """from nextpy.psx import interactive_component, useState, useEffect

# SSR renders the initial HTML; the browser then hydrates this island
@interactive_component(hydrate="visible")
def Chart():
    [data, setData] = useState(None)

    def setup():
        async def load():
            res = await fetch("/api/chart")
            setData(await res.json())
        load()
        return None

    useEffect(setup, [])

    if not data:
        return &lt;div&gt;Loading chart…&lt;/div&gt;
    return &lt;canvas id="chart" width="400" height="200"&gt;&lt;/canvas&gt;"""

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
                        <span class="text-white">PSX Core Internals</span>
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
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">PSX Core Internals</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        PSX (Python JSX) is the layer that turns your Python components into fast HTML on the server and reactive islands in the browser. This page explains what happens between <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> and the pixels.
                    </p>
                </header>

                <div id="what-is-psx" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">What PSX is</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        PSX has two halves. On the server, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> evaluates Python f-string expressions inside an HTML template and returns a string — your markup is built with full Python power. In the browser, the hydration engine scans the rendered HTML for interactive components, replays their state into a signal graph, and binds events — no virtual DOM diffing of the whole page.
                    </p>
                </div>

                <div id="server-side" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Server-side rendering</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        A plain <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@component</code> runs entirely on the server. Expressions inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> — conditionals, comprehensions, function calls — evaluate in Python before any bytes reach the client:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={pipeline_example} />
                </div>

                <div id="hydration" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Hydration islands</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        An <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@interactive_component</code> still renders on the server — the client receives real HTML, not a blank div. The runtime then attaches behavior to that DOM in place. The <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">hydrate</code> strategy controls when:
                    </p>
                    <div class="overflow-hidden rounded-xl border border-zinc-800/80 mt-4">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-400">
                                <tr><th class="text-left px-4 py-2.5 font-medium">Strategy</th><th class="text-left px-4 py-2.5 font-medium">When it hydrates</th></tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">eager</td><td class="px-4 py-2.5">Immediately on page load (default)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">visible</td><td class="px-4 py-2.5">When scrolled into the viewport</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">interaction</td><td class="px-4 py-2.5">On first click, scroll, or keypress</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">idle</td><td class="px-4 py-2.5">When the main thread is idle</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/chart.py" snippet={island_example} />
                </div>

                <div id="state-bridge" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The state bridge</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Initial state is serialized into the page as <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">__PSX_DATA__</code> JSON. On hydration, each <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useState</code> becomes a signal; expressions that depend on state are re-evaluated through a pub-sub graph and batched with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">requestAnimationFrame</code> — scroll and mouse handlers never trigger layout thrash.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/concepts/why-nextpy" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Why NextPy?
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/concepts/routing-engine" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Routing Engine
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
                        <li><a href="#what-is-psx" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What PSX is</a></li>
                        <li><a href="#server-side" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server-side rendering</a></li>
                        <li><a href="#hydration" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Hydration islands</a></li>
                        <li><a href="#state-bridge" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The state bridge</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )





def getServerSideProps(context):
    return {"props": {"title": "PSX Core Internals - NextPy Docs"}}


default = PsxInternals

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
