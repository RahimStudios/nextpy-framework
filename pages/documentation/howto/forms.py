"""Forms & Validation - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def FormsGuide():
    validation_example = """from fastapi import Request, Response
from nextpy.server_actions import server_action, ValidationError

@server_action()
async def submit_contact(request: Request, response: Response,
                         email: str = "", message: str = ""):
    if not email or "@" not in email:
        raise ValidationError("email", "Enter a valid email address")
    if len(message) < 10:
        raise ValidationError("message", "Message must be at least 10 characters")
    # ... persist, send mail ...
    return {"success": True, "message": "Thanks — we will reply soon."}"""

    result_example = """def HandleSubmit():
    if _server_result:
        if _server_result.get("success"):
            set_sent(True)
            set_message("")
        else:
            # ValidationError surfaces as {"success": False, "error": ...}
            set_error(_server_result.get("error", "Something went wrong"))

useEffect(HandleSubmit, [_server_result])"""

    snippet_0 = """from nextpy.psx import interactive_component, useState, callServerAction

@interactive_component
def ContactForm():
    [email, setEmail] = useState("")
    [message, setMessage] = useState("")
    
    def handle_submit(e):
        e.preventDefault()
        callServerAction("submit_contact", {"email": email, "message": message})
    
    return (
        &lt;form onsubmit={handle_submit}&gt;
            &lt;input value={email} oninput={lambda e: setEmail(e.target.value)} /&gt;
            &lt;textarea value={message} oninput={lambda e: setMessage(e.target.value)}&gt;&lt;/textarea&gt;
            &lt;button type="submit"&gt;Submit&lt;/button&gt;
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
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Forms & Validation</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">
                        Forms & Validation
                    </h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Learn how to handle forms and validation in NextPy.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        NextPy provides server actions for form handling with built-in validation support.
                    </p>
                </div>

                <div id="form-handling" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Form Handling</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Use server actions for form submissions:
                    </p>
                    
                    <EnhancedCodeBlock lang="python" filename="example.py" snippet={snippet_0} />
                </div>

                <div id="validation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Server-side validation</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Never trust the client — validate inside the action. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ValidationError(field, message)</code> returns a structured error the UI can display per-field:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="lib/contact_actions.py" snippet={validation_example} />
                </div>

                <div id="handling-results" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Handling the result</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Watch <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_result</code> in a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useEffect</code> to flip the UI between idle, loading via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_loading</code>, success, and error states:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/contact_form.py" snippet={result_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/state" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                State Architecture
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/fetching" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Adopting Partial Fetching
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
                        <li><a href="#form-handling" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Form Handling</a></li>
                        <li><a href="#validation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Validation</a></li>
                        <li><a href="#handling-results" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Handling results</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )




def getServerSideProps(context):
    return {"props": {"title": "Forms & Validation - NextPy Docs"}}

default = FormsGuide

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
