"""NextPy vs Other Python Frameworks - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def NextPyVsPythonFrameworks():
    overview_example = '''from nextpy.psx import component

@component
def Page(props):
    # File-based route: pages/dashboard.py -> /dashboard
    # Server-rendered Python, hydrated where interactive
    return psx("""
        <h1>Dashboard</h1>
        <MetricCards stats={props["stats"]} />
        <Counter />
    """)'''

    quickstart = '''# Single CLI for the whole lifecycle
$ nextpy dev      # development server with hot reload
$ nextpy build    # production build + static export
$ nextpy start    # run the production server'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Core Concepts</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">NextPy vs Python Frameworks</span>
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
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">NextPy vs Other Python Frameworks</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Python has no shortage of web frameworks — but most were designed for one layer of the stack. NextPy is a full-stack framework: file-based routing, server and client rendering, interactive components, and a built-in backend, all in one Python project. This page compares it honestly against the five frameworks people most often ask about.
                    </p>
                </header>

                <div id="at-a-glance" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">At a glance</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy sits in a different category than most Python web frameworks. Where Flask and FastAPI are primarily backend toolkits and Streamlit is a data-app tool, NextPy targets the same product as Next.js — a complete application framework — with Python as the authoring language:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={overview_example} />
                    <EnhancedCodeBlock lang="bash" filename="terminal" snippet={quickstart} />
                </div>

                <div id="comparison-table" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Detailed comparison</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/80">
                        <table class="w-full text-sm min-w-[720px]">
                            <thead class="bg-zinc-900/60 text-zinc-400">
                                <tr>
                                    <th class="text-left px-4 py-2.5 font-medium">Framework</th>
                                    <th class="text-left px-4 py-2.5 font-medium">Language paradigm</th>
                                    <th class="text-left px-4 py-2.5 font-medium">Rendering</th>
                                    <th class="text-left px-4 py-2.5 font-medium">Routing</th>
                                    <th class="text-left px-4 py-2.5 font-medium">Reactivity</th>
                                    <th class="text-left px-4 py-2.5 font-medium">Backend integration</th>
                                    <th class="text-left px-4 py-2.5 font-medium">Best for</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr>
                                    <td class="px-4 py-2.5 font-semibold text-white">NextPy</td>
                                    <td class="px-4 py-2.5">Python (PSX JSX-like syntax)</td>
                                    <td class="px-4 py-2.5">SSR, SSG, ISR, streaming, selective hydration</td>
                                    <td class="px-4 py-2.5">File-based, Next.js-style layouts</td>
                                    <td class="px-4 py-2.5">Fine-grained signals + hooks</td>
                                    <td class="px-4 py-2.5">Built-in: ORM, auth, admin, tasks, websocket, plugins</td>
                                    <td class="px-4 py-2.5">Full-stack Python apps, React-grade UX</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-semibold text-white">Flask</td>
                                    <td class="px-4 py-2.5">Python micro-framework</td>
                                    <td class="px-4 py-2.5">Template-rendered HTML, client JS optional</td>
                                    <td class="px-4 py-2.5">Decorator-based, explicit</td>
                                    <td class="px-4 py-2.5">None built in (pair with Alpine/HTMX/JS)</td>
                                    <td class="px-4 py-2.5">Bring your own: SQLAlchemy, auth libs</td>
                                    <td class="px-4 py-2.5">APIs, small apps, maximum flexibility</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-semibold text-white">FastAPI</td>
                                    <td class="px-4 py-2.5">Python, async-native</td>
                                    <td class="px-4 py-2.5">JSON APIs; HTML via Jinja2 optional</td>
                                    <td class="px-4 py-2.5">Decorator-based, OpenAPI-generated</td>
                                    <td class="px-4 py-2.5">None — pure API layer</td>
                                    <td class="px-4 py-2.5">Pydantic, DI, async first-class</td>
                                    <td class="px-4 py-2.5">APIs, microservices, async backends</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-semibold text-white">Django</td>
                                    <td class="px-4 py-2.5">Python "batteries included"</td>
                                    <td class="px-4 py-2.5">Server-rendered templates (SSR)</td>
                                    <td class="px-4 py-2.5">File-based with app registry</td>
                                    <td class="px-4 py-2.5">None built in (Django + htmx common)</td>
                                    <td class="px-4 py-2.5">ORM, admin, auth, migrations, forms</td>
                                    <td class="px-4 py-2.5">Large content-heavy apps, admin-heavy systems</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-semibold text-white">Streamlit</td>
                                    <td class="px-4 py-2.5">Python scripting model</td>
                                    <td class="px-4 py-2.5">Full-page rerun on every interaction</td>
                                    <td class="px-4 py-2.5">Single script, multipage via files</td>
                                    <td class="px-4 py-2.5">Top-down script reruns</td>
                                    <td class="px-4 py-2.5">Data libraries, caching, sessions</td>
                                    <td class="px-4 py-2.5">Data dashboards and internal tools</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-semibold text-white">Reflex / pynecone</td>
                                    <td class="px-4 py-2.5">Python full-stack (React compiled)</td>
                                    <td class="px-4 py-2.5">Client-side SPA + server state</td>
                                    <td class="px-4 py-2.5">File-based pages + components</td>
                                    <td class="px-4 py-2.5">Reactive vars (compiled to signals)</td>
                                    <td class="px-4 py-2.5">Built-in auth, DB (SQLModel), REST API</td>
                                    <td class="px-4 py-2.5">Python-first web apps, similar niche</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="vs-flask" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">NextPy vs Flask</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Flask is a micro-framework: it gives you routing, request handling, and a template engine, then steps aside. That minimalism is its strength and its limitation.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Where NextPy is stronger:</strong> Flask ships no UI framework, no built-in reactivity, and no data-fetching conventions. Building an interactive page in Flask means choosing and integrating a JS framework yourself. NextPy gives you SSR/SSG/ISR, hydrated interactive components, server actions, auth, an ORM, admin, background tasks, and plugins out of the box — one <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy dev/build/start</code> workflow with no separate frontend toolchain.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Where Flask is stronger:</strong> Flask is smaller, simpler to reason about, and has a decade of extensions and community knowledge. It imposes no structure, so anything Flask can do, you can do — including serving JSON APIs with total control. NextPy's added structure (PSX components, the component router, hydration model) is exactly what you don't want if you're building a thin API or a CLI-adjacent service. Flask also has a vastly larger ecosystem of plugins and Stack Overflow answers.
                    </p>
                </div>

                <div id="vs-fastapi" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">NextPy vs FastAPI</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        FastAPI is the gold standard for Python APIs: async-first, type-annotated, with automatic OpenAPI docs and dependency injection. It does one thing extremely well — expose endpoints — and leaves the frontend to someone else.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Where NextPy is stronger:</strong> FastAPI has no answer for the UI layer. Teams using it typically pair it with React, Vue, or HTMX, duplicating models and auth logic across two codebases. NextPy keeps the API and the interface in one Python project — API routes live alongside pages under <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/api/</code>, and server actions let the UI call backend functions directly without writing REST handlers.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Where FastAPI is stronger:</strong> FastAPI's async model is more mature and flexible. Its dependency injection, background tasks, WebSocket support, and OpenAPI generation are battle-tested at massive scale. NextPy's server is ASGI-based and supports async handlers, but it is opinionated — if you need a pure, high-throughput API service with arbitrary middleware composition and minimal overhead, FastAPI is the better tool. Many teams also use FastAPI as the API layer <em>behind</em> a NextPy-style frontend; the two aren't mutually exclusive.
                    </p>
                </div>

                <div id="vs-django" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">NextPy vs Django</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Django is the heavyweight: ORM with migrations, admin site, auth, forms, i18n, and two decades of production hardening. NextPy borrows Django's "batteries included" philosophy but targets a different era of web development.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Where NextPy is stronger:</strong> Django's UI story is server-rendered templates — capable, but dated compared to modern interactive apps. Adding rich interactivity means reaching for htmx, Django REST Framework + a JS SPA, or Inertia. NextPy renders interactive components natively with fine-grained signals and selective hydration, supports streaming responses, and provides SSR/SSG/ISR semantics that Django only approximates. For a new product where UX polish matters, NextPy gets you there without a second frontend codebase.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Where Django is stronger:</strong> This is the honest gap. Django's migration system, ORM maturity, admin customization, security track record, and ecosystem (DRF, Celery, channels, django-allauth) are unmatched in Python. NextPy's ORM and admin are functional but younger — migrations, complex query patterns, and battle-testing are areas where Django wins today. For large teams, long-lived projects, or apps where the admin panel is a core deliverable, Django remains the safer choice.
                    </p>
                </div>

                <div id="vs-streamlit" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">NextPy vs Streamlit</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Streamlit makes it trivial to turn a Python script into a shareable app — which is precisely why it's popular for data work, and precisely why it isn't a web application framework.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Where NextPy is stronger:</strong> Streamlit reruns your entire script top-to-bottom on every widget interaction — fine for dashboards, painful for real applications. There's no file-based routing model, no SSR/SSG, no fine control over rendering, no URL-addressable application structure, and limited options for production auth or multi-user state. NextPy apps have real routes, real URLs, selective hydration (only interactive islands hydrate), and a full backend — auth, ORM, tasks, websockets — built in.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Where Streamlit is stronger:</strong> For its actual purpose, Streamlit is unbeatable: a data scientist can have a working internal tool in an hour with zero web knowledge. NextPy requires understanding components, routing, and rendering modes. If the deliverable is a quick data exploration dashboard or an internal analytics page, Streamlit is the right tool — don't use NextPy for that.
                    </p>
                </div>

                <div id="vs-reflex" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">NextPy vs Reflex (pynecone)</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        This is the closest comparison — Reflex also compiles Python to a React frontend. The differences are in philosophy and rendering model.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Where NextPy is stronger:</strong> Reflex apps are client-side SPAs that load state from the server; NextPy is a true full-stack framework with server-side rendering, static generation, ISR, streaming, and Next.js-style file conventions (layouts, loading, error boundaries, not-found). NextPy's data-fetching model — <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getStaticProps</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getStaticPaths</code> — gives SEO-critical pages real HTML at request or build time. NextPy also ships a broader backend surface: admin site, background task queue, websocket broadcasting, and a plugin system.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Where Reflex is stronger:</strong> Reflex's reactive state model is arguably more approachable — you define state and the compiler handles the rest, with less ceremony than NextPy's explicit component/hook model. Reflex also has a larger and more active community today, more examples, and a more polished component library. If your priority is rapid iteration on a Python-authored interactive app and you don't need SSR/SSG semantics, Reflex is a legitimate and possibly better choice right now.
                    </p>
                </div>

                <div id="when-to-choose" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">When to choose NextPy</h2>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300">
                        <li><strong>You want a complete product in Python</strong> — pages, API, auth, admin, background jobs, and database in one deployable, without a JavaScript frontend codebase.</li>
                        <li><strong>SEO and performance matter</strong> — you need SSR, SSG, or ISR for public-facing pages, not just a client-rendered SPA.</li>
                        <li><strong>You're coming from Next.js</strong> — file-based routing, layouts, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Link</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Head</code>, data-fetching functions, and server actions all have direct Python equivalents.</li>
                        <li><strong>Interactivity should be surgical</strong> — fine-grained signals and selective hydration mean only the interactive parts of a page ship JavaScript to the browser.</li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">When not to choose NextPy:</strong> pick Django for large, admin-heavy, long-lived applications where its ecosystem and migrations are decisive; pick FastAPI for pure API services; pick Flask for minimal backends; pick Streamlit for quick data dashboards; and evaluate Reflex if your team prefers its state model and you're not sold on NextPy's rendering pipeline yet.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/concepts/why-nextpy" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Why NextPy?
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/concepts/nextpy-vs-nextjs" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                NextPy vs Next.js
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
                        <li><a href="#at-a-glance" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">At a glance</a></li>
                        <li><a href="#comparison-table" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Detailed comparison</a></li>
                        <li><a href="#vs-flask" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">vs Flask</a></li>
                        <li><a href="#vs-fastapi" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">vs FastAPI</a></li>
                        <li><a href="#vs-django" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">vs Django</a></li>
                        <li><a href="#vs-streamlit" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">vs Streamlit</a></li>
                        <li><a href="#vs-reflex" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">vs Reflex</a></li>
                        <li><a href="#when-to-choose" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">When to choose NextPy</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "NextPy vs Python Frameworks - NextPy Docs"}}


default = NextPyVsPythonFrameworks
