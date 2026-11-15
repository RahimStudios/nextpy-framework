"""Performance - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def PerformanceAPI():
    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Reference API</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Performance</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Performance</h1>
                    <p class="leading-relaxed text-zinc-300">
                        How NextPy renders, caches, hydrates, and hot-reloads &mdash; and how to keep your app fast.
                    </p>
                </header>

                <div id="rendering" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Rendering model</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><strong class="text-zinc-200">SSR by default</strong> &mdash; every page is server-rendered to HTML on each request (or served from cache when safe).</li>
                        <li><strong class="text-zinc-200">Selective hydration</strong> &mdash; only components marked interactive hydrate in the browser; static markup stays untouched.</li>
                        <li><strong class="text-zinc-200">Fine-grained bindings</strong> &mdash; state updates patch bound DOM nodes via <code class="font-mono text-xs">data-bind</code> attributes instead of re-rendering the page.</li>
                        <li><strong class="text-zinc-200">rAF batching</strong> &mdash; scroll and mouse-driven updates are batched through <code class="font-mono text-xs">requestAnimationFrame</code>.</li>
                    </ul>
                </div>

                <div id="caching" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">HTTP caching</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The server computes an ETag for every page. Requests without cookies or auth headers on cacheable routes get <code class="font-mono text-xs">Cache-Control: private, max-age=30, stale-while-revalidate=120</code> and support <code class="font-mono text-xs">304 Not Modified</code>. Pages with <code class="font-mono text-xs">getServerSideProps</code> always send <code class="font-mono text-xs">no-store</code>.
                    </p>
                </div>

                <div id="static-generation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Static generation &amp; ISR</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Use <code class="font-mono text-xs">getStaticProps</code> to render at build time and <code class="font-mono text-xs">revalidate</code> for Incremental Static Regeneration. See <Link href="/documentation/reference/data-fetching" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">Data Fetching</Link>.
                    </p>
                </div>

                <div id="hot-reload" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Hot reload &amp; HMR</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        With <code class="font-mono text-xs">NEXTPY_HOT_RELOAD=True</code> (default), file changes reload modules and the client router picks up the new page without a full refresh. JSX syntax errors render a dedicated error page with the offending file and line.
                    </p>
                </div>

                <div id="tips" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Performance tips</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li>Keep server-only objects (DB sessions, request) out of component props &mdash; only JSON-safe values hydrate.</li>
                        <li>Prefer <code class="font-mono text-xs">getStaticProps</code> for content that changes rarely; add <code class="font-mono text-xs">revalidate</code> instead of SSR when possible.</li>
                        <li>Use <code class="font-mono text-xs">useFetch</code> for data that only matters after interaction instead of blocking SSR.</li>
                        <li>Avoid heavy work in <code class="font-mono text-xs">getServerSideProps</code> &mdash; it runs on every request.</li>
                        <li>Mark long lists with stable keys so updates patch efficiently.</li>
                    </ul>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/metadata" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Metadata &amp; SEO
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/utils" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Utility Modules
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
                        <li><a href="#rendering" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Rendering model</a></li>
                        <li><a href="#caching" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">HTTP caching</a></li>
                        <li><a href="#static-generation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Static generation</a></li>
                        <li><a href="#hot-reload" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Hot reload</a></li>
                        <li><a href="#tips" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Performance tips</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Performance - NextPy Docs"}}


default = PerformanceAPI

