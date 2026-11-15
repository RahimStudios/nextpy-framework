"""Styling — NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def StylingGuide():
    tailwind_example = """from nextpy.psx import component

@component
def Card():
    return (
        <div class="max-w-sm rounded-xl border border-zinc-800 bg-zinc-900 p-6 shadow-lg hover:shadow-xl transition-shadow">
            <h3 class="text-lg font-semibold text-white">Card title</h3>
            <p class="mt-2 text-sm text-zinc-400">Styled entirely with utility classes.</p>
            <button class="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500">
                Action
            </button>
        </div>
    )"""

    state_example = """from nextpy.psx import interactive_component, useState

@interactive_component
def Toggle():
    [on, setOn] = useState(False)

    def cls(active, inactive):
        return active if on else inactive

    return (
        <button
            onclick={lambda e: setOn(not on)}
            class={cls(
                "bg-emerald-600 text-white",
                "bg-zinc-800 text-zinc-400"
            )}
        >
            {"ON" if on else "OFF"}
        </button>
    )"""

    css_example = """# assets/styles/custom.css
.card-glow {
    box-shadow: 0 0 24px rgba(59, 130, 246, 0.25);
    transition: box-shadow 0.3s ease;
}
.card-glow:hover {
    box-shadow: 0 0 32px rgba(59, 130, 246, 0.45);
}"""

    layout_example = """from nextpy.psx import component, psx

@component
def RootLayout(children):
    return psx(\"\"\"
        <html>
            <head>
                <link rel=\"stylesheet\" href=\"/static/css/custom.css\" />
            </head>
            <body>{children}</body>
        </html>
    \"\"\")"""

    psx_style_example = """from nextpy.psx import component, psx

@component
def Page():
    cls = "bg-blue-600 text-white"
    return psx(f\"\"\"
        <button class="{cls} px-4 py-2 rounded-lg">Click</button>
    \"\"\")"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Getting Started</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Styling</span>
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
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Styling</h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy ships with Tailwind CSS out of the box. Write utility classes directly in your markup — the JIT compiler scans your pages, components, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> strings and generates only the CSS you use.
                    </p>
                </header>

                <div id="utility-classes" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Utility classes</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Every element accepts a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">class</code> attribute. Combine layout, spacing, color, and state utilities — responsive prefixes like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">sm:</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">md:</code>, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">dark:</code> work as usual:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/card.py" snippet={tailwind_example} />
                </div>

                <div id="conditional-styles" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Conditional styles</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">class</code> accepts expressions, so state-driven styling is just a Python ternary or helper function. When state changes, only the class attribute updates — no re-render of the whole page:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/toggle.py" snippet={state_example} />
                </div>

                <div id="custom-css" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Custom CSS</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        For styles Tailwind can't express, drop a stylesheet in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">assets/styles/</code> and link it from your root layout. Custom classes compose with utilities — use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">!important</code> sparingly:
                    </p>
                    <EnhancedCodeBlock lang="css" filename="assets/styles/custom.css" snippet={css_example} />
                    <EnhancedCodeBlock lang="python" filename="pages/layout.psx" snippet={layout_example} />
                </div>

                <div id="psx-strings" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Styling inside psx() strings</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The Tailwind scanner also reads class attributes inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> template strings, so dynamically built markup gets its utilities generated too. Dynamic class fragments are safe — the scanner matches complete utility tokens:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={psx_style_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/getting-started/error-handling" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Error Handling
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/route-handlers" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Route Handlers
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                            </span>
                        </Link>
                    </div>
                </footer>
            </article>

            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-4 pl-8 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
                <div class="text-sm">
                    <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                    <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#utility-classes" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Utility classes</a></li>
                        <li><a href="#conditional-styles" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Conditional styles</a></li>
                        <li><a href="#custom-css" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Custom CSS</a></li>
                        <li><a href="#psx-strings" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">psx() strings</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Styling - NextPy Docs"}}


default = StylingGuide

