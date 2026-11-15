"""Metadata & SEO - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def MetadataAPI():
    props_example = """# pages/about.py
async def get_server_side_props(context):
    return {
        "props": {
            "title": "About Us",
            "description": "Learn what makes NextPy different."
        }
    }"""

    head_example = """from nextpy.psx import component, Head, Title, Meta

@component
def SeoPage():
    return (
        <div>
            <Head>
                <Title>Dashboard - My App</Title>
                <Meta name="description" content="Your dashboard" />
                <Meta property="og:title" content="Dashboard" />
            </Head>
            <h1>Dashboard</h1>
        </div>
    )"""

    sitemap_example = """# pages/sitemap.xml.py
def get_template():
    return "sitemap.xml"

async def get_server_side_props(context):
    from fastapi.responses import Response
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    xml += '</urlset>'
    return Response(content=xml, media_type="application/xml")"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Reference API</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Metadata &amp; SEO</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Metadata &amp; SEO</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Control page titles, meta tags, sitemaps, and robots.txt in NextPy.
                    </p>
                </header>

                <div id="page-props" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Page props</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Return <code class="font-mono text-xs">title</code> and <code class="font-mono text-xs">description</code> from <code class="font-mono text-xs">get_server_side_props</code> or <code class="font-mono text-xs">getServerSideProps</code>. Templates render them through the <code class="font-mono text-xs">title</code> variable and the <code class="font-mono text-xs">title</code> block in <code class="font-mono text-xs">_page.html</code>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/about.py" snippet={props_example} />
                </div>

                <div id="head-components" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Head components</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        In PSX pages, wrap <code class="font-mono text-xs">Title</code>, <code class="font-mono text-xs">Meta</code>, and <code class="font-mono text-xs">Script</code> inside <code class="font-mono text-xs">Head</code> to inject tags into the document head.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/dashboard.py" snippet={head_example} />
                </div>

                <div id="sitemap-robots" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">sitemap.xml &amp; robots.txt</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        File routes ending in <code class="font-mono text-xs">.xml.py</code> / <code class="font-mono text-xs">.txt.py</code> can serve raw content. Use <code class="font-mono text-xs">get_template()</code> to pick the template and return a FastAPI <code class="font-mono text-xs">Response</code> for full control.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/sitemap.xml.py" snippet={sitemap_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        This project ships working examples at <code class="font-mono text-xs">pages/sitemap.xml.py</code> and <code class="font-mono text-xs">pages/robots.txt.py</code>.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/server-actions" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Server Actions
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/performance" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Performance
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
                        <li><a href="#page-props" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Page props</a></li>
                        <li><a href="#head-components" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Head components</a></li>
                        <li><a href="#sitemap-robots" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">sitemap.xml &amp; robots.txt</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Metadata & SEO - NextPy Docs"}}


default = MetadataAPI

