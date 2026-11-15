"""Your First App - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def FirstApp():
    setup_example = """# Create a new NextPy app
nextpy create my-first-app
cd my-first-app

# Start the development server
nextpy dev"""

    page_example = """# pages/index.py — file-based routing: this file IS "/"
from nextpy.psx import component, Link

@component
def Home():
    return (
        <div class="p-8">
            <h1 class="text-3xl font-bold">Hello NextPy</h1>
            <p>Server-rendered on every request.</p>
            <Link href="/about">About</Link>
        </div>
    )

default = Home"""

    island_example = """# components/counter.py — hydrates independently
from nextpy.psx import interactive_component, useState

@interactive_component
def Counter():
    [count, set_count] = useState(0)

    def Increment():
        set_count(count + 1)

    return (
        <button onclick={Increment} class="px-4 py-2 bg-blue-600 text-white rounded">
            Clicked {count} times
        </button>
    )"""

    layout_example = """# pages/about.py — inherits the root layout automatically
from nextpy.psx import component, Link

@component
def About():
    return (
        <div class="p-8">
            <h1>About</h1>
            <Link href="/">Back home</Link>
        </div>
    )

default = About"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Tutorials</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Your First App</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Your First App
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        Learn how to build your first NextPy application from scratch.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        In this tutorial, you'll create a simple NextPy application with routing and interactivity.
                    </p>
                </div>

                <div id="setup" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Setup</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Scaffold the project and start the dev server — hot reload picks up every file change:
                    </p>
                    <EnhancedCodeBlock
                        lang="bash"
                        filename="terminal"
                        snippet={setup_example}
                    />
                </div>

                <div id="first-page" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Your first page</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Files under <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code> become routes — <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/index.py</code> serves <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/</code>. Write JSX directly in the component; the framework compiles it:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={page_example} />
                </div>

                <div id="navigation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Navigation</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Link</code> component with an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">href</code> prop navigates client-side — the router fetches the new page and swaps the content without a full reload:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/about.py" snippet={layout_example} />
                </div>

                <div id="interactivity" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Adding interactivity</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Mark a component <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@interactive_component</code> and it hydrates in the browser — state updates re-render only that island:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/counter.py" snippet={island_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/performance" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Performance
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/tutorials/ai-chat" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                AI Chat App
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
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Overview</a></li>
                        <li><a href="#setup" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Setup</a></li>
                        <li><a href="#first-page" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Your First Page</a></li>
                        <li><a href="#navigation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Navigation</a></li>
                        <li><a href="#interactivity" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Interactivity</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Your First App - NextPy Docs"}}

default = FirstApp

