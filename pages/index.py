from nextpy.psx import component, Link, psx
import html


@component
def EnhancedCodeBlock(props=None):
    """Enhanced code block component for displaying code snippets"""
    props = props or {}
    snippet = props.get("snippet", props.get("code", ""))
    if isinstance(snippet, str):
        snippet = snippet.replace('_RAW_CODE:', '')
        snippet = html.unescape(snippet)
        snippet = snippet.replace('&#10;', '\n')
        snippet = snippet.replace('\\n', '\n')

    lang = props.get("lang", "python")
    filename = props.get("filename", None)

    lang_display = html.escape(str(lang))
    code_class = f"language-{lang_display} font-mono block whitespace-pre"

    filename_html = ''
    if filename:
        filename_html = (
            '<span class="text-xs font-mono font-medium text-zinc-300/90 select-none tracking-tight truncate max-w-[280px] inline-block align-bottom">'
            + html.escape(str(filename)) + '</span>'
        )

    return psx(f"""
        <div class="my-6 overflow-hidden rounded-2xl border border-zinc-800/70 bg-[#0a0a0c] font-sans shadow-[0_8px_30px_rgb(0,0,0,0.35)] antialiased group ring-1 ring-white/[0.03]">
            <div class="flex items-center justify-between pl-4 pr-3 py-2.5 border-b border-zinc-800/60 bg-gradient-to-b from-zinc-900/70 to-zinc-900/30 select-none">
                <div class="flex items-center gap-3.5 min-w-0">
                    <div class="flex items-center gap-1.5 shrink-0" aria-hidden="true">
                        <span class="w-3 h-3 rounded-full bg-[#ff5f57] shadow-[inset_0_0_0_0.5px_rgba(0,0,0,0.3)]"></span>
                        <span class="w-3 h-3 rounded-full bg-[#febc2e] shadow-[inset_0_0_0_0.5px_rgba(0,0,0,0.3)]"></span>
                        <span class="w-3 h-3 rounded-full bg-[#28c840] shadow-[inset_0_0_0_0.5px_rgba(0,0,0,0.3)]"></span>
                    </div>
                    <div class="flex items-center gap-2.5 min-w-0">
                        {filename_html}
                        <span class="shrink-0 px-1.5 py-0.5 text-[10px] font-mono font-semibold tracking-wider text-zinc-500 uppercase bg-zinc-900/80 rounded-md border border-zinc-800/80">
                            {lang_display}
                        </span>
                    </div>
                </div>
                <button
                    class="shrink-0 ml-3 inline-flex items-center gap-1.5 px-2.5 py-1 text-[11px] font-medium text-zinc-400 hover:text-zinc-100 bg-zinc-900/60 hover:bg-zinc-800/70 border border-zinc-800/70 hover:border-zinc-700 rounded-lg transition-all duration-150"
                    onclick="navigator.clipboard.writeText(this.closest('.group').querySelector('code').innerText);var l=this.querySelector('.cb-label');l.textContent='Copied';setTimeout(()=>l.textContent='Copy',1500)"
                >
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                    <span class="cb-label">Copy</span>
                </button>
            </div>
            <code class="block p-5 overflow-x-auto text-[13px] leading-[1.7] text-zinc-200 scrollbar-thin bg-[#0a0a0c] selection:bg-blue-500/25 selection:text-blue-100 {code_class}">{{snippet}}</code>
        </div>
    """)


@component
def Page(props=None):
    props = props or {}
    title = props.get("title", "NextPy - The Python Framework")

    description = props.get(
        "description",
        "NextPy is a Python-first full-stack framework. Build reactive interfaces, "
        "render pages on the server, and power your entire application with Python."
    )

    counter_code = (
        "from nextpy.psx import component, useState\n\n"
        "@component\n"
        "def Counter(props=None):\n"
        "    [count, set_count] = useState(0)\n\n"
        "    def increment():\n"
        "        set_count(count + 1)\n\n"
        "    return (\n"
        "        <div>\n"
        "            <h1>{count}</h1>\n"
        "            <button onClick={increment}>\n"
        "                Increment\n"
        "            </button>\n"
        "        </div>\n"
        "    )"
    )

    return (
        <div class="font-sans antialiased bg-white text-gray-900">

            {/* Hero */}
            <section class="relative overflow-hidden min-h-screen flex items-center bg-gradient-to-b from-blue-50 to-white">
                <div class="absolute inset-0 bg-[radial-gradient(#e0e7ff_1px,transparent_4px)] [background-size:20px_20px] opacity-50"></div>

                <div class="relative mx-auto max-w-7xl px-6 py-20 lg:px-8">
                    <div class="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-16 items-center">
                        {/* Left - Content */}
                        <div>
                            <h1 class="mt-8 text-5xl font-bold leading-[1.1] tracking-tight text-gray-900 sm:text-6xl lg:text-7xl">
                                Write Python.<br />
                                <span class="text-blue-600">Build the modern web.</span>
                            </h1>

                            <p class="mt-8 max-w-xl text-lg leading-relaxed text-gray-600">
                                {description}
                            </p>

                            <div class="mt-10 flex flex-wrap items-center gap-4">
                                <Link href="/documentation" className="bg-blue-600 px-8 py-3.5 text-sm font-semibold text-white transition-colors hover:bg-blue-700 shadow-lg shadow-blue-600/30">
                                    Get Started →
                                </Link>
                                <Link href="/documentation" className="border border-gray-300 bg-white px-8 py-3.5 text-sm font-semibold text-gray-700 transition-colors hover:bg-gray-50">
                                    Explore Docs
                                </Link>
                            </div>

                            <p class="mt-8 text-sm text-gray-500">
                                Built with NextPy · Python UI · A single Python-first development experience
                            </p>
                        </div>

                        {/* Right - Code preview */}
                        <div class="relative">
                            <EnhancedCodeBlock
                                snippet={counter_code}
                                lang="Python"
                                filename="pages/counter.py"
                            />
                        </div>
                    </div>
                </div>
            </section>

            {/* Capabilities */}
            <section class="py-24 bg-gray-50">
                <div class="px-6 mx-auto max-w-7xl lg:px-8">
                    <div class="max-w-2xl mx-auto lg:text-center">
                        <p class="text-sm font-semibold tracking-wider text-blue-600 uppercase">Everything included</p>
                        <h2 class="mt-3 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">One framework, every layer</h2>
                        <p class="mt-4 text-lg text-gray-600">NextPy covers rendering, reactivity, data and deployment — so you can focus on product, not plumbing.</p>
                    </div>

                    <div class="grid max-w-6xl grid-cols-1 gap-6 mx-auto mt-16 sm:grid-cols-2 lg:grid-cols-3">
                        <Link href="/documentation/concepts/rendering" className="group block p-8 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-xl">
                            <div class="flex items-center justify-center w-12 h-12 text-white bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg">
                                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
                                </svg>
                            </div>
                            <h3 class="mt-6 text-lg font-bold text-gray-900">Rendering</h3>
                            <p class="mt-2 text-sm leading-6 text-gray-600">SSR, SSG and supported revalidation — pick per page with getServerSideProps, getStaticProps and getStaticPaths.</p>
                            <span class="inline-block mt-4 text-sm font-semibold text-blue-600 group-hover:text-blue-700">Learn more →</span>
                        </Link>

                        <Link href="/documentation/concepts/psx-internals" className="group block p-8 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-xl">
                            <div class="flex items-center justify-center w-12 h-12 text-white bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl shadow-lg">
                                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 22.5 12 13.5H3.75z" />
                                </svg>
                            </div>
                            <h3 class="mt-6 text-lg font-bold text-gray-900">Reactive UI</h3>
                            <p class="mt-2 text-sm leading-6 text-gray-600">Build interactive interfaces with PSX — useState, useEffect and useRef with fine-grained DOM updates.</p>
                            <span class="inline-block mt-4 text-sm font-semibold text-blue-600 group-hover:text-blue-700">Learn more →</span>
                        </Link>

                        <Link href="/documentation/getting-started/layouts-pages" className="group block p-8 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-xl">
                            <div class="flex items-center justify-center w-12 h-12 text-white bg-gradient-to-br from-violet-500 to-violet-600 rounded-xl shadow-lg">
                                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                                </svg>
                            </div>
                            <h3 class="mt-6 text-lg font-bold text-gray-900">Routing</h3>
                            <p class="mt-2 text-sm leading-6 text-gray-600">Organize applications using file-based routing — drop a .py file in pages/ and it's a route.</p>
                            <span class="inline-block mt-4 text-sm font-semibold text-blue-600 group-hover:text-blue-700">Learn more →</span>
                        </Link>

                        <Link href="/documentation/reference/server-actions" className="group block p-8 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-xl">
                            <div class="flex items-center justify-center w-12 h-12 text-white bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg">
                                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
                                </svg>
                            </div>
                            <h3 class="mt-6 text-lg font-bold text-gray-900">Server Actions</h3>
                            <p class="mt-2 text-sm leading-6 text-gray-600">Connect frontend interactions to Python logic — callServerAction with built-in loading and error state.</p>
                            <span class="inline-block mt-4 text-sm font-semibold text-blue-600 group-hover:text-blue-700">Learn more →</span>
                        </Link>

                        <Link href="/documentation/howto/api" className="group block p-8 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-xl">
                            <div class="flex items-center justify-center w-12 h-12 text-white bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl shadow-lg">
                                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 3.75c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
                                </svg>
                            </div>
                            <h3 class="mt-6 text-lg font-bold text-gray-900">API Development</h3>
                            <p class="mt-2 text-sm leading-6 text-gray-600">Build application endpoints in Python — REST APIs under pages/api plus streaming for real-time.</p>
                            <span class="inline-block mt-4 text-sm font-semibold text-blue-600 group-hover:text-blue-700">Learn more →</span>
                        </Link>

                        <Link href="/documentation/howto/database" className="group block p-8 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-xl">
                            <div class="flex items-center justify-center w-12 h-12 text-white bg-gradient-to-br from-rose-500 to-rose-600 rounded-xl shadow-lg">
                                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 3.75c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
                                </svg>
                            </div>
                            <h3 class="mt-6 text-lg font-bold text-gray-900">Data & Auth</h3>
                            <p class="mt-2 text-sm leading-6 text-gray-600">SQLAlchemy models, sessions, and protected routes built in — write queries in Python, render results in PSX.</p>
                            <span class="inline-block mt-4 text-sm font-semibold text-blue-600 group-hover:text-blue-700">Learn more →</span>
                        </Link>

                        <Link href="/documentation" className="group block p-8 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-xl">
                            <div class="flex items-center justify-center w-12 h-12 text-white bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl shadow-lg">
                                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
                                </svg>
                            </div>
                            <h3 class="mt-6 text-lg font-bold text-gray-900">Developer Experience</h3>
                            <p class="mt-2 text-sm leading-6 text-gray-600">CLI, debugging and development tooling — fast iteration with hot reload and error overlays.</p>
                            <span class="inline-block mt-4 text-sm font-semibold text-blue-600 group-hover:text-blue-700">Learn more →</span>
                        </Link>
                    </div>
                </div>
            </section>

            {/* How it works */}
            <section class="py-24 bg-white">
                <div class="px-6 mx-auto max-w-7xl lg:px-8">
                    <div class="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-20 items-center">
                        <div>
                            <p class="text-sm font-semibold tracking-wider text-blue-600 uppercase">How it works</p>
                            <h2 class="mt-3 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">One language. Your entire application.</h2>
                            <p class="mt-4 text-lg text-gray-600">NextPy isn't just a backend framework with HTML templates. It's a complete Python-first development experience.</p>

                            <div class="mt-8 space-y-4">
                                <div class="flex items-start gap-4">
                                    <div class="flex items-center justify-center flex-shrink-0 w-8 h-8 text-white bg-blue-600 font-bold rounded-full">1</div>
                                    <div>
                                        <h3 class="text-lg font-semibold text-gray-900">Write components in Python</h3>
                                        <p class="text-sm text-gray-600">Use PSX markup to create reactive UI components with useState, useEffect and useRef.</p>
                                    </div>
                                </div>
                                <div class="flex items-start gap-4">
                                    <div class="flex items-center justify-center flex-shrink-0 w-8 h-8 text-white bg-blue-600 font-bold rounded-full">2</div>
                                    <div>
                                        <h3 class="text-lg font-semibold text-gray-900">Define routes and layouts</h3>
                                        <p class="text-sm text-gray-600">File-based routing with dynamic segments, layouts and nested pages.</p>
                                    </div>
                                </div>
                                <div class="flex items-start gap-4">
                                    <div class="flex items-center justify-center flex-shrink-0 w-8 h-8 text-white bg-blue-600 font-bold rounded-full">3</div>
                                    <div>
                                        <h3 class="text-lg font-semibold text-gray-900">Fetch and manage data</h3>
                                        <p class="text-sm text-gray-600">getServerSideProps, getStaticProps and SQLAlchemy for data fetching and ORM.</p>
                                    </div>
                                </div>
                                <div class="flex items-start gap-4">
                                    <div class="flex items-center justify-center flex-shrink-0 w-8 h-8 text-white bg-blue-600 font-bold rounded-full">4</div>
                                    <div>
                                        <h3 class="text-lg font-semibold text-gray-900">Render and hydrate</h3>
                                        <p class="text-sm text-gray-600">SSR, SSG and ISR with selective hydration for optimal performance.</p>
                                    </div>
                                </div>
                                <div class="flex items-start gap-4">
                                    <div class="flex items-center justify-center flex-shrink-0 w-8 h-8 text-white bg-blue-600 font-bold rounded-full">5</div>
                                    <div>
                                        <h3 class="text-lg font-semibold text-gray-900">Build and deploy</h3>
                                        <p class="text-sm text-gray-600">nextpy build produces production-ready output for any platform.</p>
                                    </div>
                                </div>
                            </div>

                            <a href="/documentation/tutorials/first-app" className="inline-flex items-center mt-8 text-sm font-semibold text-blue-600 hover:text-blue-700" data-nextpy-link="true" data-nextpy-prefetch="true">Follow the first-app tutorial →</a>
                        </div>

                        <div class="relative">
                            <EnhancedCodeBlock
                                snippet={counter_code}
                                lang="Python"
                                filename="pages/counter.py"
                            />
                        </div>
                    </div>
                </div>
            </section>

            {/* Real Applications */}
            <section class="py-24 bg-gray-50 border-y border-gray-200">
                <div class="px-6 mx-auto max-w-7xl lg:px-8">
                    <div class="max-w-2xl mx-auto lg:text-center">
                        <p class="text-sm font-semibold tracking-wider text-blue-600 uppercase">Built for real applications</p>
                        <h2 class="mt-3 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">Production-ready by design</h2>
                        <p class="mt-4 text-lg text-gray-600">NextPy powers real applications — from SaaS dashboards to AI apps and real-time systems.</p>
                    </div>

                    <div class="grid max-w-5xl grid-cols-1 gap-6 mx-auto mt-16 sm:grid-cols-2 lg:grid-cols-3">
                        <div class="p-8 bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all">
                            <h3 class="text-lg font-bold text-gray-900">SaaS Dashboards</h3>
                            <p class="mt-2 text-sm text-gray-600">Build data-rich dashboards with SQLAlchemy, server actions and reactive components.</p>
                        </div>
                        <div class="p-8 bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all">
                            <h3 class="text-lg font-bold text-gray-900">AI Applications</h3>
                            <p class="mt-2 text-sm text-gray-600">Streaming responses, API routes and server-side logic for AI-powered features.</p>
                        </div>
                        <div class="p-8 bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all">
                            <h3 class="text-lg font-bold text-gray-900">Blogs & Publishing</h3>
                            <p class="mt-2 text-sm text-gray-600">SSG and ISR for fast, SEO-friendly content sites with markdown support.</p>
                        </div>
                        <div class="p-8 bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all">
                            <h3 class="text-lg font-bold text-gray-900">Business Systems</h3>
                            <p class="mt-2 text-sm text-gray-600">CRUD applications with authentication, database ORM and file-based routing.</p>
                        </div>
                        <div class="p-8 bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all">
                            <h3 class="text-lg font-bold text-gray-900">Real-time Apps</h3>
                            <p class="mt-2 text-sm text-gray-600">WebSocket support and streaming for live updates and collaborative features.</p>
                        </div>
                        <div class="p-8 bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all">
                            <h3 class="text-lg font-bold text-gray-900">E-commerce</h3>
                            <p class="mt-2 text-sm text-gray-600">Product catalogs, checkout flows and inventory management in Python.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Developer Experience */}
            <section class="py-24 bg-white">
                <div class="px-6 mx-auto max-w-7xl lg:px-8">
                    <div class="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-20 items-center">
                        <div>
                            <p class="text-sm font-semibold tracking-wider text-blue-600 uppercase">Developer Experience</p>
                            <h2 class="mt-3 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">Get started in seconds</h2>
                            <p class="mt-4 text-lg text-gray-600">Install NextPy and start building immediately. No JavaScript toolchain required.</p>

                            <div class="mt-8 bg-gray-900 border border-gray-800 p-6 font-mono text-sm">
                                <div class="flex items-center justify-between mb-4">
                                    <span class="text-gray-500"># Install</span>
                                    <button class="text-xs text-blue-400 hover:text-blue-300">Copy</button>
                                </div>
                                <p class="text-gray-300"><span class="text-blue-400">$</span> pip install nextpy-framework</p>
                                <div class="mt-4 flex items-center justify-between mb-4">
                                    <span class="text-gray-500"># Create project</span>
                                    <button class="text-xs text-blue-400 hover:text-blue-300">Copy</button>
                                </div>
                                <p class="text-gray-300"><span class="text-blue-400">$</span> nextpy create my-app</p>
                                <div class="mt-4 flex items-center justify-between mb-4">
                                    <span class="text-gray-500"># Run dev server</span>
                                    <button class="text-xs text-blue-400 hover:text-blue-300">Copy</button>
                                </div>
                                <p class="text-gray-300"><span class="text-blue-400">$</span> cd my-app && nextpy dev</p>
                            </div>

                            <p class="mt-4 text-sm text-gray-500">From zero to a running full-stack app in under a minute.</p>
                        </div>

                        <div class="overflow-hidden bg-white border border-gray-200 shadow-2xl">
                            <div class="flex items-center gap-2 px-5 py-3 border-b border-gray-200 bg-gray-50">
                                <span class="w-2.5 h-2.5 bg-red-400"></span>
                                <span class="w-2.5 h-2.5 bg-yellow-400"></span>
                                <span class="w-2.5 h-2.5 bg-green-400"></span>
                                <span class="ml-3 text-xs font-mono text-gray-500">terminal</span>
                            </div>
                            <div class="p-6 space-y-3 font-mono text-sm bg-gray-900">
                                <p class="text-gray-400"># Create a new NextPy project</p>
                                <p class="text-blue-400">$ nextpy create my-app</p>
                                <p class="text-gray-600">✓ Project created successfully</p>
                                <p class="text-blue-400">$ cd my-app && nextpy dev</p>
                                <p class="text-gray-600">✓ Server running at http://localhost:8000</p>
                                <p class="text-gray-400 mt-4"># Hot reload enabled — changes apply instantly</p>
                                <p class="text-blue-400">$ nextpy build</p>
                                <p class="text-gray-600">✓ Production build complete</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Ecosystem */}
            <section class="py-24 bg-gray-50 border-y border-gray-200">
                <div class="px-6 mx-auto max-w-7xl lg:px-8">
                    <div class="max-w-2xl mx-auto lg:text-center">
                        <p class="text-sm font-semibold tracking-wider text-blue-600 uppercase">Ecosystem & Community</p>
                        <h2 class="mt-3 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">Built in the open</h2>
                        <p class="mt-4 text-lg text-gray-600">NextPy is open source and community-driven. Contribute, learn, and build together.</p>
                    </div>

                    <div class="grid max-w-4xl grid-cols-1 gap-6 mx-auto mt-16 sm:grid-cols-2 lg:grid-cols-4">
                        <a href="https://github.com/RAHIMSTUDIOS/nextpy-framework" target="_blank" className="group block p-6 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg text-center">
                            <h3 class="text-lg font-bold text-gray-900">GitHub</h3>
                            <p class="mt-2 text-sm text-gray-600">Source code, issues and pull requests.</p>
                        </a>
                        <Link href="/documentation" className="group block p-6 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg text-center">
                            <h3 class="text-lg font-bold text-gray-900">Documentation</h3>
                            <p class="mt-2 text-sm text-gray-600">Tutorials, guides and API reference.</p>
                        </Link>
                        <Link href="/examples" className="group block p-6 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg text-center">
                            <h3 class="text-lg font-bold text-gray-900">Examples</h3>
                            <p class="mt-2 text-sm text-gray-600">Interactive demos and code samples.</p>
                        </Link>
                        <a href="https://github.com/RAHIMSTUDIOS/nextpy-framework/discussions" target="_blank" className="group block p-6 transition-all bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg text-center">
                            <h3 class="text-lg font-bold text-gray-900">Community</h3>
                            <p class="mt-2 text-sm text-gray-600">Discussions and support.</p>
                        </a>
                    </div>
                </div>
            </section>

            {/* Final CTA */}
            <section class="py-32 bg-gradient-to-b from-blue-50 to-white">
                <div class="px-6 mx-auto max-w-4xl text-center lg:px-8">
                    <h2 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl lg:text-6xl">
                        The web is evolving.<br />
                        <span class="text-blue-600">Build it with Python.</span>
                    </h2>
                    <p class="mt-6 text-lg text-gray-600">Start building your next application with NextPy today.</p>
                    <div class="mt-10 flex flex-wrap items-center justify-center gap-4">
                        <Link href="/documentation" className="bg-blue-600 px-8 py-4 text-base font-semibold text-white transition-colors hover:bg-blue-700 shadow-lg shadow-blue-600/30">
                            Get Started →
                        </Link>
                        <a href="https://github.com/RAHIMSTUDIOS/nextpy-framework" target="_blank" className="border border-gray-300 bg-white px-8 py-4 text-base font-semibold text-gray-700 transition-colors hover:bg-gray-50">
                            Explore GitHub
                        </a>
                    </div>
                </div>
            </section>

        </div>
    )
