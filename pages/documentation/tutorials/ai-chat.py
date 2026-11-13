"""AI Chat App - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def AIChatApp():
    chat_ui_example = '''from nextpy.psx import interactive_component, useState, useEffect, useRef, callServerAction

@interactive_component
def ChatWindow():
    [messages, set_messages] = useState([])
    [input_text, set_input_text] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)
    bottom_ref = useRef(None)

    def SendMessage():
        text = input_text.strip()
        if not text or _server_loading:
            return
        set_messages(messages + [{"role": "user", "content": text}])
        set_input_text("")
        callServerAction("chat", {"message": text})

    def HandleResult():
        if _server_result and _server_result.get("reply"):
            set_messages(messages + [
                {"role": "user", "content": _server_result.get("prompt", "")},
                {"role": "assistant", "content": _server_result["reply"]},
            ])

    def ScrollToBottom():
        if bottom_ref.current:
            bottom_ref.current.scrollIntoView({"behavior": "smooth"})

    useEffect(HandleResult, [_server_result])
    useEffect(ScrollToBottom, [messages])'''

    action_example = '''import os
import httpx
from nextpy.server_actions import server_action

@server_action()
async def chat(request, message: str = ""):
    """Proxy a chat completion to an OpenAI-compatible API."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"success": False, "error": "OPENAI_API_KEY not set"}

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": message}],
            },
        )
    data = resp.json()
    reply = data["choices"][0]["message"]["content"]
    return {"success": True, "reply": reply, "prompt": message}'''

    page_example = """from nextpy.psx import component, interactive_component

@component
def ChatPage():
    return (
        &lt;div class="max-w-3xl mx-auto h-[80vh] flex flex-col"&gt;
            &lt;h1 class="text-2xl font-bold mb-4"&gt;AI Chat&lt;/h1&gt;
            &lt;ChatWindow /&gt;
        &lt;/div&gt;
    )

default = ChatPage"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-12 w-full max-w-6xl mx-auto">
                <DocsScrollSpy />

            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-16 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-6">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Tutorials</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">AI Chat App</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">
                        AI Chat App
                    </h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Build an AI-powered chat application with NextPy.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        This tutorial builds a chat UI where the browser owns the message list and a server action proxies requests to an LLM API. The API key never reaches the client — it stays in the server action's environment.
                    </p>
                </div>

                <div id="architecture" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Architecture</h2>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div class="rounded-xl border border-zinc-800 bg-zinc-950/40 p-5">
                            <div class="text-xs font-semibold uppercase tracking-wider text-blue-400 mb-2">Browser</div>
                            <p class="text-sm text-zinc-400">ChatWindow renders messages from <code class="font-mono text-xs">useState</code> and calls the action on submit.</p>
                        </div>
                        <div class="rounded-xl border border-zinc-800 bg-zinc-950/40 p-5">
                            <div class="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">Server action</div>
                            <p class="text-sm text-zinc-400"><code class="font-mono text-xs">chat()</code> holds the API key and returns the model's reply as JSON.</p>
                        </div>
                        <div class="rounded-xl border border-zinc-800 bg-zinc-950/40 p-5">
                            <div class="text-xs font-semibold uppercase tracking-wider text-purple-400 mb-2">LLM API</div>
                            <p class="text-sm text-zinc-400">Any OpenAI-compatible endpoint — OpenAI, Anthropic proxies, or a local model server.</p>
                        </div>
                    </div>
                </div>

                <div id="chat-ui" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The chat component</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Messages live in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useState</code> — each update re-renders only the bound nodes. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_result</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_loading</code> are the reserved keys the runtime fills after the action returns. A <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useRef</code> pins the scroll container to the newest message.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/chat_window.py" snippet={chat_ui_example} />
                </div>

                <div id="server-action" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The server action</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@server_action()</code> functions are async Python that run on the server. Return a plain dict — it is serialized to JSON and lands in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_result</code>:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="lib/chat_actions.py" snippet={action_example} />
                </div>

                <div id="wiring" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Wiring the page</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        The page stays a plain <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@component</code> — only the interactive island hydrates:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/chat.py" snippet={page_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-400">
                        <li>Set <code class="font-mono text-xs">OPENAI_API_KEY</code> (or your provider's key) in the environment — never in source.</li>
                        <li>Swap the endpoint for any OpenAI-compatible API, or call a local model over <code class="font-mono text-xs">httpx</code>.</li>
                        <li>For multi-turn chat, persist messages with <code class="font-mono text-xs">nextpy.db</code> and pass history into the action.</li>
                    </ul>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/tutorials/first-app" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Your First App
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/tutorials/dashboard" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Dashboard App
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
                        <li><a href="#architecture" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Architecture</a></li>
                        <li><a href="#chat-ui" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Chat component</a></li>
                        <li><a href="#server-action" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server action</a></li>
                        <li><a href="#wiring" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Wiring the page</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )




def getServerSideProps(context):
    return {"props": {"title": "AI Chat App - NextPy Docs"}}

default = AIChatApp

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
