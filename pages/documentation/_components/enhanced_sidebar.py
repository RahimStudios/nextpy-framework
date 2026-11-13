from nextpy.psx import component, psx, Link

@component
def EnhancedSidebar():
    """Enhanced interactive sidebar using collapsible HTML5 sections."""
    return psx("""
        <aside class="w-full space-y-4 text-sm font-medium select-none">
            
            <!-- Tutorials Section -->
            <details class="group/section" open>
                <summary class="flex items-center justify-between list-none py-2 text-zinc-200 hover:text-white cursor-pointer transition-colors">
                    <span class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-zinc-400 group-hover/section:text-zinc-200 transition-colors" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                        Tutorials
                    </span>
                    <svg class="w-3.5 h-3.5 text-zinc-500 group-open/section:rotate-90 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                </summary>
                <ul class="mt-1 space-y-1 border-l border-zinc-800 pl-4 ml-2 text-zinc-400">
                    <li>
                        <Link href="/documentation/tutorials/first-app" className="flex items-center justify-between py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">
                            <span>Your First App</span> <span className="text-[11px] text-zinc-600 font-mono">10m</span>
                        </Link>
                    </li>
                    <li>
                        <Link href="/documentation/tutorials/todo-app" className="flex items-center justify-between py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">
                            <span>Todo App</span> <span className="text-[11px] text-zinc-600 font-mono">30m</span>
                        </Link>
                    </li>
                    <li>
                        <Link href="/documentation/tutorials/blog-app" className="flex items-center justify-between py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">
                            <span>Blog App</span> <span className="text-[11px] text-zinc-600 font-mono">45m</span>
                        </Link>
                    </li>
                    <li>
                        <Link href="/documentation/tutorials/ai-chat" className="flex items-center justify-between py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">
                            <span>AI Chat App</span> <span className="text-[11px] text-zinc-600 font-mono">1h</span>
                        </Link>
                    </li>
                    <li>
                        <Link href="/documentation/tutorials/dashboard" className="flex items-center justify-between py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">
                            <span>Analytics Dashboard</span> <span className="text-[11px] text-zinc-600 font-mono">1.5h</span>
                        </Link>
                    </li>
                </ul>
            </details>

            <!-- Getting Started Section -->
            <details class="group/section" open>
                <summary class="flex items-center justify-between list-none py-2 text-zinc-200 hover:text-white cursor-pointer transition-colors">
                    <span class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-zinc-400 group-hover/section:text-zinc-200 transition-colors" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Getting Started
                    </span>
                    <svg class="w-3.5 h-3.5 text-zinc-500 group-open/section:rotate-90 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                </summary>
                <ul class="mt-1 space-y-1 border-l border-zinc-800 pl-4 ml-2 text-zinc-400">
                    <li><Link href="/documentation/getting-started/installation" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Installation</Link></li>
                    <li><Link href="/documentation/getting-started/project-structure" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Project Structure</Link></li>
                    <li><Link href="/documentation/getting-started/layouts-pages" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Layouts and Pages</Link></li>
                    <li><Link href="/documentation/getting-started/linking" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Linking and Navigation</Link></li>
                    <li><Link href="/documentation/getting-started/fetching-data" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Fetching Data</Link></li>
                    <li><Link href="/documentation/getting-started/caching" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Caching & Revalidation</Link></li>
                    <li><Link href="/documentation/getting-started/error-handling" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Error Handling</Link></li>
                    <li><Link href="/documentation/getting-started/styling" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Styling (Tailwind)</Link></li>
                    <li><Link href="/documentation/getting-started/route-handlers" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Route Handlers</Link></li>
                    <li><Link href="/documentation/getting-started/deploying" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Deploying</Link></li>
                    <li><Link href="/documentation/getting-started/upgrading" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Upgrading to v2</Link></li>
                </ul>
            </details>

            <!-- How-to Guides Section -->
            <details class="group/section">
                <summary class="flex items-center justify-between list-none py-2 text-zinc-200 hover:text-white cursor-pointer transition-colors">
                    <span class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-zinc-400 group-hover/section:text-zinc-200 transition-colors" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                        </svg>
                        How-to Guides
                    </span>
                    <svg class="w-3.5 h-3.5 text-zinc-500 group-open/section:rotate-90 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                </summary>
                <ul class="mt-1 space-y-1 border-l border-zinc-800 pl-4 ml-2 text-zinc-400">
                    <li><Link href="/documentation/howto/auth" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Authentication & Auth Guards</Link></li>
                    <li><Link href="/documentation/howto/database" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Database Management (ORM)</Link></li>
                    <li><Link href="/documentation/howto/api" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">API Development</Link></li>
                    <li><Link href="/documentation/howto/state" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">State Architecture</Link></li>
                    <li><Link href="/documentation/howto/forms" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Forms & Validation</Link></li>
                    <li><Link href="/documentation/howto/fetching" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Adopting Partial Fetching</Link></li>
                    <li><Link href="/documentation/howto/full-stack" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Full Stack Paradigms</Link></li>
                    <li><Link href="/documentation/howto/building" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Production Building</Link></li>
                    <li><Link href="/documentation/howto/public-pages" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Public & Static Pages</Link></li>
                    <li><Link href="/documentation/howto/redirecting" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Redirecting & Rewrites</Link></li>
                    <li><Link href="/documentation/howto/i18n" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Internationalization (i18n)</Link></li>
                    <li><Link href="/documentation/howto/testing" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Testing (Unit & E2E)</Link></li>
                </ul>
            </details>

            <!-- Explanations Section -->
            <details class="group/section">
                <summary class="flex items-center justify-between list-none py-2 text-zinc-200 hover:text-white cursor-pointer transition-colors">
                    <span class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-zinc-400 group-hover/section:text-zinc-200 transition-colors" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        Core Concepts
                    </span>
                    <svg class="w-3.5 h-3.5 text-zinc-500 group-open/section:rotate-90 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                </summary>
                <ul class="mt-1 space-y-1 border-l border-zinc-800 pl-4 ml-2 text-zinc-400">
                    <li><Link href="/documentation/concepts/why-nextpy" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Why NextPy?</Link></li>
                    <li><Link href="/documentation/concepts/psx-internals" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">PSX Core Internals</Link></li>
                    <li><Link href="/documentation/concepts/routing-engine" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Routing Engine</Link></li>
                    <li><Link href="/documentation/concepts/rendering" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Rendering (SSR, SSG, ISR)</Link></li>
                    <li><Link href="/documentation/concepts/state-model" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">State Management Model</Link></li>
                    <li><Link href="/documentation/concepts/compilation" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Compilation Pipeline</Link></li>
                    <li><Link href="/documentation/concepts/security" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Security & Sandboxing</Link></li>
                </ul>
            </details>

            <!-- Reference Section -->
            <details class="group/section">
                <summary class="flex items-center justify-between list-none py-2 text-zinc-200 hover:text-white cursor-pointer transition-colors">
                    <span class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-zinc-400 group-hover/section:text-zinc-200 transition-colors" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                        Reference API
                    </span>
                    <svg class="w-3.5 h-3.5 text-zinc-500 group-open/section:rotate-90 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                </summary>
                <ul class="mt-1 space-y-1 border-l border-zinc-800 pl-4 ml-2 text-zinc-400">
                    <li><Link href="/documentation/reference/cli" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">CLI Engine Commands</Link></li>
                    <li><Link href="/documentation/reference/config" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Configuration (nextpy.config)</Link></li>
                    <li><Link href="/documentation/reference/components" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Built-in Elements</Link></li>
                    <li><Link href="/documentation/reference/hooks" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">State & Hooks</Link></li>
                    <li><Link href="/documentation/reference/data-fetching" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Data Fetching</Link></li>
                    <li><Link href="/documentation/reference/router" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Router API</Link></li>
                    <li><Link href="/documentation/reference/events" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Event System</Link></li>
                    <li><Link href="/documentation/reference/server-actions" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Server Actions</Link></li>
                    <li><Link href="/documentation/reference/metadata" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Metadata & SEO</Link></li>
                    <li><Link href="/documentation/reference/performance" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Performance</Link></li>
                    <li><Link href="/documentation/reference/utils" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">Utility Modules</Link></li>
                    <li><Link href="/documentation/reference/typescript" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-white hover:bg-zinc-800/50 transition-all">TypeScript Integration</Link></li>
                </ul>
            </details>

            <!-- Legacy Content Section -->
            <details class="group/section">
                <summary class="flex items-center justify-between list-none py-2 text-zinc-500 hover:text-zinc-400 cursor-pointer transition-colors">
                    <span class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-zinc-600 group-hover/section:text-zinc-500 transition-colors" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4 4" />
                        </svg>
                        Legacy Docs (v0)
                    </span>
                    <svg class="w-3.5 h-3.5 text-zinc-600 group-open/section:rotate-90 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                </summary>
                <ul class="mt-1 space-y-1 border-l border-zinc-800 pl-4 ml-2 text-zinc-600">
                    <li><Link href="/legacy/installation" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-zinc-400 hover:bg-zinc-900 transition-all">Installation (Old)</Link></li>
                    <li><Link href="/legacy/quickstart" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-zinc-400 hover:bg-zinc-900 transition-all">Quick Start</Link></li>
                    <li><Link href="/legacy/project-architecture" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-zinc-400 hover:bg-zinc-900 transition-all">Project Architecture</Link></li>
                    <li><Link href="/legacy/migration" className="block py-1.5 px-2 -mx-2 rounded-md hover:text-zinc-400 hover:bg-zinc-900 transition-all">Migration Guide</Link></li>
                </ul>
            </details>

        </aside>
    """)