from nextpy.psx import component, psx, Link

_SECTION_CLS = "group/section"
_SUMMARY_CLS = "flex items-center justify-between list-none py-2 text-zinc-200 hover:text-white cursor-pointer transition-colors"
_ICON_CLS = "w-4 h-4 text-zinc-400 group-hover/section:text-zinc-200 transition-colors"
_CHEVRON_CLS = "w-3.5 h-3.5 text-zinc-500 group-open/section:rotate-90 transition-transform duration-200"
_UL_CLS = "mt-1 space-y-1 border-l border-zinc-800 pl-4 ml-2 text-zinc-400"
_LINK_CLS = "block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all"


def _section(title, icon_path, items, open_=False):
    lis = "\n".join(
        f'                    <li><Link href="{href}" className="{_LINK_CLS}">{label}</Link></li>'
        for href, label in items
    )
    return f"""
            <details class="{_SECTION_CLS}"{' open' if open_ else ''}>
                <summary class="{_SUMMARY_CLS}">
                    <span class="flex items-center gap-2.5">
                        <svg class="{_ICON_CLS}" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="{icon_path}" />
                        </svg>
                        {title}
                    </span>
                    <svg class="{_CHEVRON_CLS}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                </summary>
                <ul class="{_UL_CLS}">
{lis}
                </ul>
            </details>"""


@component
def EnhancedSidebar():
    """Enhanced interactive sidebar using collapsible HTML5 sections."""
    return psx("""
        <aside class="w-full space-y-4 text-sm font-medium select-none">

            <Link href="/documentation" className="flex items-center gap-2.5 py-2 text-zinc-200 rounded-md hover:text-white transition-colors">
                <svg class="w-4 h-4 text-zinc-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                Introduction
            </Link>
""" + "\n".join([
        _section("Tutorials",
            "M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253",
            [
                ("/documentation/tutorials/first-app", "Your First App"),
                ("/documentation/tutorials/todo-app", "Todo App"),
                ("/documentation/tutorials/blog-app", "Blog App"),
                ("/documentation/tutorials/ai-chat", "AI Chat App"),
                ("/documentation/tutorials/dashboard", "Analytics Dashboard"),
            ], open_=True),
        _section("Getting Started",
            "M13 10V3L4 14h7v7l9-11h-7z",
            [
                ("/documentation/getting-started/installation", "Installation"),
                ("/documentation/getting-started/project-structure", "Project Structure"),
                ("/documentation/getting-started/layouts-pages", "Layouts and Pages"),
                ("/documentation/getting-started/linking", "Linking and Navigation"),
                ("/documentation/getting-started/fetching-data", "Fetching Data"),
                ("/documentation/getting-started/error-handling", "Error Handling"),
                ("/documentation/getting-started/styling", "Styling (Tailwind)"),
                ("/documentation/getting-started/route-handlers", "Route Handlers"),
            ], open_=True),
        _section("How-to Guides",
            "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01",
            [
                ("/documentation/guides", "Guides Overview"),
                ("/documentation/howto/auth", "Authentication & Auth Guards"),
                ("/documentation/howto/database", "Database Management (ORM)"),
                ("/documentation/howto/api", "API Development"),
                ("/documentation/howto/state", "State Architecture"),
                ("/documentation/howto/forms", "Forms & Validation"),
                ("/documentation/howto/full-stack", "Full Stack Paradigms"),
                ("/documentation/howto/public-pages", "Public & Static Pages"),
                ("/documentation/howto/redirecting", "Redirecting & Rewrites"),
                ("/documentation/howto/background-tasks", "Background Tasks"),
                ("/documentation/howto/realtime", "Real-Time & WebSockets"),
                ("/documentation/howto/admin-panel", "Admin Panel"),
                ("/documentation/howto/middleware-guide", "Middleware"),
                ("/documentation/howto/plugins", "Plugin System"),
                ("/documentation/howto/streaming", "Streaming SSR"),
                ("/documentation/howto/devtools-debugging", "Debugging & DevTools"),
            ]),
        _section("Core Concepts",
            "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
            [
                ("/documentation/concepts/why-nextpy", "Why NextPy?"),
                ("/documentation/concepts/architecture", "Architecture Overview"),
                ("/documentation/concepts/psx-internals", "PSX Core Internals"),
                ("/documentation/concepts/routing-engine", "Routing Engine"),
                ("/documentation/concepts/rendering", "Rendering (SSR, SSG, ISR)"),
                ("/documentation/concepts/state-model", "State Management Model"),
                ("/documentation/concepts/compilation", "Compilation Pipeline"),
                ("/documentation/concepts/security", "Security & Sandboxing"),
                ("/documentation/concepts/nextpy-vs-python-frameworks", "vs Python Frameworks"),
                ("/documentation/concepts/nextpy-vs-nextjs", "vs Next.js"),
            ]),
        _section("API Reference",
            "M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4",
            [
                ("/documentation/api-reference", "API Reference Overview"),
                ("/documentation/reference/cli", "CLI Engine Commands"),
                ("/documentation/reference/config", "Configuration (nextpy.config)"),
                ("/documentation/reference/components", "Built-in Elements"),
                ("/documentation/reference/psx-api", "PSX API"),
                ("/documentation/reference/hooks", "State & Hooks"),
                ("/documentation/reference/data-fetching", "Data Fetching"),
                ("/documentation/reference/router", "Router API"),
                ("/documentation/reference/events", "Event System"),
                ("/documentation/reference/server-actions", "Server Actions"),
                ("/documentation/reference/auth-api", "Authentication API"),
                ("/documentation/reference/state-sync-api", "State Sync API"),
                ("/documentation/reference/metadata", "Metadata & SEO"),
                ("/documentation/reference/performance", "Performance"),
                ("/documentation/reference/utils", "Utility Modules"),
                ("/documentation/reference/platform-utils", "Platform Utilities"),
                ("/documentation/reference/security-api", "Security API"),
                ("/documentation/reference/api-router", "API Router"),
                ("/documentation/reference/caching", "In-Memory Cache"),
                ("/documentation/reference/typescript", "TypeScript Integration"),
            ]),
        _section("Advanced Guides",
            "M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z",
            [
                ("/documentation/getting-started/caching", "Caching & Revalidation"),
                ("/documentation/getting-started/upgrading", "Upgrading NextPy"),
                ("/documentation/howto/fetching", "Partial Data Fetching"),
                ("/documentation/howto/i18n", "Internationalization (i18n)"),
                ("/documentation/howto/testing", "Testing (Unit & E2E)"),
            ]),
        _section("Deployment",
            "M2.25 15a4.5 4.5 0 004.5 4.5H18a3.75 3.75 0 001.332-7.257 3 3 0 00-3.758-3.848 5.25 5.25 0 00-10.233 2.33A4.502 4.502 0 002.25 15z",
            [
                ("/documentation/getting-started/deploying", "Deploying NextPy"),
                ("/documentation/howto/building", "Production Building"),
                ("/documentation/howto/deployment", "Deployment Guide"),
            ]),
        _section("Legacy Docs (v0)",
            "M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4",
            [
                ("/legacy/installation", "Installation (Old)"),
                ("/legacy/quickstart", "Quick Start"),
                ("/legacy/project-architecture", "Project Architecture"),
                ("/legacy/migration", "Migration Guide"),
            ]),
    ]) + """

        </aside>
    """)
