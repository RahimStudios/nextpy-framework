"""Internationalization (i18n) - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def I18nGuide():
    strings_example = '''# lib/i18n.py — translation tables

STRINGS = {
    "en": {"greeting": "Hello", "cta": "Get started"},
    "fr": {"greeting": "Bonjour", "cta": "Commencer"},
    "es": {"greeting": "Hola", "cta": "Empezar"},
}

def t(locale: str, key: str) -> str:
    return STRINGS.get(locale, STRINGS["en"]).get(key, key)'''

    detect_example = '''# pages/index.py — resolve locale per request

SUPPORTED = ["en", "fr", "es"]

def getServerSideProps(context):
    # 1. explicit choice cookie wins
    locale = context.request.cookies.get("locale")
    # 2. fall back to Accept-Language
    if locale not in SUPPORTED:
        accept = context.request.headers.get("accept-language", "en")
        locale = accept.split(",")[0].split("-")[0]
    if locale not in SUPPORTED:
        locale = "en"

    return {"props": {
        "locale": locale,
        "greeting": t(locale, "greeting"),
        "cta": t(locale, "cta"),
    }}'''

    switch_example = '''from nextpy.psx import interactive_component, useState, callServerAction, useEffect

@interactive_component
def LocaleSwitcher():
    [locale, set_locale] = useState(props.get("locale", "en"))

    def Switch(lang):
        # persist the choice, then reload server-rendered strings
        callServerAction("set_locale", {"locale": lang})'''

    action_example = '''from fastapi import Request, Response
from nextpy.server_actions import server_action

@server_action()
async def set_locale(request: Request, response: Response, locale: str):
    response.set_cookie("locale", locale, max_age=31536000)
    return {"success": True, "redirect": "/"}'''

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
                        <span class="text-white">Internationalization (i18n)</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">
                        Internationalization (i18n)
                    </h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Learn how to add multi-language support to your NextPy application.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-400">
        NextPy doesn't ship a dedicated i18n module — the idiomatic pattern is locale detection in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code>, a translation table in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">lib/</code>, and translated strings passed down as props. Because strings arrive via SSR, SEO and first paint stay correct in every language.
                    </p>
                </div>

                <div id="strings" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Translation tables</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Keep a nested dict per locale with a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">t()</code> helper that falls back to the default language for missing keys:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="lib/i18n.py" snippet={strings_example} />
                </div>

                <div id="detection" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Detecting the locale</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Resolve the locale per request — a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">locale</code> cookie set by the switcher wins; otherwise parse <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Accept-Language</code>; otherwise fall back to the default:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={detect_example} />
                </div>

                <div id="switching" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Switching languages</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        A small interactive component calls a server action that sets the cookie, then the app reloads so every page re-renders in the new locale:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/locale_switcher.py" snippet={switch_example} />
                    <EnhancedCodeBlock lang="python" filename="lib/locale_actions.py" snippet={action_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/redirecting" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Redirecting & Rewrites
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/testing" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Testing (Unit & E2E)
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
                        <li><a href="#strings" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Translation tables</a></li>
                        <li><a href="#detection" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Detecting locale</a></li>
                        <li><a href="#switching" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Switching</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )




def getServerSideProps(context):
    return {"props": {"title": "Internationalization (i18n) - NextPy Docs"}}

default = I18nGuide

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
