import json
from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock, CodeTabs, FileTree

# Register components
register_component("EnhancedCodeBlock", EnhancedCodeBlock)
register_component("CodeTabs", CodeTabs)
register_component("FileTree", FileTree)

@component
def ProjectStructure():
    # --- DATA PREPARATION ---
    top_level_app = json.dumps([
        {"name": "pages/", "type": "folder"},
        {"name": "├── about.py", "type": "file"},
        {"name": "├── blog/", "type": "folder"},
        {"name": "├── index.py", "type": "file"},
        {"name": "└── ...", "type": "file"}
    ])
    
    top_level_src = json.dumps([
        {"name": "src/", "type": "folder"},
        {"name": "├── pages/", "type": "folder"},
        {"name": "├── components/", "type": "folder"},
        {"name": "└── ...", "type": "file"}
    ])

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <!-- MAIN CONTENT AREA -->
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">

                <!-- Top Breadcrumb & Actions -->
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Getting Started</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Project Structure</span>
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
                <header id="header">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Project structure and organization
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        This page provides an overview of <strong class="text-white">all</strong> the folder and file conventions in NextPy, and recommendations for organizing your project.
                    </p>
                </header>

                <!-- Section: Folder and file conventions -->
                <div id="folder-and-file-conventions" class="space-y-8 pt-6 border-t border-zinc-800/80">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Folder and file conventions</h2>
                    
                    <!-- Top-level folders -->
                    <div id="top-level-folders" class="space-y-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Top-level folders
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">Top-level folders are used to organize your application's code and static assets.</p>

                        <!-- Visual Diagram -->
                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 grid grid-cols-1 md:grid-cols-2 gap-8 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px]">
                            <FileTree files='{top_level_app}' />
                            <FileTree files='{top_level_src}' />
                        </div>

                        <div class="w-full text-sm border-t border-zinc-800">
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages</span></div>
                                <div class="text-zinc-300">App Router</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">templates</span></div>
                                <div class="text-zinc-300">Jinja2 base templates</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">public</span></div>
                                <div class="text-zinc-300">Static assets to be served</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">src</span></div>
                                <div class="text-zinc-300">Optional application source folder</div>
                            </div>
                        </div>
                    </div>

                    <!-- Top-level files -->
                    <div id="top-level-files" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Top-level files
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">Top-level files are used to configure your application, manage dependencies, run proxy, integrate monitoring tools, and define environment variables.</p>

                        <div class="text-sm font-semibold text-zinc-300 py-2">NextPy</div>
                        <div class="w-full text-sm border-t border-zinc-800">
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-56"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">nextpy.config.py</span></div>
                                <div class="text-zinc-300">Configuration file for NextPy</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-56"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">requirements.txt</span></div>
                                <div class="text-zinc-300">Project dependencies and scripts</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-56"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">instrumentation.py</span></div>
                                <div class="text-zinc-300">OpenTelemetry and Instrumentation file</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-56"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">proxy.py</span></div>
                                <div class="text-zinc-300">NextPy request proxy</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-56"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">.env</span></div>
                                <div class="text-zinc-300">Environment variables (should not be tracked by version control)</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-56"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">.env.local</span></div>
                                <div class="text-zinc-300">Local environment variables (should not be tracked by version control)</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-56"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">.env.production</span></div>
                                <div class="text-zinc-300">Production environment variables (should not be tracked by version control)</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-56"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">.env.development</span></div>
                                <div class="text-zinc-300">Development environment variables (should not be tracked by version control)</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-56"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">.gitignore</span></div>
                                <div class="text-zinc-300">Git files and folders to ignore</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-56"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pyproject.toml</span></div>
                                <div class="text-zinc-300">Configuration file for Python tooling</div>
                            </div>
                        </div>
                    </div>

                    <!-- Routing Files -->
                    <div id="routing-files" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Routing Files
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            Add <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">index.py</span> to expose a route, <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">layout.psx</span> for shared UI such as header, nav, or footer, <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">loading.py</span> for skeletons, <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">error.py</span> for error boundaries, and <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">api.py</span> for APIs.
                        </p>

                        <div class="w-full text-sm border-t border-zinc-800">
                            <div class="border-b border-zinc-800 py-3 flex font-semibold text-white">
                                <div class="w-32">File</div>
                                <div class="w-56">Extensions</div>
                                <div>Description</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">layout</span></div>
                                <div class="w-56 flex gap-2">
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.py</span>
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.psx</span>
                                </div>
                                <div class="text-zinc-300">Layout</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">index</span></div>
                                <div class="w-56 flex gap-2">
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.py</span>
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.psx</span>
                                </div>
                                <div class="text-zinc-300">Page</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">loading</span></div>
                                <div class="w-56 flex gap-2">
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.py</span>
                                </div>
                                <div class="text-zinc-300">Loading UI</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">not-found</span></div>
                                <div class="w-56 flex gap-2">
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.py</span>
                                </div>
                                <div class="text-zinc-300">Not found UI</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">error</span></div>
                                <div class="w-56 flex gap-2">
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.py</span>
                                </div>
                                <div class="text-zinc-300">Error UI</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">global-error</span></div>
                                <div class="w-56 flex gap-2">
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.py</span>
                                </div>
                                <div class="text-zinc-300">Global error UI</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">api</span></div>
                                <div class="w-56 flex gap-2">
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.py</span>
                                </div>
                                <div class="text-zinc-300">API endpoint</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-32"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">template</span></div>
                                <div class="w-56 flex gap-2">
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.py</span>
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.psx</span>
                                </div>
                                <div class="text-zinc-300">Re-rendered layout</div>
                            </div>
                        </div>
                    </div>

                    <!-- Nested routes -->
                    <div id="nested-routes" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Nested routes
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            Folders define URL segments. Nesting folders nests segments. Layouts at any level wrap their child segments. A route becomes public when an <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">index.py</span> or <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">api.py</span> file exists.
                        </p>

                        <div class="w-full text-sm border-t border-zinc-800">
                            <div class="border-b border-zinc-800 py-3 flex font-semibold text-white">
                                <div class="w-64">Path</div>
                                <div class="w-48">URL pattern</div>
                                <div>Notes</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/layout.psx</span></div>
                                <div class="w-48 font-mono text-zinc-400">—</div>
                                <div class="text-zinc-300">Root layout wraps all routes</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/blog/layout.psx</span></div>
                                <div class="w-48 font-mono text-zinc-400">—</div>
                                <div class="text-zinc-300">Wraps /blog and descendants</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/index.py</span></div>
                                <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">/</span></div>
                                <div class="text-zinc-300">Public route</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/blog/index.py</span></div>
                                <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">/blog</span></div>
                                <div class="text-zinc-300">Public route</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/blog/authors/index.py</span></div>
                                <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">/blog/authors</span></div>
                                <div class="text-zinc-300">Public route</div>
                            </div>
                        </div>
                    </div>

                    <!-- Dynamic routes -->
                    <div id="dynamic-routes" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Dynamic routes
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            Parameterize segments with square brackets. Use <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#91;segment&#93;</span> for a single param, <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#91;...segment&#93;</span> for catch-all, and <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#91;&#91;...segment&#93;&#93;</span> for optional catch-all. Access values via the <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">params</span> prop.
                        </p>

                        <div class="w-full text-sm border-t border-zinc-800">
                            <div class="border-b border-zinc-800 py-3 flex font-semibold text-white">
                                <div class="w-64">Path</div>
                                <div>URL pattern</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/blog/&#91;slug&#93;/index.py</span></div>
                                <div><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">/blog/my-first-post</span></div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/shop/&#91;...slug&#93;/index.py</span></div>
                                <div class="flex gap-2">
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">/shop/clothing</span>
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">/shop/clothing/shirts</span>
                                </div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/docs/&#91;&#91;...slug&#93;&#93;/index.py</span></div>
                                <div class="flex gap-2 flex-wrap">
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">/docs</span>
                                    <span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">/docs/layouts-and-pages</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Route groups and private folders -->
                    <div id="route-groups-and-private-folders" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Route groups and private folders
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            Organize code without changing URLs with route groups <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#40;group&#41;</span>, and colocate non-routable files with private folders <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">_folder</span>.
                        </p>

                        <div class="w-full text-sm border-t border-zinc-800">
                            <div class="border-b border-zinc-800 py-3 flex font-semibold text-white">
                                <div class="w-64">Path</div>
                                <div class="w-48">URL pattern</div>
                                <div>Notes</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/&#40;marketing&#41;/index.py</span></div>
                                <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">/</span></div>
                                <div class="text-zinc-300">Group omitted from URL</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/&#40;shop&#41;/cart/index.py</span></div>
                                <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">/cart</span></div>
                                <div class="text-zinc-300">Share layouts within &#40;shop&#41;</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-64"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">pages/blog/_components/Post.py</span></div>
                                <div class="w-48 font-mono text-zinc-400">—</div>
                                <div class="text-zinc-300">Not routable; safe place for UI utilities</div>
                            </div>
                        </div>
                    </div>

                    <!-- Parallel and Intercepted Routes -->
                    <div id="parallel-and-intercepted-routes" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Parallel and Intercepted Routes
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            These features fit specific UI patterns, such as slot-based layouts or modal routing. Use <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">@slot</span> for named slots rendered by a parent layout.
                        </p>

                        <div class="w-full text-sm border-t border-zinc-800">
                            <div class="border-b border-zinc-800 py-3 flex font-semibold text-white">
                                <div class="w-48">Pattern</div>
                                <div class="w-48">Meaning</div>
                                <div>Typical use case</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">@folder</span></div>
                                <div class="w-48 text-zinc-300">Named slot</div>
                                <div class="text-zinc-400">Sidebar + main content</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">&#40;.&#41;folder</span></div>
                                <div class="w-48 text-zinc-300">Intercept same level</div>
                                <div class="text-zinc-400">Preview sibling route in a modal</div>
                            </div>
                            <div class="border-b border-zinc-800 py-4 flex items-center">
                                <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">&#40;..&#41;folder</span></div>
                                <div class="w-48 text-zinc-300">Intercept parent</div>
                                <div class="text-zinc-400">Open a child of the parent as an overlay</div>
                            </div>
                        </div>
                    </div>

                    <!-- Metadata file conventions -->
                    <div id="metadata-file-conventions" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Metadata file conventions
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>

                        <!-- App icons -->
                        <div id="app-icons" class="space-y-4">
                            <h4 class="text-lg font-semibold text-white">App icons</h4>
                            <div class="w-full text-sm border-t border-zinc-800">
                                <div class="border-b border-zinc-800 py-4 flex items-center">
                                    <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">favicon</span></div>
                                    <div class="w-32 flex gap-1"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.ico</span></div>
                                    <div class="text-zinc-300">Favicon file</div>
                                </div>
                                <div class="border-b border-zinc-800 py-4 flex items-center">
                                    <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">icon</span></div>
                                    <div class="w-32 flex gap-1 flex-wrap"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.ico</span><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.jpg</span><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.png</span></div>
                                    <div class="text-zinc-300">App Icon file</div>
                                </div>
                                <div class="border-b border-zinc-800 py-4 flex items-center">
                                    <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">icon</span></div>
                                    <div class="w-32 flex gap-1"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.js</span><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.py</span></div>
                                    <div class="text-zinc-300">Generated App Icon</div>
                                </div>
                            </div>
                        </div>

                        <!-- Open Graph -->
                        <div id="open-graph-and-twitter-images" class="space-y-4 pt-4">
                            <h4 class="text-lg font-semibold text-white">Open Graph and Twitter images</h4>
                            <div class="w-full text-sm border-t border-zinc-800">
                                <div class="border-b border-zinc-800 py-4 flex items-center">
                                    <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">opengraph-image</span></div>
                                    <div class="w-48 flex gap-1"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.jpg</span><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.png</span></div>
                                    <div class="text-zinc-300">Open Graph image file</div>
                                </div>
                                <div class="border-b border-zinc-800 py-4 flex items-center">
                                    <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">twitter-image</span></div>
                                    <div class="w-48 flex gap-1"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.jpg</span><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.png</span></div>
                                    <div class="text-zinc-300">Twitter image file</div>
                                </div>
                            </div>
                        </div>

                        <!-- SEO -->
                        <div id="seo" class="space-y-4 pt-4">
                            <h4 class="text-lg font-semibold text-white">SEO</h4>
                            <div class="w-full text-sm border-t border-zinc-800">
                                <div class="border-b border-zinc-800 py-4 flex items-center">
                                    <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">sitemap</span></div>
                                    <div class="w-32 flex gap-1"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.xml</span></div>
                                    <div class="text-zinc-300">Sitemap file</div>
                                </div>
                                <div class="border-b border-zinc-800 py-4 flex items-center">
                                    <div class="w-48"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-300">robots</span></div>
                                    <div class="w-32 flex gap-1"><span class="bg-zinc-800/60 border border-zinc-700/50 px-2 py-1 rounded text-xs font-mono text-zinc-400">.txt</span></div>
                                    <div class="text-zinc-300">Robots file</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Section: Organizing your project -->
                <div id="organizing-your-project" class="space-y-8 pt-6 border-t border-zinc-800/80">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Organizing your project</h2>
                    <p class="text-base text-zinc-400">
                        NextPy is <strong class="text-white">unopinionated</strong> about how you organize and colocate your project files. But it does provide several features to help you organize your project.
                    </p>

                    <!-- Component hierarchy -->
                    <div id="component-hierarchy" class="space-y-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Component hierarchy
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">The components defined in special files are rendered in a specific hierarchy:</p>
                        <ul class="list-disc pl-6 space-y-2 text-zinc-400">
                            <li><span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">layout.psx</span></li>
                            <li><span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">template.py</span></li>
                            <li><span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">error.py</span> (React error boundary)</li>
                            <li><span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">loading.py</span> (React suspense boundary)</li>
                            <li><span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">not-found.py</span> (React error boundary for "not found" UI)</li>
                            <li><span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">index.py</span> or nested <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">layout.psx</span></li>
                        </ul>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 flex flex-col md:flex-row items-center gap-6 mt-6">
                            <div class="w-full md:w-64">
                                <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-3">
                                    <div class="flex items-center gap-2 text-sm font-mono text-zinc-400 mb-2"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>layout.psx</div>
                                    <div class="flex items-center gap-2 text-sm font-mono text-zinc-500 pl-6"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>template.py</div>
                                    <div class="flex items-center gap-2 text-sm font-mono text-zinc-500 pl-6"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>error.py</div>
                                    <div class="flex items-center gap-2 text-sm font-mono text-zinc-500 pl-6"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>loading.py</div>
                                    <div class="flex items-center gap-2 text-sm font-mono text-zinc-500 pl-6"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>not-found.py</div>
                                    <div class="flex items-center gap-2 text-sm font-mono text-zinc-500 pl-6"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                </div>
                            </div>
                            <div class="hidden md:flex items-center justify-center w-8">
                                <svg class="w-6 h-6 text-zinc-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                            </div>
                            <div class="w-full md:flex-1">
                                <div class="bg-zinc-900 border border-zinc-800 rounded-lg overflow-hidden shadow-xl p-5 font-mono text-sm leading-relaxed text-zinc-300">
                                    <div class="text-blue-400">&lt;Layout&gt;</div>
                                    <div class="pl-4 text-zinc-500">&lt;Template&gt;</div>
                                    <div class="pl-8 text-rose-400">&lt;ErrorBoundary fallback=&#123;&lt;Error /&gt;&#125;&gt;</div>
                                    <div class="pl-12 text-amber-400">&lt;Suspense fallback=&#123;&lt;Loading /&gt;&#125;&gt;</div>
                                    <div class="pl-16 text-rose-400">&lt;ErrorBoundary fallback=&#123;&lt;NotFound /&gt;&#125;&gt;</div>
                                    <div class="pl-20 text-emerald-400">&lt;Page /&gt;</div>
                                    <div class="pl-16 text-rose-400">&lt;/ErrorBoundary&gt;</div>
                                    <div class="pl-12 text-amber-400">&lt;/Suspense&gt;</div>
                                    <div class="pl-8 text-rose-400">&lt;/ErrorBoundary&gt;</div>
                                    <div class="pl-4 text-zinc-500">&lt;/Template&gt;</div>
                                    <div class="text-blue-400">&lt;/Layout&gt;</div>
                                </div>
                            </div>
                        </div>
                        <p class="text-base text-zinc-400 mt-4">
                            The components are rendered recursively in nested routes, meaning the components of a route segment will be nested <strong>inside</strong> the components of its parent segment.
                        </p>
                    </div>

                    <!-- Colocation -->
                    <div id="colocation" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Colocation
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            In the <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">pages</span> directory, nested folders define route structure. Each folder represents a route segment that is mapped to a corresponding segment in a URL path.
                        </p>
                        <p class="text-base text-zinc-400 mt-4">
                            However, even though route structure is defined through folders, a route is <strong>not publicly accessible</strong> until an <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">index.py</span> or <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">api.py</span> file is added to a route segment.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 overflow-x-auto mt-6">
                            <div class="w-56 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>dashboard</div>
                                    <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>settings</div>
                                    <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>api</div>
                                </div>
                            </div>
                            <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                            <div class="space-y-2 shrink-0">
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/dashboard</div>
                                    <span class="px-2 py-0.5 rounded-full bg-red-900/30 text-red-400 border border-red-900/50 text-[10px] font-bold uppercase tracking-wider">Not Routable</span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/dashboard/settings</div>
                                    <span class="px-2 py-0.5 rounded-full bg-red-900/30 text-red-400 border border-red-900/50 text-[10px] font-bold uppercase tracking-wider">Not Routable</span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/api</div>
                                    <span class="px-2 py-0.5 rounded-full bg-red-900/30 text-red-400 border border-red-900/50 text-[10px] font-bold uppercase tracking-wider">Not Routable</span>
                                </div>
                            </div>
                        </div>

                        <p class="text-base text-zinc-400 mt-4">
                            And, even when a route is made publicly accessible, only the <strong>content returned</strong> by <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">index.py</span> or <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">api.py</span> is sent to the client.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 overflow-x-auto mt-6">
                            <div class="w-56 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>dashboard</div>
                                    <div class="flex items-center gap-2 pl-4 text-emerald-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                    <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>api</div>
                                    <div class="flex items-center gap-2 pl-4 text-emerald-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>users.py</div>
                                </div>
                            </div>
                            <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                            <div class="space-y-2 shrink-0">
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/dashboard</div>
                                    <span class="px-2 py-0.5 rounded-full bg-emerald-900/30 text-emerald-400 border border-emerald-900/50 text-[10px] font-bold uppercase tracking-wider">Routable</span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/api/users</div>
                                    <span class="px-2 py-0.5 rounded-full bg-emerald-900/30 text-emerald-400 border border-emerald-900/50 text-[10px] font-bold uppercase tracking-wider">Routable</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Private folders -->
                    <div id="private-folders" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Private folders
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            Private folders can be created by prefixing a folder with an underscore: <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">_folderName</span>
                        </p>
                        <p class="text-base text-zinc-400 mt-4">
                            This indicates the folder is a private implementation detail and should not be considered by the routing system, thereby <strong>opting the folder and all its subfolders</strong> out of routing.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 overflow-x-auto mt-6">
                            <div class="w-64 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>dashboard</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2 text-zinc-500"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>_components</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>button.py</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>...</div>
                                    <div class="flex items-center gap-2 text-zinc-500"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>_lib</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>format-date.py</div>
                                    <div class="flex items-center gap-2 text-emerald-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                </div>
                            </div>
                            <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                            <div class="space-y-2 shrink-0">
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/dashboard/_lib</div>
                                    <span class="px-2 py-0.5 rounded-full bg-red-900/30 text-red-400 border border-red-900/50 text-[10px] font-bold uppercase tracking-wider">Not Routable</span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/dashboard</div>
                                    <span class="px-2 py-0.5 rounded-full bg-emerald-900/30 text-emerald-400 border border-emerald-900/50 text-[10px] font-bold uppercase tracking-wider">Routable</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Route groups -->
                    <div id="route-groups" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Route groups
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            Route groups can be created by wrapping a folder in parenthesis: <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#40;folderName&#41;</span>
                        </p>
                        <p class="text-base text-zinc-400 mt-4">
                            This indicates the folder is for organizational purposes and should <strong>not be included</strong> in the route's URL path.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 overflow-x-auto mt-6">
                            <div class="w-64 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>&#40;admin&#41;</div>
                                    <div class="flex items-center gap-2 pl-4"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>dashboard</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                    <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>&#40;marketing&#41;</div>
                                    <div class="flex items-center gap-2 pl-4"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>about</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                </div>
                            </div>
                            <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                            <div class="space-y-2 shrink-0">
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/dashboard</div>
                                </div>
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/about</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- src folder -->
                    <div id="src-folder" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-lg font-mono border border-zinc-700/50">src</span> folder
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            NextPy supports storing application code including <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">pages</span> inside an optional <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">src</span> folder. This separates application code from project configuration files which mostly live in the root of a project.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 overflow-x-auto mt-6">
                            <div class="w-64 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>your-project</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>src</div>
                                    <div class="flex items-center gap-2 pl-4"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                    <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>requirements.txt</div>
                                    <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>nextpy.config.py</div>
                                </div>
                            </div>
                            <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                            <div class="flex items-center gap-2 bg-zinc-800/50 border border-zinc-700/50 rounded-md px-4 py-2 font-mono text-sm text-zinc-300 shrink-0">
                                <svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                                /
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Section: Examples -->
                <div id="examples" class="space-y-8 pt-6 border-t border-zinc-800/80">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Examples</h2>
                    <p class="text-base text-zinc-400">
                        The following section lists a very high-level overview of common strategies. The simplest takeaway is to choose a strategy that works for you and your team and be consistent across the project.
                    </p>
                    
                    <div class="p-4 rounded-xl border border-zinc-800 bg-zinc-900/30 flex gap-3 text-sm text-zinc-400 mt-6">
                        <svg class="w-5 h-5 text-zinc-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        <div class="space-y-2">
                            <strong class="text-white font-medium">Good to know:</strong>
                            <p>In our examples below, we're using <code class="text-zinc-200 font-mono text-xs px-1 py-0.5 rounded bg-zinc-900 border border-zinc-800">components</code> and <code class="text-zinc-200 font-mono text-xs px-1 py-0.5 rounded bg-zinc-900 border border-zinc-800">lib</code> folders as generalized placeholders, their naming has no special framework significance and your projects might use other folders like <code class="text-zinc-200 font-mono text-xs px-1 py-0.5 rounded bg-zinc-900 border border-zinc-800">ui</code>, <code class="text-zinc-200 font-mono text-xs px-1 py-0.5 rounded bg-zinc-900 border border-zinc-800">utils</code>, <code class="text-zinc-200 font-mono text-xs px-1 py-0.5 rounded bg-zinc-900 border border-zinc-800">hooks</code>, <code class="text-zinc-200 font-mono text-xs px-1 py-0.5 rounded bg-zinc-900 border border-zinc-800">styles</code>, etc.</p>
                        </div>
                    </div>

                    <!-- Store project files outside of app -->
                    <div id="store-project-files-outside-of-app" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Store project files outside of <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-lg font-mono border border-zinc-700/50">pages</span>
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            This strategy stores all application code in shared folders in the <strong>root of your project</strong> and keeps the <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">pages</span> directory purely for routing purposes.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center mt-6">
                            <div class="w-64 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>your-project</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2 text-zinc-300"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>components</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>...</div>
                                    <div class="flex items-center gap-2 text-zinc-300"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>lib</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>...</div>
                                    <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>dashboard</div>
                                    <div class="flex items-center gap-2 pl-12"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Store project files in top-level folders inside of app -->
                    <div id="store-project-files-in-top-level-folders-inside-of-app" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Store project files in top-level folders inside of <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-lg font-mono border border-zinc-700/50">pages</span>
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            This strategy stores all application code in shared folders in the <strong>root of the <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">pages</span> directory</strong>.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center mt-6">
                            <div class="w-64 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>your-project</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                                    <div class="flex items-center gap-2 pl-4 text-zinc-300"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>components</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>...</div>
                                    <div class="flex items-center gap-2 pl-4 text-zinc-300"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>lib</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>...</div>
                                    <div class="flex items-center gap-2 pl-4"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>dashboard</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                    <div class="flex items-center gap-2 pl-4"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Split project files by feature or route -->
                    <div id="split-project-files-by-feature-or-route" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Split project files by feature or route
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            This strategy stores globally shared application code in the root <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">pages</span> directory and <strong>splits</strong> more specific application code into the route segments that use them.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center mt-6">
                            <div class="w-64 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>your-project</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                                    <div class="flex items-center gap-2 pl-4 text-zinc-300"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>components</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>...</div>
                                    <div class="flex items-center gap-2 pl-4 text-zinc-300"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>lib</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>...</div>
                                    <div class="flex items-center gap-2 pl-4"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>dashboard</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                    <div class="flex items-center gap-2 pl-4"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Organize routes without affecting the URL path -->
                    <div id="organize-routes-without-affecting-the-url-path" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Organize routes without affecting the URL path
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            To organize routes without affecting the URL, create a group to keep related routes together. The folders in parenthesis will be omitted from the URL <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#40;marketing&#41;</span> or <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#40;shop&#41;</span>.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 overflow-x-auto mt-6">
                            <div class="w-64 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2 text-zinc-500"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                    <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>&#40;marketing&#41;</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>about</div>
                                    <div class="flex items-center gap-2 pl-12"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                    <div class="flex items-center gap-2 pl-4"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>blog</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                    <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>&#40;shop&#41;</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>account</div>
                                    <div class="flex items-center gap-2 pl-12"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                </div>
                            </div>
                            <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                            <div class="space-y-2 shrink-0">
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/about</div>
                                </div>
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/blog</div>
                                </div>
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/account</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Opting specific segments into a layout -->
                    <div id="opting-specific-segments-into-a-layout" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Opting specific segments into a layout
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            To opt specific routes into a layout, create a new route group <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#40;shop&#41;</span> and move the routes that share the same layout into the group <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">account</span> and <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">cart</span>. The routes outside of the group will not share the layout <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">checkout</span>.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 overflow-x-auto mt-6">
                            <div class="w-64 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2 text-zinc-500"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                    <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>&#40;shop&#41;</div>
                                    <div class="flex items-center gap-2 pl-8 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>account</div>
                                    <div class="flex items-center gap-2 pl-12"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>cart</div>
                                    <div class="flex items-center gap-2 pl-12"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                    <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>checkout</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                </div>
                            </div>
                            <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                            <div class="space-y-2 shrink-0">
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/account</div>
                                </div>
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/cart</div>
                                </div>
                                <div class="flex items-center gap-3">
                                    <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/checkout</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Opting for loading skeletons on a specific route -->
                    <div id="opting-for-loading-skeletons-on-a-specific-route" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Opting for loading skeletons on a specific route
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            To apply a loading skeleton via a <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">loading.py</span> file to a specific route, create a new route group <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#40;overview&#41;</span> and then move your <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">loading.py</span> inside that route group.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center mt-6">
                            <div class="w-64 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>dashboard</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2 text-zinc-500"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>&#40;overview&#41;</div>
                                    <div class="flex items-center gap-2 pl-8 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>loading.py</div>
                                    <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Creating multiple root layouts -->
                    <div id="creating-multiple-root-layouts" class="space-y-6 pt-6">
                        <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                            Creating multiple root layouts
                            <svg class="w-4 h-4 text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                        </h3>
                        <p class="text-base text-zinc-400">
                            To create multiple root layouts, remove the top-level <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">layout.psx</span> file, and add a <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">layout.psx</span> file inside each route group. This is useful for partitioning an application into sections that have a completely different UI or experience. The <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&lt;html&gt;</span> and <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&lt;body&gt;</span> tags need to be added to each root layout.
                        </p>

                        <div class="p-8 rounded-xl border border-zinc-800 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 overflow-x-auto mt-6">
                            <div class="w-64 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                                <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                                <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                    <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>&#40;marketing&#41;</div>
                                    <div class="flex items-center gap-2 pl-8 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>...</div>
                                    <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>&#40;shop&#41;</div>
                                    <div class="flex items-center gap-2 pl-8 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                    <div class="flex items-center gap-2 pl-8 text-zinc-600"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>...</div>
                                </div>
                            </div>
                        </div>

                        <p class="text-base text-zinc-400 mt-4">
                            In the example above, both <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#40;marketing&#41;</span> and <span class="bg-zinc-800/50 text-zinc-200 px-1.5 py-0.5 rounded text-sm font-mono border border-zinc-700/50">&#40;shop&#41;</span> have their own root layout.
                        </p>
                    </div>
                </div>

                <div class="text-sm text-zinc-500 mt-8">
                    Last updated July 21, 2026
                </div>

                <!-- Footer Pagination -->
                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/getting-started/installation" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Installation
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/layouts-pages" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Layouts and Pages
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                            </span>
                        </Link>
                    </div>
                </footer>
            </article>

            <!-- RIGHT SIDEBAR (ON THIS PAGE) -->
            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-4 pl-8 pb-24 h-[calc(100vh-6rem)] overflow-y-auto scrollbar-none">
                <div class="text-sm">
                    <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                    
                    <ul class="space-y-2.5 font-medium text-zinc-400 border-l border-zinc-800">
                        <!-- Main section -->
                        <li>
                            <a href="#folder-and-file-conventions" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors font-semibold text-zinc-300">Folder and file conventions</a>
                            
                            <!-- Sub-items -->
                            <ul class="space-y-2 mt-2 mb-4">
                                <li><a href="#top-level-folders" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Top-level folders</a></li>
                                <li><a href="#top-level-files" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Top-level files</a></li>
                                <li><a href="#routing-files" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Routing Files</a></li>
                                <li><a href="#nested-routes" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Nested routes</a></li>
                                <li><a href="#dynamic-routes" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Dynamic routes</a></li>
                                <li><a href="#route-groups-and-private-folders" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px] leading-snug">Route groups and private folders</a></li>
                                <li><a href="#parallel-and-intercepted-routes" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px] leading-snug">Parallel and Intercepted Routes</a></li>
                               
                            </ul>
                        </li>

                        <!-- Main section -->
                        <li>
                            <a href="#organizing-your-project" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors font-semibold text-zinc-300">Organizing your project</a>
                            <ul class="space-y-2 mt-2 mb-4">
                                <li><a href="#component-hierarchy" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Component hierarchy</a></li>
                                <li><a href="#colocation" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Colocation</a></li>
                                <li><a href="#private-folders" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Private folders</a></li>
                                <li><a href="#route-groups" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Route groups</a></li>
                                <li><a href="#src-folder" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">src folder</a></li>
                            </ul>
                        </li>

                        <!-- Main section -->
                        <li>
                            <a href="#examples" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors font-semibold text-zinc-300">Examples</a>
                            <ul class="space-y-2 mt-2">
                                <li><a href="#store-project-files-outside-of-app" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px] leading-snug">Store project files outside of app</a></li>
                                <li><a href="#store-project-files-in-top-level-folders-inside-of-app" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px] leading-snug">Store project files in top-level folders inside of app</a></li>
                                <li><a href="#split-project-files-by-feature-or-route" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px] leading-snug">Split project files by feature or route</a></li>
                                <li><a href="#organize-routes-without-affecting-the-url-path" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px] leading-snug">Organize routes without affecting the URL path</a></li>
                                <li><a href="#opting-specific-segments-into-a-layout" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px] leading-snug">Opting specific segments into a layout</a></li>
                                <li><a href="#opting-for-loading-skeletons-on-a-specific-route" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px] leading-snug">Opting for loading skeletons on a specific route</a></li>
                                <li><a href="#creating-multiple-root-layouts" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px] leading-snug">Creating multiple root layouts</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>

                <!-- Feedback Links -->
                <div class="pt-8 mt-8 border-t border-zinc-800/80 text-sm font-medium space-y-4">
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
            "title": "Project Structure",
        }
    }

default = ProjectStructure

