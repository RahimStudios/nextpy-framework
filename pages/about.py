from nextpy.psx import component, Link


@component
def AboutPage(props=None):
    props = props or {}
    title = props.get('title', 'About NextPy')

    principles = [
        ("One language", "Frontend and backend in Python — no context-switching, no glue code."),
        ("Zero JS build", "PSX compiles to a reactive runtime served inline — nothing to bundle."),
        ("Web fundamentals", "SSR, SSG, ISR, streaming and server actions — the full modern stack."),
        ("Batteries included", "ORM, auth, CLI, caching and API routes ship in the box."),
    ]

    stack = [
        ("Backend", "FastAPI + Uvicorn", "High-performance async framework with automatic OpenAPI documentation."),
        ("Frontend", "PSX + Tailwind CSS", "Reactive Python UI compiled to the browser — no JavaScript toolchain."),
        ("Database", "SQLAlchemy ORM", "First-class models with support for SQLite, PostgreSQL and MySQL."),
        ("Auth", "Session Auth + Guards", "Cookie sessions, login actions and protected routes out of the box."),
        ("Real-time", "WebSocket + Streaming", "Live updates, pub/sub channels and streaming responses."),
        ("Tooling", "CLI + Utilities", "nextpy create, dev and build — plus caching, metadata and SEO helpers."),
    ]

    shipped = [
        ("PSX engine", "Signal-based reactivity, selective hydration, WAAPI animations and FLIP transitions — all from Python."),
        ("SSR, SSG, ISR & SPA router", "Three rendering modes with client-side navigation, prefetching and per-layout asset loading."),
        ("Server actions & API routes", "Secure RPC-style actions plus REST endpoints and streaming responses."),
        ("Auth, ORM & CLI", "Cookie sessions, SQLAlchemy models, route guards and a scaffolding CLI."),
        ("Animation playground", "138 live animation demos with copy-paste PSX code — Motion, gestures, FLIP, exits."),
        ("Documentation site", "Tutorials, concepts, how-to guides and the full API reference."),
    ]

    roadmap = [
        "First-class file uploads",
        "Built-in internationalization (i18n)",
        "Pytest-style app testing API",
        "Plugin & template ecosystem",
        "Page-level WebSocket hooks",
    ]

    return (
        <div class="font-sans antialiased">

            {/* Hero */}
            <section class="relative overflow-hidden border-b border-gray-100">
                <div class="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_4px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]"></div>
                <div class="relative px-4 mx-auto max-w-7xl pt-20 pb-16 sm:pt-24 sm:pb-20 lg:px-8">
                    <div class="max-w-3xl mx-auto text-center">
                        <p class="text-sm font-semibold tracking-wider text-blue-600 uppercase">About</p>
                        <h1 class="mt-3 text-4xl font-extrabold tracking-tight text-gray-950 sm:text-6xl">{title}</h1>
                        <p class="max-w-2xl mx-auto mt-6 text-lg leading-8 text-gray-600">
                            Bridging Python's power with modern web development. Build production-ready
                            applications faster — frontend and backend in one language.
                        </p>
                    </div>
                </div>
            </section>

            {/* Mission */}
            <section class="py-24 bg-white">
                <div class="px-6 mx-auto max-w-7xl lg:px-8">
                    <div class="max-w-2xl">
                        <p class="text-sm font-semibold tracking-wider text-blue-600 uppercase">Our mission</p>
                        <h2 class="mt-3 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                            Python developers shouldn't have to leave Python to ship on the web.
                        </h2>
                    </div>
                    <div class="grid items-start gap-12 mt-12 lg:grid-cols-2">
                        <div class="space-y-5 text-base leading-7 text-gray-600">
                            <p>
                                NextPy was created to solve a fundamental problem: Python developers
                                shouldn't have to abandon their preferred language or ecosystem to build
                                modern web applications.
                            </p>
                            <p>
                                We combined the rendering model of modern meta-frameworks with Python's
                                elegance — creating a framework that lets you write pages, components,
                                server logic and API routes in a single language, with a reactive UI
                                engine that needs no JavaScript build step.
                            </p>
                            <p>
                                The result is a full-stack framework that stays out of your way:
                                file-based routing, SSR/SSG/ISR rendering, server actions, an ORM,
                                authentication and a CLI — all batteries included.
                            </p>
                        </div>
                        <div class="grid gap-4 sm:grid-cols-2">
                            {for p in principles:
                                <div class="p-6 border border-gray-200 rounded-2xl">
                                    <h3 class="text-base font-bold text-gray-900">{p[0]}</h3>
                                    <p class="mt-1.5 text-sm leading-6 text-gray-600">{p[1]}</p>
                                </div>
                            }
                        </div>
                    </div>
                </div>
            </section>

            {/* Tech stack */}
            <section class="py-24 bg-gray-50 border-y border-gray-100">
                <div class="px-6 mx-auto max-w-7xl lg:px-8">
                    <div class="max-w-2xl mx-auto lg:text-center">
                        <p class="text-sm font-semibold tracking-wider text-blue-600 uppercase">Tech stack</p>
                        <h2 class="mt-3 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Built on proven technology</h2>
                        <p class="mt-4 text-lg text-gray-600">Every layer is a production-grade component — nothing reinvented, nothing bolted on.</p>
                    </div>
                    <div class="grid gap-6 mt-16 sm:grid-cols-2 lg:grid-cols-3">
                        {for t in stack:
                            <div class="p-6 bg-white border border-gray-200 rounded-2xl">
                                <p class="text-xs font-semibold tracking-wider text-gray-400 uppercase">{t[0]}</p>
                                <h3 class="mt-2 text-lg font-bold text-gray-900">{t[1]}</h3>
                                <p class="mt-2 text-sm leading-6 text-gray-600">{t[2]}</p>
                            </div>
                        }
                    </div>
                </div>
            </section>

            {/* What's shipped */}
            <section class="py-24 bg-white">
                <div class="grid gap-12 px-6 mx-auto max-w-7xl lg:grid-cols-2 lg:px-8">
                    <div>
                        <p class="text-sm font-semibold tracking-wider text-blue-600 uppercase">Shipped</p>
                        <h2 class="mt-3 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">What NextPy includes today</h2>
                        <ul class="mt-10 space-y-6">
                            {for s in shipped:
                                <li class="flex items-start gap-4">
                                    <div class="flex items-center justify-center flex-shrink-0 w-6 h-6 mt-0.5 text-white rounded-full bg-emerald-600">
                                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg>
                                    </div>
                                    <div>
                                        <strong class="text-gray-900">{s[0]}</strong>
                                        <p class="mt-1 text-sm leading-6 text-gray-600">{s[1]}</p>
                                    </div>
                                </li>
                            }
                        </ul>
                    </div>
                    <div>
                        <p class="text-sm font-semibold tracking-wider text-gray-400 uppercase">On the roadmap</p>
                        <div class="mt-10 p-8 bg-gray-50 border border-gray-200 rounded-2xl">
                            <ul class="space-y-4">
                                {for r in roadmap:
                                    <li class="flex items-center gap-3 text-gray-700">
                                        <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
                                        {r}
                                    </li>
                                }
                            </ul>
                            <p class="mt-6 text-sm text-gray-500">Roadmap items are prioritized by community need — vote on GitHub Discussions.</p>
                        </div>
                        <div class="grid gap-4 mt-8 sm:grid-cols-2">
                            <Link href="/" className="block p-6 text-center transition-all bg-gray-950 rounded-2xl hover:bg-gray-800">
                                <span class="text-sm font-bold text-white">Try the framework →</span>
                            </Link>
                            <Link href="/documentation" className="block p-6 text-center transition-all border border-gray-300 rounded-2xl hover:bg-gray-50">
                                <span class="text-sm font-bold text-gray-900">Read the docs</span>
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Community CTA */}
            <section class="px-6 pb-24 mx-auto max-w-7xl lg:px-8">
                <div class="relative px-8 py-16 overflow-hidden text-center text-white bg-gray-950 sm:px-16 rounded-3xl">
                    <div class="absolute inset-0 bg-[radial-gradient(#1f2937_1px,transparent_4px)] [background-size:16px_16px] opacity-40"></div>
                    <div class="relative">
                        <h2 class="text-3xl font-bold tracking-tight sm:text-4xl">Join the community</h2>
                        <p class="max-w-xl mx-auto mt-4 text-lg text-gray-400">
                            NextPy is open-source. Contribute, report issues, or just say hello.
                        </p>
                        <div class="flex flex-wrap justify-center gap-4 mt-10">
                            <Link href="https://github.com/RAHIMSTUDIOS/nextpy-framework" target="_blank" className="px-8 py-3 text-sm font-bold text-white transition border border-gray-700 rounded-full hover:bg-gray-800">
                                GitHub
                            </Link>
                            <Link href="/documentation" className="px-8 py-3 text-sm font-bold text-gray-950 transition bg-white rounded-full hover:bg-gray-200">
                                Documentation
                            </Link>
                            <Link href="https://github.com/RAHIMSTUDIOS/nextpy-framework/discussions" target="_blank" className="px-8 py-3 text-sm font-bold text-white transition border border-gray-700 rounded-full hover:bg-gray-800">
                                Discussions
                            </Link>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )


def getServerSideProps(context):
    return {
        'props': {
            'title': 'About NextPy'
        }
    }


default = AboutPage
