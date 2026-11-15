"""NextPy vs Next.js - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def NextPyVsNextJs():
    mapping_example = '''// Next.js (app router)
// app/dashboard/layout.tsx
export default function Layout({ children }) {
    return <div><Sidebar />{children}</div>
}

// app/dashboard/page.tsx
export default async function Page({ params }) {
    const user = await getUser(params.id)
    return <h1>Hello {user.name}</h1>
}'''

    nextpy_example = '''# NextPy — same structure, Python
# pages/dashboard/layout.py
@component
def Layout(props):
    return psx("""
        <div><Sidebar />{props.children}</div>
    """)

# pages/dashboard/page.py
@component
def Page(props):
    user = fetch_user(props["params"]["id"])
    return <h1>Hello {user["name"]}</h1>'''

    migration_snippet = '''# Next.js
import Link from "next/link"
import Head from "next/head"

export default function Post({ post }) {
    return (
        <>
            <Head><title>{post.title}</title></Head>
            <Link href={`/blog/${post.slug}`}>{post.title}</Link>
        </>
    )
}

# NextPy — direct equivalents
from nextpy.psx import component, Link
from nextpy.components.head import Head

@component
def Post(props):
    post = props["post"]
    return (
        <>
            <Head><title>{post["title"]}</title></Head>
            <Link href={"/blog/" + post["slug"]}>{post["title"]}</Link>
        </>
    )'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Core Concepts</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">NextPy vs Next.js</span>
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
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">NextPy vs Next.js</h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy is explicitly a Python answer to Next.js — same architectural ideas (file-based routing, server rendering, data fetching, server actions), different authoring language and runtime. This page maps the concepts one-to-one, then is honest about where Next.js is still ahead.
                    </p>
                </header>

                <div id="shared-model" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The shared mental model</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Both frameworks organize an application as a file tree where paths become URLs, both render HTML on the server for fast first paint and SEO, and both hydrate interactive parts in the browser. If you know the Next.js app router, NextPy's page conventions will feel immediately familiar — layouts nest, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">loading</code>/<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">error</code>/<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">not-found</code> are special files, and dynamic segments like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">[slug]</code> work the same way:
                    </p>
                    <EnhancedCodeBlock lang="tsx" filename="app/dashboard/page.tsx" snippet={mapping_example} />
                    <EnhancedCodeBlock lang="python" filename="pages/dashboard/page.py" snippet={nextpy_example} />
                </div>

                <div id="concept-mapping" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Concept mapping: Next.js → NextPy</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Nearly every Next.js primitive has a Python equivalent in NextPy 5.x:
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/80">
                        <table class="w-full text-sm min-w-[680px]">
                            <thead class="bg-zinc-900/60 text-zinc-400">
                                <tr>
                                    <th class="text-left px-4 py-2.5 font-medium">Next.js</th>
                                    <th class="text-left px-4 py-2.5 font-medium">NextPy</th>
                                    <th class="text-left px-4 py-2.5 font-medium">Notes</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">app/ or pages/ dir</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">pages/</td>
                                    <td class="px-4 py-2.5">Single pages tree; special files map directly</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">layout.tsx / page.tsx</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">layout.py / page.py</td>
                                    <td class="px-4 py-2.5">Nesting, props.children equivalent via PSX children</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">loading.tsx / error.tsx / not-found.tsx</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">loading.py / error.py / not-found.py</td>
                                    <td class="px-4 py-2.5">Special-file conventions supported by the component router</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">Server Components (default)</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">@component</td>
                                    <td class="px-4 py-2.5">Server-rendered Python functions returning PSX</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">"use client" components</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">@interactive_component</td>
                                    <td class="px-4 py-2.5">Hydrates in browser; useState/useEffect/signals</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">getServerSideProps</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">get_server_side_props</td>
                                    <td class="px-4 py-2.5">Runs per request; camelCase also accepted</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">getStaticProps / getStaticPaths</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">get_static_props / get_static_paths</td>
                                    <td class="px-4 py-2.5">Build-time generation; revalidate → ISR</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">next/link</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">Link</td>
                                    <td class="px-4 py-2.5">Client-side nav with prefetch, replace, scroll</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">next/head</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">Head</td>
                                    <td class="px-4 py-2.5">Meta, link, script injection per page</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">"use server" actions</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">@server_action / ServerAction</td>
                                    <td class="px-4 py-2.5">Typed results, schema validation, auth guards</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">middleware.ts</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">middleware.py</td>
                                    <td class="px-4 py-2.5">Auth, cache, CSRF, rate-limit middleware classes</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">revalidate (ISR)</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">revalidate</td>
                                    <td class="px-4 py-2.5">Seconds-based regeneration on static props</td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">Suspense / streaming</td>
                                    <td class="px-4 py-2.5 font-mono text-xs text-blue-400">streaming responses</td>
                                    <td class="px-4 py-2.5">Async chunked HTML streaming built in</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="component-syntax" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Components and navigation in practice</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        JSX becomes PSX — the same tag-based syntax, transpiled by NextPy's preprocessor into Python component calls. Importing <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Link</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Head</code> works almost identically:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/blog/post.py" snippet={migration_snippet} />
                </div>

                <div id="honest-differences" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Honest differences</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The mapping above is real, but the two frameworks are not equivalent. Here is where Next.js is genuinely ahead:
                    </p>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300">
                        <li><strong>Ecosystem maturity.</strong> Next.js has a massive component ecosystem (shadcn/ui, Radix, MUI, thousands of npm packages), years of edge-case fixes, and Vercel's production infrastructure. NextPy's component and plugin ecosystem is far younger.</li>
                        <li><strong>Hosting and edge.</strong> Vercel offers zero-config global deployment, edge runtime, image optimization, and analytics. NextPy deploys as a standard Python ASGI app — you choose your own host, which is more flexible but less turnkey.</li>
                        <li><strong>React's expressiveness.</strong> JSX compiles to real React; the entire React ecosystem (hooks libraries, state managers, animation) is available. NextPy reimplements the model in Python — powerful, but you lose direct access to React internals and the npm universe.</li>
                        <li><strong>Reactivity model.</strong> React re-renders component trees with a virtual DOM diff. NextPy uses fine-grained signals and selective hydration — often more efficient, but a different mental model with fewer documented patterns.</li>
                        <li><strong>Battle-testing.</strong> Next.js powers major production sites at enormous scale. NextPy 5.0 is newer; expect rough edges and rapid evolution.</li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-300">
                        Where NextPy is genuinely ahead or different: backend features are first-class rather than bolted on (ORM, auth, admin site, background tasks, websockets, plugins all ship in the box), there's no Node.js toolchain required for authors, and a single Python codebase covers concerns that in Next.js typically mean API routes plus separate services.
                    </p>
                </div>

                <div id="migration" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Migration notes for Next.js developers</h2>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300">
                        <li><strong>Keep your mental model.</strong> Routes, layouts, loading/error boundaries, and data-fetching functions translate almost one-to-one — start by mapping your <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">app/</code> tree to <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code>.</li>
                        <li><strong>Translate JSX to PSX.</strong> Tag syntax is familiar; expressions move inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> strings or PSX components. Props dictionaries replace JSX props objects.</li>
                        <li><strong>Replace "use client" with @interactive_component</strong> and hooks (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useState</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useEffect</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useMemo</code>) work the same way.</li>
                        <li><strong>Server actions become @server_action</strong> — Python functions with schema validation instead of TS-typed server functions.</li>
                        <li><strong>Watch for Python-isms.</strong> Strings concat instead of template literals, dict access instead of optional chaining, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">None</code> instead of <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">null</code>/<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">undefined</code>.</li>
                        <li><strong>Don't expect 1:1 npm packages.</strong> The component ecosystem is different — evaluate NextPy's built-ins and plugins first.</li>
                    </ul>
                </div>

                <div id="which-to-choose" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Which should you choose?</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Choose Next.js</strong> if your team is invested in TypeScript/React, you need the npm ecosystem, or you want Vercel's managed platform. It is the more mature, more powerful option today.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Choose NextPy</strong> if you want the same full-stack architecture in pure Python — one language from database to UI, no Node.js toolchain for authors, and built-in backend services. It's the right call for Python teams who want modern SSR/SSG apps without learning React.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/concepts/nextpy-vs-python-frameworks" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                NextPy vs Python Frameworks
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/concepts/security" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Security &amp; Sandboxing
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
                        <li><a href="#shared-model" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Shared mental model</a></li>
                        <li><a href="#concept-mapping" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Concept mapping</a></li>
                        <li><a href="#component-syntax" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Components &amp; navigation</a></li>
                        <li><a href="#honest-differences" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Honest differences</a></li>
                        <li><a href="#migration" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Migration notes</a></li>
                        <li><a href="#which-to-choose" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Which to choose</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "NextPy vs Next.js - NextPy Docs"}}


default = NextPyVsNextJs
