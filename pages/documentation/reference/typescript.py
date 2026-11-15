"""TypeScript Integration - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, useState
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def TypeScriptAPI():
    config_example = """from nextpy.psx import Config

config = Config(
    app_name="my-app",
    tailwind=True,
    typescript=True,   # emit tsconfig.json + typed client runtime
)"""

    typed_example = """from nextpy.psx import component, useState
from typing import Optional

@component
def Profile(props):
    [name, set_name] = useState("")
    user: Optional[dict] = props.get("user")

    return (
        <h1>{user["name"] if user else "Guest"}</h1>
    )"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Reference API</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">TypeScript</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">TypeScript Integration</h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy is Python-first, but ships TypeScript definitions for the client runtime so editors and tooling can type-check hydrated components, events, and the router.
                    </p>
                </header>

                <div id="enable" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Enabling TypeScript</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Set <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">typescript=True</code> in your config to generate a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">tsconfig.json</code> and typed declarations for the browser runtime:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="nextpy.config.py" snippet={config_example} />
                </div>

                <div id="typed-python" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Type hints in Python</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Pages are plain Python, so standard typing works everywhere — annotate props, state, and handler signatures for editor autocomplete and static checks:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/profile.py" snippet={typed_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Run <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">mypy</code> (v1.8+) or <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pyright</code> against your project; NextPy respects the configured rules during builds.
                    </p>
                </div>

                <div id="client-types" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Client runtime types</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The generated declarations cover the globals your handlers can touch — <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">window.navigateTo</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">window.__nextpyRouter</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">callServerAction</code>, state setters, and the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_result</code> / <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_loading</code> keys.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/utils" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Utilities
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <span class="block p-5 rounded-xl border border-zinc-800/30 bg-zinc-950/20 opacity-50 select-none">
                            <span class="block text-xs font-medium text-zinc-600 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-zinc-600 flex items-center justify-end gap-1">
                                —
                            </span>
                        </span>
                    </div>
                </footer>
            </article>

            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-4 pl-8 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
                <div class="text-sm">
                    <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                    <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#enable" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Enabling TypeScript</a></li>
                        <li><a href="#typed-python" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Type hints in Python</a></li>
                        <li><a href="#client-types" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Client runtime types</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "TypeScript - NextPy Docs"}}


default = TypeScriptAPI

