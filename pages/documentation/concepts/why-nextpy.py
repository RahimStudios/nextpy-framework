"""Why NextPy? — NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def WhyNextPy():
    example = """from nextpy.psx import component, interactive_component, useState

@component
def Page(props):
    # Server-rendered on every request — full Python power
    posts = fetch_posts_from_db()
    return psx(f\"\"\"
        <h1>{len(posts)} posts</h1>
        <PostList posts={posts} />
    \"\"\")

@interactive_component
def Counter():
    # Hydrates in the browser — React-like state, zero reloads
    [count, setCount] = useState(0)
    return <button onclick={lambda e: setCount(count + 1)}>{count}</button>"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Core Concepts</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Why NextPy?</span>
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
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Why NextPy?</h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy is a full-stack Python framework that delivers React-grade interactivity with Python-grade simplicity — one language, one deployable, from database to pixel.
                    </p>
                </header>

                <div id="the-problem" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The problem it solves</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Traditional Python web apps force a choice: server-rendered pages that feel dated, or a JavaScript frontend that duplicates your backend logic in a second language. NextPy removes the split — your pages, components, API routes, and business logic are all Python, compiled to the same fast paths modern JS frameworks use.
                    </p>
                </div>

                <div id="architecture" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">One runtime, three rendering modes</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Every page picks its rendering strategy automatically or explicitly — server-rendered for fresh data, static for cached content, and hydrated islands for interactivity:
                    </p>
                    <div class="p-8 rounded-xl border border-zinc-800/60 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-6 mt-6">
                        <div class="flex flex-col items-center gap-2">
                            <div class="bg-zinc-800/50 border border-zinc-700/50 rounded-lg px-4 py-3 text-sm font-mono text-zinc-300">Browser</div>
                            <svg class="w-5 h-5 text-zinc-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 14l-7 7m0 0l-7-7m7 7V3"/></svg>
                        </div>
                        <div class="bg-zinc-800/50 border border-zinc-700/50 rounded-lg px-4 py-3 text-sm font-mono text-blue-400">Hydrated islands<br/><span class="text-xs text-zinc-500">useState · useEffect · signals</span></div>
                        <div class="text-zinc-600 font-mono">+</div>
                        <div class="bg-zinc-800/50 border border-zinc-700/50 rounded-lg px-4 py-3 text-sm font-mono text-emerald-400">SSR / SSG / ISR<br/><span class="text-xs text-zinc-500">pages/ + getServerSideProps</span></div>
                        <div class="text-zinc-600 font-mono">+</div>
                        <div class="bg-zinc-800/50 border border-zinc-700/50 rounded-lg px-4 py-3 text-sm font-mono text-violet-400">API routes<br/><span class="text-xs text-zinc-500">pages/api/*.py</span></div>
                    </div>
                </div>

                <div id="key-benefits" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Key benefits</h2>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300">
                        <li><strong>Full-stack Python</strong> — pages, components, API routes, auth, and ORM models share one language and one runtime.</li>
                        <li><strong>React-like reactivity</strong> — <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useState</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useEffect</code>, and fine-grained signals update the DOM without reloads.</li>
                        <li><strong>File-system routing</strong> — folders and files under <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code> become URLs; layouts nest automatically.</li>
                        <li><strong>SSR + ISR out of the box</strong> — <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">revalidate</code> give you fresh or cached pages with zero config.</li>
                        <li><strong>Server actions</strong> — call Python functions directly from the client with typed results and auth guards.</li>
                        <li><strong>Tailwind JIT</strong> — utility classes scanned from your Python and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> strings.</li>
                    </ul>
                </div>

                <div id="example" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">What it looks like</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Server-rendered page and hydrated interactive component in the same file — no build step, no JSX toolchain, no second language:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/getting-started/upgrading" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Upgrading
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/concepts/architecture" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Architecture Overview
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
                        <li><a href="#the-problem" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The problem it solves</a></li>
                        <li><a href="#architecture" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Three rendering modes</a></li>
                        <li><a href="#key-benefits" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Key benefits</a></li>
                        <li><a href="#example" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What it looks like</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Why NextPy? - NextPy Docs"}}


default = WhyNextPy

