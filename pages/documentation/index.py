from nextpy.psx import component, Link, register_component

@component
def DocumentationPage():
    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <!-- MAIN CONTENT AREA -->
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">

                <!-- Top Breadcrumb & Actions -->
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentations</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Introduction</span>
                    </div>
                    
                    <!-- Copy Page Button -->
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

                <!-- Page Header -->
                <header id="what-is-nextpy" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Welcome to NextPy
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy is a highly optimized Python framework for building modern full-stack web applications.
                        By utilizing pre-compiled structures, it unifies user interfaces, routing patterns, and data persistence models under a single clean execution layer.
                    </p>
                </header>

                <!-- Section: What is NextPy -->
                <div id="" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">
                        What is NextPy?
                    </h2>
                    <div class="space-y-4 text-base leading-7 text-zinc-300">
                        <p>
                            <strong class="text-zinc-200 font-semibold">NextPy bridges the division between Python computation speed and JavaScript-style reactive interfaces.</strong> It abstracts complex configurations away entirely, allowing you to focus on logic orchestration rather than asset scaffolding.
                        </p>
                        <p>
                            Rather than requiring developers to assemble several independent technologies to build a full-stack application, NextPy provides an integrated architecture.

Its inspiration comes from the developer experience of Next.js, but NextPy is built around Python.

The central idea: Bring the developer experience of modern full-stack frameworks to the Python ecosystem.
                        </p>
                        <p>
                            Whether you are structuring isolated microservice routers, building distributed application networks, or crafting real-time AI dashboards, NextPy handles asset optimization, server-side generation workflows, and code delivery pipelines out of the box.
                        </p>
                    </div>
                </div>

                <!-- Section: How to use -->
                <div id="how-to-use" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">
                        How to use the documentation
                    </h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The documentation is structured systematically into distinct segments tailored to your immediate project milestones:
                    </p>
                    
                    <!-- 3-Column Feature Grid -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
                        
                        <!-- Card 1 -->
                        <a href="/documentation/getting-started/installation" class="group block p-6 rounded-xl border border-zinc-800/60 bg-zinc-950/40 hover:bg-zinc-900/60 hover:border-zinc-700 transition-all">
                            <div class="flex items-center gap-3 mb-3">
                                <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400">
                                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                                </div>
                                <h3 class="text-sm font-semibold text-white group-hover:text-blue-400 transition-colors">Getting Started</h3>
                            </div>
                            <p class="text-sm leading-relaxed text-zinc-500 group-hover:text-zinc-400 transition-colors">
                                Step-by-step guides covering rapid component setup, package distribution installations, and sandbox environment assembly.
                            </p>
                        </a>

                        <!-- Card 2 -->
                        <a href="/documentation/guides" class="group block p-6 rounded-xl border border-zinc-800/60 bg-zinc-950/40 hover:bg-zinc-900/60 hover:border-zinc-700 transition-all">
                            <div class="flex items-center gap-3 mb-3">
                                <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
                                </div>
                                <h3 class="text-sm font-semibold text-white group-hover:text-emerald-400 transition-colors">Guides</h3>
                            </div>
                            <p class="text-sm leading-relaxed text-zinc-500 group-hover:text-zinc-400 transition-colors">
                                Deep dives on token-based secure authorization systems, real-time context streaming, state persistence, and performance scaling.
                            </p>
                        </a>

                        <!-- Card 3 -->
                        <a href="/documentation/api-reference" class="group block p-6 rounded-xl border border-zinc-800/60 bg-zinc-950/40 hover:bg-zinc-900/60 hover:border-zinc-700 transition-all">
                            <div class="flex items-center gap-3 mb-3">
                                <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400">
                                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h7"/></svg>
                                </div>
                                <h3 class="text-sm font-semibold text-white group-hover:text-purple-400 transition-colors">API Reference</h3>
                            </div>
                            <p class="text-sm leading-relaxed text-zinc-500 group-hover:text-zinc-400 transition-colors">
                                Rigorous technical signatures, return parameters, configuration flags, and complete shell mapping variables for all core modules.
                            </p>
                        </a>

                    </div>
                </div>

                <!-- Section: Version Handling -->
                <div id="version-handling" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">
                        Version handling
                    </h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy manages dependencies through standard Python tooling. The framework ships with a pre-configured <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">requirements.txt</code> or <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pyproject.toml</code> that pins the core runtime and client library versions to ensure maximum compatibility across your deployment environments.
                    </p>
                </div>

                <!-- Section: Prerequisites -->
                <div id="prerequisites" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">
                        Pre-requisite knowledge
                    </h2>
                    <p class="text-base leading-7 text-zinc-300">
                        While NextPy provides a clean developer abstraction pattern, you will find it beneficial to maintain basic engineering familiarity with these core paradigms:
                    </p>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300 marker:text-zinc-600">
                        <li><strong class="text-zinc-200 font-semibold">Python 3.11+ Programming:</strong> Standard structural objects, async context execution loops, and package manager environments.</li>
                        <li><strong class="text-zinc-200 font-semibold">Component State Trees:</strong> Understanding data distribution flow across nested visualization layouts.</li>
                        <li><strong class="text-zinc-200 font-semibold">Web Basics:</strong> High-level knowledge of request-response operations, network routes, and style grids.</li>
                    </ul>
                </div>

                <!-- Section: Accessibility -->
                <div id="accessibility" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">
                        Accessibility
                    </h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Our reference structures are formatted to conform tightly to clean semantic markup matrices. For optimal audio readout feedback cycles, we suggest relying on modern screen reader applications such as VoiceOver or NVDA.
                    </p>
                </div>

                <!-- Section: Community -->
                <div id="community" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">
                        Join our Community
                    </h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Stuck on an architectural layout configuration or searching for design performance patterns? Reach out to the global development circle on our active tracking boards:
                    </p>
                    <div class="flex flex-wrap gap-6 text-sm font-medium pt-2">
                        <a href="#" class="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors">
                            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"/></svg>
                            GitHub Discussions
                        </a>
                        <a href="#" class="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors">
                            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z"/></svg>
                            Discord Server
                        </a>
                        <a href="#" class="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors">
                            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                            X / Twitter Community
                        </a>
                    </div>
                </div>

                <!-- Section: Next Steps -->
                <div id="next-steps" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">
                        Next Steps
                    </h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Now that you understand the core philosophy of NextPy, you're ready to set up your environment and create your first application.
                    </p>
                </div>

                <!-- Footer Pagination -->
                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <div class="block p-5 rounded-xl border border-zinc-800/30 bg-zinc-950/20 opacity-50 select-none">
                            <span class="block text-xs font-medium text-zinc-600 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-zinc-600 flex items-center gap-1">
                                <svg class="w-4 h-4 text-zinc-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                —
                            </span>
                        </div>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/installation" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Installation
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                            </span>
                        </Link>
                    </div>
                </footer>
            </article>

            <!-- RIGHT SIDEBAR -->
            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-4 pl-8 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
                <div class="text-sm">
                    <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                    <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#what-is-nextpy" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What is NextPy?</a></li>
                        <li><a href="#how-to-use" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">How to use the docs</a></li>
                        <li><a href="#version-handling" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Version handling</a></li>
                        <li><a href="#prerequisites" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Pre-requisite knowledge</a></li>
                        <li><a href="#accessibility" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Accessibility</a></li>
                        <li><a href="#community" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Join our Community</a></li>
                        <li><a href="#next-steps" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Next Steps</a></li>
                    </ul>
                </div>
                <div class="pt-8 mt-8 border-t border-zinc-800/50 text-sm font-medium space-y-4">
                    <a href="#" class="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors">
                        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg>
                        Give feedback
                    </a>
                    <a href="#" class="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors">
                        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                        Edit this page on GitHub
                    </a>
                </div>
            </aside>

        </div>
    )


def getServerSideProps(context):
    return {
        "props": {
            "title": "NextPy Docs",
        }
    }

default = DocumentationPage

