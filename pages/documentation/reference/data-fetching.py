"""Data Fetching - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def DataFetchingAPI():
    ssr_example = """from nextpy.psx import component
from nextpy.db import get_session, Job

@component
def JobList(props):
    jobs = props.get("jobs", [])
    return (
        <ul>
            {for job in jobs:
                <li>{job["title"]} - {job["company"]}</li>
            }
        </ul>
    )


def getServerSideProps(context):
    db = next(get_session())
    jobs = db.query(Job).limit(20).all()
    db.close()
    return {
        "props": {
            "jobs": [{"title": j.title, "company": j.company} for j in jobs]
        }
    }

default = JobList"""

    ssg_example = """def getStaticProps(context):
    posts = fetch_posts_from_cms()
    return {
        "props": {"posts": posts},
        "revalidate": 60  # ISR: regenerate at most every 60s
    }"""

    client_example = """from nextpy.psx import component, useFetch

@component
def LiveStats():
    fetch = useFetch("/api/stats")
    data = fetch["data"] or {}

    return <p>Total users: {data.get("users", 0)}</p>"""

    api_example = """# pages/api/users.py - file-based API route
from nextpy.db import get_session, User

async def get(request):
    db = next(get_session())
    users = db.query(User).all()
    db.close()
    return {"users": [{"id": u.id, "name": u.name} for u in users]}"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Reference API</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Data Fetching</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Data Fetching</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Three ways to get data into a NextPy page: server-side props, static generation, and client-side fetching.
                    </p>
                </header>

                <div id="getserversideprops" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">getServerSideProps (SSR)</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Define a module-level <code class="font-mono text-xs">getServerSideProps(context)</code> function. It runs on every request; its <code class="font-mono text-xs">props</code> dict is passed to your component. Use it for per-user or live data.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/jobs/index.py" snippet={ssr_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        The <code class="font-mono text-xs">context</code> dict exposes <code class="font-mono text-xs">params</code>, <code class="font-mono text-xs">query</code>, and <code class="font-mono text-xs">request</code>. Pages using SSR are never served from the static cache.
                    </p>
                </div>

                <div id="getstaticprops" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">getStaticProps (SSG / ISR)</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">getStaticProps(context)</code> runs at build time and caches the result. Add <code class="font-mono text-xs">revalidate</code> (seconds) for Incremental Static Regeneration.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/blog/[slug].py" snippet={ssg_example} />
                </div>

                <div id="client-fetching" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Client-side fetching</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Use <code class="font-mono text-xs">useFetch(url)</code> inside a component to load JSON from an API route after hydration. Returns <code class="font-mono text-xs">data</code>, <code class="font-mono text-xs">loading</code>, <code class="font-mono text-xs">error</code>, and <code class="font-mono text-xs">refetch</code>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/stats.py" snippet={client_example} />
                </div>

                <div id="api-routes" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">API routes</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Files under <code class="font-mono text-xs">pages/api/</code> become HTTP endpoints. Define async <code class="font-mono text-xs">get</code>, <code class="font-mono text-xs">post</code>, <code class="font-mono text-xs">put</code>, <code class="font-mono text-xs">patch</code>, <code class="font-mono text-xs">delete</code>, or <code class="font-mono text-xs">head</code> functions; handlers receive <code class="font-mono text-xs">request</code> and <code class="font-mono text-xs">params</code> for dynamic segments.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/users.py" snippet={api_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/hooks" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Hooks API
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/router" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Router API
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
                        <li><a href="#getserversideprops" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">getServerSideProps</a></li>
                        <li><a href="#getstaticprops" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">getStaticProps</a></li>
                        <li><a href="#client-fetching" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Client-side fetching</a></li>
                        <li><a href="#api-routes" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">API routes</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Data Fetching - NextPy Docs"}}


default = DataFetchingAPI

