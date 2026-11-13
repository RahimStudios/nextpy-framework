"""Production Building - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def BuildingGuide():
    cli_example = '''# Development — hot reload, debug tools, unminified assets
nextpy dev --port 5000

# Production build — optimized, minified, tree-shaken, code-split
nextpy build --out out

# Serve the production build
nextpy start --port 5000

# Fully static export for CDN/host-agnostic deploys
nextpy export --out out'''

    options_example = '''nextpy build --help

Options:
  -o, --out PATH        Output directory (default: out)
  --clean / --no-clean  Clean the output dir first (default: on)
  --optimize            Build optimization (default: on)
  --minify              Minify JS/CSS assets (default: on)
  --tree-shake          Drop unused code (default: on)
  --code-split          Split bundles per route (default: on)'''

    env_example = '''# .env — production settings are read from the environment
DEBUG=false
DEVELOPMENT=false
SECRET_KEY=generate-a-long-random-string
DATABASE_URL=postgresql://user:pass@host/db
FRONTEND_URL=https://your-domain.com'''

    misc_example = '''# Inspect what the router registered
nextpy routes

# Scaffold a new page, API handler, or component
nextpy generate page pricing
nextpy generate api health
nextpy generate component StatCard

# Create an admin user for protected areas
nextpy createsuperuser

# Wipe the dev database
nextpy flushdb'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-12 w-full max-w-6xl mx-auto">
                <DocsScrollSpy />

            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-16 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-6">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Production Building</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">
                        Production Building
                    </h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Learn how to build and optimize your NextPy application for production.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-400">
        The NextPy CLI covers the whole lifecycle: <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy dev</code> for development with hot reload, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy build</code> for an optimized production bundle, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy start</code> to serve it, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy export</code> for fully static output.
                    </p>
                </div>

                <div id="commands" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The four commands</h2>
                    <EnhancedCodeBlock lang="bash" filename="terminal" snippet={cli_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-400">
                        <li><strong>dev</strong> — reload and debug on by default; pass <code class="font-mono text-xs">--no-reload</code> or <code class="font-mono text-xs">--no-debug</code> to disable.</li>
                        <li><strong>build</strong> — writes optimized assets to <code class="font-mono text-xs">out/</code>; every optimization can be toggled.</li>
                        <li><strong>start</strong> — production server; reload and debug are off.</li>
                        <li><strong>export</strong> — emits static files you can host anywhere.</li>
                    </ul>
                </div>

                <div id="build-options" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Build options</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Tune the optimizer per deploy — e.g. disable code splitting for a single-file bundle:
                    </p>
                    <EnhancedCodeBlock lang="bash" filename="terminal" snippet={options_example} />
                </div>

                <div id="environment" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Production environment</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Settings resolve from environment variables — set them in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.env</code> locally and in your host's secret store in production:
                    </p>
                    <EnhancedCodeBlock lang="bash" filename=".env" snippet={env_example} />
                </div>

                <div id="other-commands" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Other useful commands</h2>
                    <EnhancedCodeBlock lang="bash" filename="terminal" snippet={misc_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/full-stack" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Full Stack Paradigms
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/public-pages" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Public & Static Pages
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
                        <li><a href="#commands" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The four commands</a></li>
                        <li><a href="#build-options" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Build options</a></li>
                        <li><a href="#environment" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Environment</a></li>
                        <li><a href="#other-commands" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Other commands</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )




def getServerSideProps(context):
    return {"props": {"title": "Production Building - NextPy Docs"}}

default = BuildingGuide

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
