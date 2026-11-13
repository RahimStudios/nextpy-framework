"""Deploying — NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def DeployingGuide():
    env_example = """# .env — loaded automatically at startup
DATABASE_URL=postgresql://user:pass@host:5432/mydb
SECRET_KEY=change-me-in-production
DEBUG=false"""

    prod_example = """# Terminal 1 — build optimized static assets
nextpy build --out dist

# Terminal 2 — start the production server
nextpy start --port 5000 --host 0.0.0.0

# Or serve behind a process manager:
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app"""

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
                        <span class="text-white">Deploying</span>
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
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">Deploying</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        A NextPy app is a standard ASGI server plus static assets &mdash; it runs anywhere Python and a reverse proxy can. This page covers production builds, environment configuration, and platform options.
                    </p>
                </header>

                <div id="production-build" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Production build</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy build</code> bundles and minifies your JS/CSS assets into <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">out/</code> &mdash; or a custom directory via the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">--out</code> flag. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy start</code> then serves the app with reload and debug disabled:
                    </p>
                    <EnhancedCodeBlock lang="bash" filename="terminal" snippet={prod_example} />
                </div>

                <div id="environment" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Environment &amp; configuration</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Settings resolve from <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.config</code>, environment variables, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.env</code> files. Never commit secrets &mdash; inject them per environment:
                    </p>
                    <EnhancedCodeBlock lang="bash" filename=".env" snippet={env_example} />
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        Access config at runtime via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">from nextpy.config import settings</code> &mdash; <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">settings.get("key", default)</code>.
                    </p>
                </div>

                <div id="platforms" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Platform options</h2>
                    <div class="grid sm:grid-cols-2 gap-4 mt-4">
                        <div class="p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/50">
                            <div class="text-sm font-semibold text-blue-400 mb-2">VPS / bare server</div>
                            <p class="text-sm leading-6 text-zinc-400">Run <code class="text-zinc-200 font-mono text-xs">nextpy start</code> under systemd or a process manager, fronted by Nginx/Caddy for TLS.</p>
                        </div>
                        <div class="p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/50">
                            <div class="text-sm font-semibold text-emerald-400 mb-2">Docker</div>
                            <p class="text-sm leading-6 text-zinc-400">Package <code class="text-zinc-200 font-mono text-xs">main.py</code>, <code class="text-zinc-200 font-mono text-xs">pages/</code>, <code class="text-zinc-200 font-mono text-xs">assets/</code>, and dependencies in one image.</p>
                        </div>
                        <div class="p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/50">
                            <div class="text-sm font-semibold text-violet-400 mb-2">Static export</div>
                            <p class="text-sm leading-6 text-zinc-400"><code class="text-zinc-200 font-mono text-xs">nextpy export</code> emits static files for CDN hosting &mdash; pages that need SSR still require the server.</p>
                        </div>
                        <div class="p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/50">
                            <div class="text-sm font-semibold text-amber-400 mb-2">PaaS</div>
                            <p class="text-sm leading-6 text-zinc-400">Any ASGI host (Render, Railway, Fly.io) works &mdash; set the start command to <code class="text-zinc-200 font-mono text-xs">nextpy start</code>.</p>
                        </div>
                    </div>
                </div>

                <div id="checklist" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Pre-deploy checklist</h2>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li>Set <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">DEBUG=false</code> and a strong <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">SECRET_KEY</code>.</li>
                        <li>Point the database at a managed instance; run migrations before deploy.</li>
                        <li>Run <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy build</code> so Tailwind scans production classes.</li>
                        <li>Verify <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/api</code> routes and server actions respond correctly.</li>
                    </ul>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/getting-started/route-handlers" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Route Handlers
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/upgrading" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Upgrading to v2
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
                        <li><a href="#production-build" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Production build</a></li>
                        <li><a href="#environment" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Environment &amp; config</a></li>
                        <li><a href="#platforms" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Platform options</a></li>
                        <li><a href="#checklist" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Pre-deploy checklist</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )





def getServerSideProps(context):
    return {"props": {"title": "Deploying - NextPy Docs"}}


default = DeployingGuide

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
