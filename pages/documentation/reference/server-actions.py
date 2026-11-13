"""Server Actions - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def ServerActionsAPI():
    action_example = """# pages/actions/todo_actions.py
from nextpy.server_actions import server_action, ValidationError
from nextpy.db import get_session, Todo

@server_action(name="create_todo")
async def create_todo(title: str):
    if not title:
        raise ValidationError("title", "Title cannot be empty")
    db = next(get_session())
    todo = Todo(title=title, completed=False)
    db.add(todo)
    db.commit()
    db.close()
    return {"id": todo.id}"""

    client_example = """from nextpy.psx import interactive_component, useState, useEffect, callServerAction

@interactive_component
def TodoForm():
    [title, setTitle] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def submit(e):
        e.preventDefault()
        callServerAction("create_todo", {"title": title})

    def handle_result():
        if _server_result and _server_result.get("success"):
            setTitle("")
            window.location.reload()

    useEffect(handle_result, [_server_result])

    return (
        &lt;form onsubmit={submit}&gt;
            &lt;input value={title} oninput={lambda e: setTitle(e.target.value)} /&gt;
            &lt;button type="submit" disabled={_server_loading}&gt;
                {"Saving..." if _server_loading else "Add"}
            &lt;/button&gt;
        &lt;/form&gt;
    )"""

    options_example = """@server_action(
    name="update_profile",
    schema=ProfileSchema,      # Pydantic model or ActionSchema
    auth=True,                 # require authenticated user
    roles=("admin",),          # optional role restriction
)"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-12 w-full max-w-6xl mx-auto">
                <DocsScrollSpy />

            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-16 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-6">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Reference API</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Server Actions</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">Server Actions</h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Call Python functions from the browser without writing an API route. Actions are registered with <code class="font-mono text-sm">@server_action</code> and invoked via <code class="font-mono text-sm">callServerAction</code>.
                    </p>
                </header>

                <div id="defining" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Defining an action</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Put actions in <code class="font-mono text-xs">pages/actions/</code> (or any imported module). The decorator registers the function under a name; params are filtered to the function signature and validated.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/todo_actions.py" snippet={action_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-400">
                        <li><code class="font-mono text-xs">ValidationError(field, message)</code> &mdash; returned to the client as a structured error.</li>
                        <li><code class="font-mono text-xs">ServerActionError(message, code)</code> &mdash; for domain failures like "not found".</li>
                        <li>Every result is wrapped as <code class="font-mono text-xs">{"{success, data, timestamp}"}</code> or <code class="font-mono text-xs">{"{success: false, error}"}</code>.</li>
                    </ul>
                </div>

                <div id="options" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Options</h2>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/profile.py" snippet={options_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-400">
                        <li><code class="font-mono text-xs">schema</code> &mdash; a Pydantic model or <code class="font-mono text-xs">ActionSchema</code> for input validation.</li>
                        <li><code class="font-mono text-xs">auth=True</code> &mdash; rejects unauthenticated calls.</li>
                        <li><code class="font-mono text-xs">roles</code> &mdash; tuple of allowed roles.</li>
                    </ul>
                </div>

                <div id="calling" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Calling from a component</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        <code class="font-mono text-xs">callServerAction(name, params)</code> POSTs to <code class="font-mono text-xs">/__nextpy/actions/execute</code> and writes the result into reserved state keys: <code class="font-mono text-xs">_server_result</code> and <code class="font-mono text-xs">_server_loading</code>. React to results with <code class="font-mono text-xs">useEffect(..., [_server_result])</code>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/jobs/create.py" snippet={client_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/events" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Event System
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/metadata" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Metadata &amp; SEO
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
                        <li><a href="#defining" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Defining an action</a></li>
                        <li><a href="#options" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Options</a></li>
                        <li><a href="#calling" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Calling from a component</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )





def getServerSideProps(context):
    return {"props": {"title": "Server Actions - NextPy Docs"}}


default = ServerActionsAPI

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
