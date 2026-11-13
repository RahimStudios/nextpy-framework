"""Error Handling — NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def ErrorHandlingGuide():
    gssp_example = """from nextpy.psx import component
from nextpy import getServerSideProps
from nextpy.utils import PropsResult

@component
def Page(props):
    post = props.get("post")
    if post is None:
        return &lt;p&gt;Post unavailable&lt;/p&gt;
    return &lt;article&gt;&lt;h1&gt;{post["title"]}&lt;/h1&gt;&lt;/article&gt;

@getServerSideProps



def getServerSideProps(context):
    slug = context["params"].get("slug")
    try:
        post = fetch_post(slug)  # your data source
    except Exception as exc:
        # Log server-side, return a graceful state
        print(f"fetch_post failed: {exc}")
        return PropsResult(props={"post": None})
    if post is None:
        return PropsResult(notFound=True)  # renders the 404 page
    return PropsResult(props={"post": post})"""

    redirect_example = """from nextpy.psx import component
from nextpy import getServerSideProps
from nextpy.utils import PropsResult

@getServerSideProps
def getServerSideProps(context):
    if not context.get("preview"):
        return PropsResult(redirect={"destination": "/login", "permanent": False})
    return PropsResult(props={})"""

    api_example = """# pages/api/posts/[id].py
from fastapi import HTTPException

async def get(request, params):
    post = find_post(params["id"])
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": post}

async def delete(request, params):
    if not request.state.user:
        return {"error": "Unauthorized"}, 401
    remove_post(params["id"])
    return {"deleted": True}"""

    action_example = """from nextpy.server_actions import server_action, ValidationError, ServerActionError

@server_action
def create_post(data: dict, user_id: str):
    title = (data.get("title") or "").strip()
    if not title:
        raise ValidationError("title", "Title is required")
    if len(title) > 200:
        raise ServerActionError("Title too long", code="TITLE_TOO_LONG")
    # ... persist ...
    return {"id": 123, "title": title}"""

    client_example = """from nextpy.psx import interactive_component, useState, useEffect, callServerAction

@interactive_component
def ContactForm():
    [email, setEmail] = useState("")
    [error, setError] = useState("")
    [result, setResult] = useState(None)

    def submit(e):
        e.preventDefault()
        setError("")
        callServerAction("contact", {"email": email})

    def handle_result():
        if result and result.get("success"):
            setError("")
        elif result and result.get("error"):
            setError(result["error"])

    useEffect(handle_result, [result])

    return (
        &lt;form onsubmit={submit}&gt;
            &lt;input value={email} oninput={lambda e: setEmail(e.target.value)} /&gt;
            &lt;div style={"display: " + ("block" if error else "none")} class="text-red-600 text-sm"&gt;
                {error}
            &lt;/div&gt;
            &lt;button type="submit"&gt;Send&lt;/button&gt;
        &lt;/form&gt;
    )"""

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
                        <span class="text-white">Error Handling</span>
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
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">Error Handling</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Errors surface at four layers &mdash; data fetching, API routes, server actions, and the client. Each has its own mechanism; this page covers all of them.
                    </p>
                </header>

                <div id="data-fetching-errors" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Data fetching errors</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Catch failures inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code> and return graceful props &mdash; an unhandled exception produces a 500. Use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">PropsResult(notFound=True)</code> for missing resources and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">PropsResult(redirect=...)</code> for auth gates:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/posts/[slug].py" snippet={gssp_example} />
                    <EnhancedCodeBlock lang="python" filename="pages/dashboard.py" snippet={redirect_example} />
                </div>

                <div id="api-errors" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">API route errors</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Raise FastAPI's <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">HTTPException</code> for proper status codes, or send a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">(body, status)</code> tuple:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/posts/[id].py" snippet={api_example} />
                </div>

                <div id="server-action-errors" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Server action errors</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Raise <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ValidationError(field, message)</code> for field-level failures or <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ServerActionError(message, code)</code> for general failures. The client receives a structured <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&#123;success: False, error: ...&#125;</code> result:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="lib/actions.py" snippet={action_example} />
                </div>

                <div id="client-errors" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Client-side display</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Keep error elements mounted but hidden &mdash; toggle visibility from state so screen readers and CSS transitions behave predictably:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/contact_form.py" snippet={client_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/getting-started/caching" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Caching & Revalidation
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/styling" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Styling
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
                        <li><a href="#data-fetching-errors" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Data fetching errors</a></li>
                        <li><a href="#api-errors" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">API route errors</a></li>
                        <li><a href="#server-action-errors" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server action errors</a></li>
                        <li><a href="#client-errors" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Client-side display</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Error Handling - NextPy Docs"}}


default = ErrorHandlingGuide

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
