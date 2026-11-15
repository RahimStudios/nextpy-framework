"""Guides hub - NextPy Documentation"""

from nextpy.psx import component, Link, register_component


@component
def GuidesHub():
    guides = [
        ("/documentation/howto/auth", "Authentication & Auth Guards", "Sessions, cookies, protected routes, and role-based access.", "M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"),
        ("/documentation/howto/database", "Database Management (ORM)", "Models, sessions, migrations, pagination, and filtering.", "M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"),
        ("/documentation/howto/api", "API Development", "REST endpoints, route handlers, request/response shapes.", "M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"),
        ("/documentation/howto/state", "State Architecture", "derived values, effects, and server sync.", "M13 10V3L4 14h7v7l9-11h-7z"),
        ("/documentation/howto/forms", "Forms & Validation", "Controlled inputs, submit handlers, and validation patterns.", "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"),
        ("/documentation/howto/fetching", "Adopting Partial Fetching", "Client-side data loading without full reloads.", "M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"),
        ("/documentation/howto/full-stack", "Full Stack Paradigms", "SSR data flow, server actions, and hydration.", "M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"),
        ("/documentation/howto/building", "Production Building", "Optimized builds, assets, and deployment prep.", "M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"),
        ("/documentation/howto/public-pages", "Public & Static Pages", "SEO-friendly rendering modes and caching.", "M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"),
        ("/documentation/howto/redirecting", "Redirecting & Rewrites", "Server-side redirects, rewrites, and route guards.", "M13 5l7 7-7 7M5 12h15"),
        ("/documentation/howto/background-tasks", "Background Tasks", "Queues, @task jobs, and async work outside requests.", "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"),
        ("/documentation/howto/realtime", "Real-Time & WebSockets", "Channels, pub/sub, and multi-user state sync.", "M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"),
        ("/documentation/howto/admin-panel", "Admin Panel", "Auto-generated CRUD admin for your models.", "M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"),
        ("/documentation/howto/middleware-guide", "Middleware", "Auth, CSRF, rate limiting, and cache middleware.", "M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"),
        ("/documentation/howto/plugins", "Plugin System", "Extend NextPy with lifecycle hooks and plugins.", "M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z"),
        ("/documentation/howto/streaming", "Streaming SSR", "Stream HTML progressively to the browser.", "M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"),
        ("/documentation/howto/devtools-debugging", "Debugging & DevTools", "Error overlay, hot reload, HMR, and debug endpoints.", "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"),
        ("/documentation/howto/i18n", "Internationalization", "Locales, translated strings, and locale routing.", "M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"),
        ("/documentation/howto/testing", "Testing", "Unit tests, component tests, and E2E workflows.", "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"),
    ]

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Guides</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">How-to Guides</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Task-oriented guides for building real features with NextPy &mdash; from auth and databases to testing and deployment.
                    </p>
                </header>

                <div id="all-guides" class="grid grid-cols-1 md:grid-cols-2 gap-5">
                    {for guide in guides:
                        <Link href={guide[0]} className="group block p-6 rounded-xl border border-zinc-800/60 bg-zinc-950/40 hover:bg-zinc-900/60 hover:border-zinc-700 transition-all">
                            <div class="flex items-start gap-4">
                                <div class="flex items-center justify-center w-10 h-10 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400 shrink-0">
                                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d={guide[3]}/></svg>
                                </div>
                                <div>
                                    <h3 class="text-base font-semibold text-white group-hover:text-blue-400 transition-colors">{guide[1]}</h3>
                                    <p class="mt-1.5 text-sm leading-relaxed text-zinc-500 group-hover:text-zinc-400 transition-colors">{guide[2]}</p>
                                </div>
                            </div>
                        </Link>
                    }
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <span class="block p-5 rounded-xl border border-zinc-800/30 bg-zinc-950/20 opacity-50 select-none">
                            <span class="block text-xs font-medium text-zinc-600 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-zinc-600">&mdash;</span>
                        </span>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/api-reference" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                API Reference
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
                        <li><a href="#all-guides" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">All guides</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Guides - NextPy Docs"}}


default = GuidesHub

