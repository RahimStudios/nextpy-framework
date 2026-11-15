from nextpy.psx import component as interactive_component, Link


@interactive_component
def TemplatesPage(props=None):
    props = props or {}
    title = props.get("title", "NextPy Templates")

    return (
        <div class="min-h-screen bg-white">
            <div class="px-4 py-20 bg-gradient-to-br from-blue-50 to-indigo-50">
                <div class="max-w-6xl mx-auto text-center">
                    <h1 class="mb-6 text-5xl font-bold text-transparent md:text-6xl bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text">{title}</h1>
                    <p class="max-w-3xl mx-auto text-xl text-gray-600">
                        Production-shaped starting points for the most common NextPy apps.
                        Every template is plain Python + PSX — clone the pattern, not a black box.
                    </p>
                </div>
            </div>

            <div class="max-w-6xl px-4 py-16 mx-auto">
                <div class="grid gap-8 md:grid-cols-2">

                    <div class="flex flex-col p-8 transition-all bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md hover:border-gray-300">
                        <div class="flex items-center gap-3 mb-4">
                            <span class="px-3 py-1 text-xs font-semibold tracking-wide text-blue-700 uppercase bg-blue-50 rounded-full">SaaS</span>
                            <h2 class="text-2xl font-bold text-gray-900">Full-Stack Starter</h2>
                        </div>
                        <p class="mb-6 leading-7 text-gray-600">Cookie-session auth, ORM models, protected routes, and server actions — the complete `nextpy create` experience.</p>
                        <ul class="flex-1 mb-8 space-y-2">
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Login / Register / Logout</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Protected dashboard</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>CRUD server actions</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>SQLite ORM out of the box</li>
                        </ul>
                        <Link href="/documentation/tutorials/first-app" className="inline-flex items-center justify-center px-5 py-2.5 text-sm font-semibold text-white transition-colors bg-gray-900 rounded-lg hover:bg-gray-800">
                            Read the tutorial →
                        </Link>
                    </div>

                    <div class="flex flex-col p-8 transition-all bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md hover:border-gray-300">
                        <div class="flex items-center gap-3 mb-4">
                            <span class="px-3 py-1 text-xs font-semibold tracking-wide text-blue-700 uppercase bg-blue-50 rounded-full">Content</span>
                            <h2 class="text-2xl font-bold text-gray-900">Blog & CMS</h2>
                        </div>
                        <p class="mb-6 leading-7 text-gray-600">SSR, SSG and ISR rendering with dynamic `[slug]` routes, metadata and SEO helpers.</p>
                        <ul class="flex-1 mb-8 space-y-2">
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>getServerSideProps / getStaticProps</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Dynamic routes + getStaticPaths</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>ISR revalidation</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Sitemap & robots helpers</li>
                        </ul>
                        <Link href="/documentation/tutorials/blog-app" className="inline-flex items-center justify-center px-5 py-2.5 text-sm font-semibold text-white transition-colors bg-gray-900 rounded-lg hover:bg-gray-800">
                            Build a blog →
                        </Link>
                    </div>

                    <div class="flex flex-col p-8 transition-all bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md hover:border-gray-300">
                        <div class="flex items-center gap-3 mb-4">
                            <span class="px-3 py-1 text-xs font-semibold tracking-wide text-blue-700 uppercase bg-blue-50 rounded-full">Data</span>
                            <h2 class="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
                        </div>
                        <p class="mb-6 leading-7 text-gray-600">Reactive PSX state, fine-grained bindings and animated charts updated without full page reloads.</p>
                        <ul class="flex-1 mb-8 space-y-2">
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>useState / useEffect / useRef</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>rAF-batched updates</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Tailwind transitions</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Live data fetching</li>
                        </ul>
                        <Link href="/documentation/tutorials/dashboard" className="inline-flex items-center justify-center px-5 py-2.5 text-sm font-semibold text-white transition-colors bg-gray-900 rounded-lg hover:bg-gray-800">
                            See the tutorial →
                        </Link>
                    </div>

                    <div class="flex flex-col p-8 transition-all bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md hover:border-gray-300">
                        <div class="flex items-center gap-3 mb-4">
                            <span class="px-3 py-1 text-xs font-semibold tracking-wide text-blue-700 uppercase bg-blue-50 rounded-full">AI</span>
                            <h2 class="text-2xl font-bold text-gray-900">AI Chat App</h2>
                        </div>
                        <p class="mb-6 leading-7 text-gray-600">Streaming responses, server actions and optimistic UI for conversational interfaces.</p>
                        <ul class="flex-1 mb-8 space-y-2">
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Streaming route handlers</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Server actions</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Optimistic message state</li>
                            <li class="flex items-start gap-2 text-sm text-gray-600"><svg class="w-4 h-4 mt-0.5 text-blue-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Markdown rendering</li>
                        </ul>
                        <Link href="/documentation/tutorials/ai-chat" className="inline-flex items-center justify-center px-5 py-2.5 text-sm font-semibold text-white transition-colors bg-gray-900 rounded-lg hover:bg-gray-800">
                            Start building →
                        </Link>
                    </div>

                </div>

                <div class="p-8 mt-16 text-center border border-gray-200 rounded-2xl bg-gray-50">
                    <h2 class="mb-3 text-2xl font-bold text-gray-900">Start from the CLI</h2>
                    <p class="mb-6 text-gray-600">`nextpy create myapp` scaffolds the full-stack starter — auth, database, API routes, animations and docs-ready structure included.</p>
                    <pre class="inline-block px-6 py-3 text-sm text-left text-gray-800 bg-gray-900 rounded-lg"><code>pip install nextpy
nextpy create myapp
cd myapp
nextpy run</code></pre>
                </div>
            </div>
        </div>
    )


default = TemplatesPage
