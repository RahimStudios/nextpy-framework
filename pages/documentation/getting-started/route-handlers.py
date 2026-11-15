"""Route Handlers — NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def RouteHandlers():
    hello_example = """# pages/api/hello.py
async def get(request, params):
    return {"message": "Hello from an API route"}"""

    posts_example = """# pages/api/posts.py
from nextpy.db import get_session, Post

async def get(request, params):
    db = next(get_session())
    posts = db.query(Post).limit(20).all()
    db.close()
    return {"posts": [p.title for p in posts]}"""

    create_example = """# pages/api/posts.py
async def post(request, params):
    data = await request.json()
    db = next(get_session())
    post = Post(title=data.get("title"), body=data.get("body"))
    db.add(post)
    db.commit()
    db.close()
    return {"id": post.id, "created": True}, 201"""

    methods_example = """# pages/api/items.py
async def get(request, params):
    return {"items": []}

async def post(request, params):
    return {"created": True}, 201

async def delete(request, params):
    return {"deleted": True}"""

    dynamic_example = """# pages/api/posts/[id].py
from nextpy.db import get_session, Post

async def get(request, params):
    post_id = params["id"]
    db = next(get_session())
    post = db.query(Post).filter(Post.id == int(post_id)).first()
    db.close()
    if not post:
        return {"error": "Not found"}, 404
    return {"id": post.id, "title": post.title}"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Getting Started</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Route Handlers</span>
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
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Route Handlers</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Create REST API endpoints by adding Python files to the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/api</code> directory. The file path maps directly to the URL — no router configuration needed.
                    </p>
                </header>

                <div id="convention" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">File-system convention</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Any <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.py</code> file inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/api/</code> is served as an endpoint. Folders create path segments and bracketed names capture parameters:
                    </p>

                    <div class="p-8 rounded-xl border border-zinc-800/60 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 mt-6">
                        <div class="w-56 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                            <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages/api</div>
                            <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>health.py</div>
                                <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>posts.py</div>
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>posts</div>
                                <div class="flex items-center gap-2 pl-4 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>[id].py</div>
                            </div>
                        </div>
                        <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                        <div class="space-y-2 shrink-0">
                            <div class="bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-blue-400">/api/health</div>
                            <div class="bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-blue-400">/api/posts</div>
                            <div class="bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-blue-400">/api/posts/42</div>
                        </div>
                    </div>

                    <div class="overflow-hidden rounded-xl border border-zinc-800/80 mt-6">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-400">
                                <tr><th class="text-left px-4 py-2.5 font-medium">File</th><th class="text-left px-4 py-2.5 font-medium">Endpoint</th></tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr><td class="px-4 py-2.5 font-mono text-xs">pages/api/health.py</td><td class="px-4 py-2.5 font-mono text-xs text-blue-400">/api/health</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs">pages/api/posts.py</td><td class="px-4 py-2.5 font-mono text-xs text-blue-400">/api/posts</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs">pages/api/posts/[id].py</td><td class="px-4 py-2.5 font-mono text-xs text-blue-400">/api/posts/:id</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs">pages/api/users/settings.py</td><td class="px-4 py-2.5 font-mono text-xs text-blue-400">/api/users/settings</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="basic-handler" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Basic handler</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Handlers are plain async functions — no decorator needed. They receive the FastAPI <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">request</code> and a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">params</code> dict, and return a JSON-serializable value:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/hello.py" snippet={hello_example} />
                    <p class="text-base leading-7 text-zinc-300 mt-4">
                        Return a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">(body, status_code)</code> tuple to set the HTTP status, a FastAPI <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Response</code> for full control, or raise <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">HTTPException</code> for errors:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/posts.py" snippet={create_example} />
                </div>

                <div id="http-methods" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">HTTP methods</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Define lowercase <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">post</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">put</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">patch</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">delete</code>, or <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">head</code> functions to handle specific verbs. A module-level <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">handler</code> acts as a catch-all.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/items.py" snippet={methods_example} />
                </div>

                <div id="database" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Database access</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        API routes share the app's SQLAlchemy session. Use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_session()</code> for reads and writes — always close the session when done:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/posts.py" snippet={posts_example} />
                </div>

                <div id="dynamic-routes" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Dynamic segments</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Bracketed filename segments become path parameters. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/api/posts/[id].py</code> serves <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/api/posts/42</code> with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">params["id"] == "42"</code>:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/posts/[id].py" snippet={dynamic_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/getting-started/styling" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Styling
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/deploying" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Deploying
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
                        <li><a href="#convention" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">File-system convention</a></li>
                        <li><a href="#basic-handler" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Basic handler</a></li>
                        <li><a href="#http-methods" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">HTTP methods</a></li>
                        <li><a href="#database" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Database access</a></li>
                        <li><a href="#dynamic-routes" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Dynamic segments</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Route Handlers - NextPy Docs"}}


default = RouteHandlers

