"""CLI Reference - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def CLIReference():
    cli_snippet_1 = '''# Create a new app
nextpy create my-app

# Start development server
nextpy dev

# Build for production
nextpy build

# Start production server
nextpy start'''

    cli_snippet_2 = '''nextpy create my-app
nextpy create my-app --no-psx
nextpy create my-app --template default'''

    cli_snippet_3 = '''nextpy dev
nextpy dev --port 3000 --host 127.0.0.1
nextpy dev --no-reload --no-debug'''

    cli_snippet_4 = '''nextpy build
nextpy build --out dist
nextpy build --no-minify --no-tree-shake --no-code-split'''

    cli_snippet_5 = '''nextpy start
nextpy start --port 5000 --host 0.0.0.0'''

    cli_snippet_6 = '''nextpy export
nextpy export --out dist'''

    cli_snippet_7 = '''nextpy createsuperuser --username admin --email admin@example.com --password s3cret'''

    cli_snippet_8 = '''nextpy flushdb --username admin --password s3cret --yes'''

    cli_snippet_9 = '''nextpy routes'''

    cli_snippet_10 = '''nextpy version'''

    cli_snippet_11 = '''nextpy info'''

    cli_snippet_12 = '''nextpy generate page about
nextpy generate api users
nextpy generate component navbar'''

    cli_snippet_13 = '''nextpy plugin list'''

    cli_snippet_14 = '''nextpy plugin enable analytics
nextpy plugin enable analytics --disable'''

    cli_snippet_15 = """nextpy plugin configure analytics --config '{"api_key": "sk-123", "enabled": true}'"""

    cli_snippet_16 = '''nextpy plugin load ./my_plugin.py'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Reference API</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">CLI Reference</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        CLI Reference
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        Complete reference for the NextPy command-line interface.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The NextPy CLI provides commands for creating, building, and running your applications.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        Run <code class="font-mono text-xs">nextpy --help</code> to list all commands, or <code class="font-mono text-xs">nextpy &lt;command&gt; --help</code> for per-command options. Every command below documents its full signature, options, and examples.
                    </p>
                </div>

                <div id="commands" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Commands</h2>

                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_1} />
                </div>

                <div id="project-lifecycle" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Project Lifecycle</h2>

                    <h3 id="create" class="text-xl font-semibold text-white">create</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy create &lt;name&gt;</code> scaffolds a new NextPy project directory, installs Node and Python dependencies when possible, builds the Tailwind CSS bundle, and prints next steps.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">--psx / --no-psx</code> — Enable True JSX (PSX) support (default: enabled).</li>
                        <li><code class="font-mono text-xs">--template</code> — Project template to use (default: <code class="font-mono text-xs">default</code>).</li>
                    </ul>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_2} />

                    <h3 id="dev" class="text-xl font-semibold text-white">dev</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy dev</code> starts the development server (uvicorn) with hot reload enabled. It prepares the project, initializes the database, and watches <code class="font-mono text-xs">pages/</code>, <code class="font-mono text-xs">components/</code>, <code class="font-mono text-xs">templates/</code>, <code class="font-mono text-xs">public/</code>, <code class="font-mono text-xs">static/</code>, <code class="font-mono text-xs">styles/</code>, <code class="font-mono text-xs">scripts/</code>, and <code class="font-mono text-xs">.nextpy_framework/</code> for changes.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">--port, -p</code> — Port to run the server on (defaults to the <code class="font-mono text-xs">PORT</code> setting).</li>
                        <li><code class="font-mono text-xs">--host, -h</code> — Host to bind to (defaults to the <code class="font-mono text-xs">HOST</code> setting).</li>
                        <li><code class="font-mono text-xs">--reload / --no-reload</code> — Enable or disable hot reload (default: enabled).</li>
                        <li><code class="font-mono text-xs">--debug / --no-debug</code> — Enable or disable debug mode; sets <code class="font-mono text-xs">DEBUG</code>, <code class="font-mono text-xs">NEXTPY_DEBUG</code>, and <code class="font-mono text-xs">DEVELOPMENT</code> (default: enabled).</li>
                    </ul>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_3} />

                    <h3 id="build" class="text-xl font-semibold text-white">build</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy build</code> compiles the project into static production assets via the <code class="font-mono text-xs">Builder</code>, reporting pages built, assets processed, total size, and optimization stats.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">--out, -o</code> — Output directory for static files (default: <code class="font-mono text-xs">out</code>).</li>
                        <li><code class="font-mono text-xs">--clean / --no-clean</code> — Clean the output directory first (default: enabled).</li>
                        <li><code class="font-mono text-xs">--optimize / --no-optimize</code> — Enable build optimization (default: enabled).</li>
                        <li><code class="font-mono text-xs">--minify / --no-minify</code> — Minify JS/CSS assets (default: enabled).</li>
                        <li><code class="font-mono text-xs">--tree-shake / --no-tree-shake</code> — Enable tree shaking (default: enabled).</li>
                        <li><code class="font-mono text-xs">--code-split / --no-code-split</code> — Enable code splitting (default: enabled).</li>
                    </ul>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_4} />

                    <h3 id="start" class="text-xl font-semibold text-white">start</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy start</code> runs the production server with debug disabled (<code class="font-mono text-xs">DEBUG</code>, <code class="font-mono text-xs">NEXTPY_DEBUG</code>, and <code class="font-mono text-xs">DEVELOPMENT</code> are set to <code class="font-mono text-xs">false</code>) and uvicorn workers &mdash; 1 by default so in-process features (WebSockets, state sync, rate limiting) stay consistent; override with <code class="font-mono text-xs">NEXTPY_WORKERS</code>.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">--port, -p</code> — Port to run the server on (defaults to the <code class="font-mono text-xs">PORT</code> setting).</li>
                        <li><code class="font-mono text-xs">--host, -h</code> — Host to bind to (defaults to the <code class="font-mono text-xs">HOST</code> setting).</li>
                    </ul>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_5} />

                    <h3 id="export" class="text-xl font-semibold text-white">export</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy export</code> exports static files ready for static hosting. It always builds with a clean output directory.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">--out, -o</code> — Output directory for static files (default: <code class="font-mono text-xs">out</code>).</li>
                    </ul>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_6} />
                </div>

                <div id="database" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Database Commands</h2>

                    <h3 id="createsuperuser" class="text-xl font-semibold text-white">createsuperuser</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy createsuperuser</code> creates — or updates, if a user with the same username or email already exists — an admin superuser in the project database. You can sign in with these credentials at <code class="font-mono text-xs">/admin</code>.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">--username</code> — Superuser username (prompted if omitted).</li>
                        <li><code class="font-mono text-xs">--email</code> — Superuser email (prompted if omitted).</li>
                        <li><code class="font-mono text-xs">--password</code> — Superuser password; hidden input with confirmation prompt (prompted if omitted).</li>
                    </ul>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_7} />

                    <h3 id="flushdb" class="text-xl font-semibold text-white">flushdb</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy flushdb</code> drops and recreates every table in the project database. It first verifies that the supplied credentials belong to an active superuser, admin, or staff account.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">--username</code> — Admin username or email (prompted if omitted).</li>
                        <li><code class="font-mono text-xs">--password</code> — Admin password; hidden input (prompted if omitted).</li>
                        <li><code class="font-mono text-xs">--yes, -y</code> — Skip the confirmation prompt.</li>
                    </ul>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_8} />
                </div>

                <div id="inspection" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Inspection Commands</h2>

                    <h3 id="routes" class="text-xl font-semibold text-white">routes</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy routes</code> scans the project and lists every registered page route and API route, including HTTP methods and the source file each route was defined in, followed by a summary of static and dynamic routes.
                    </p>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_9} />

                    <h3 id="version" class="text-xl font-semibold text-white">version</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy version</code> prints the framework version, Python version, architecture (True JSX), available features, developer, license, and repository links.
                    </p>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_10} />

                    <h3 id="info" class="text-xl font-semibold text-white">info</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy info</code> shows comprehensive system information: framework details, feature status (including whether <code class="font-mono text-xs">watchdog</code> is installed for hot reload), project structure checks, and the list of available commands.
                    </p>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_11} />
                </div>

                <div id="generation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Code Generation</h2>

                    <h3 id="generate" class="text-xl font-semibold text-white">generate</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy generate &lt;type&gt; &lt;name&gt;</code> scaffolds new code. The <code class="font-mono text-xs">type</code> argument must be one of <code class="font-mono text-xs">page</code>, <code class="font-mono text-xs">api</code>, or <code class="font-mono text-xs">component</code>.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">page</code> — Creates a new page under <code class="font-mono text-xs">pages/</code>.</li>
                        <li><code class="font-mono text-xs">api</code> — Creates a new API endpoint under <code class="font-mono text-xs">pages/api/</code>.</li>
                        <li><code class="font-mono text-xs">component</code> — Creates a new reusable component.</li>
                    </ul>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_12} />
                </div>

                <div id="plugins" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Plugin Management</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The <code class="font-mono text-xs">nextpy plugin</code> command group manages NextPy plugins. If the plugin system is unavailable, install it with <code class="font-mono text-xs">pip install nextpy[plugins]</code>.
                    </p>

                    <h3 id="plugin-list" class="text-xl font-semibold text-white">plugin list</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy plugin list</code> shows the total, enabled, and disabled plugin counts plus details for each plugin: name, version, priority, dependencies, and enabled status.
                    </p>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_13} />

                    <h3 id="plugin-enable" class="text-xl font-semibold text-white">plugin enable</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy plugin enable &lt;name&gt;</code> enables a plugin by default; pass <code class="font-mono text-xs">--disable</code> to disable it instead.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">--enable / --disable</code> — Enable or disable the plugin (default: enabled).</li>
                    </ul>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_14} />

                    <h3 id="plugin-configure" class="text-xl font-semibold text-white">plugin configure</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy plugin configure &lt;name&gt;</code> applies configuration to a plugin. The configuration is passed as a JSON string via <code class="font-mono text-xs">--config</code>; omit it to apply an empty configuration.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">--config</code> — Plugin configuration as a JSON string.</li>
                    </ul>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_15} />

                    <h3 id="plugin-load" class="text-xl font-semibold text-white">plugin load</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy plugin load &lt;file_path&gt;</code> loads a plugin from a Python file and registers it with the plugin manager, printing its name, version, and priority.
                    </p>
                    <EnhancedCodeBlock lang="bash" snippet={cli_snippet_16} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/concepts/security" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Security & Sandboxing
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/components" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Components API
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
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Overview</a></li>
                        <li><a href="#commands" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Commands</a></li>
                        <li><a href="#create" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">create</a></li>
                        <li><a href="#dev" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">dev</a></li>
                        <li><a href="#build" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">build</a></li>
                        <li><a href="#start" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">start</a></li>
                        <li><a href="#export" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">export</a></li>
                        <li><a href="#createsuperuser" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">createsuperuser</a></li>
                        <li><a href="#flushdb" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">flushdb</a></li>
                        <li><a href="#routes" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">routes</a></li>
                        <li><a href="#version" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">version</a></li>
                        <li><a href="#info" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">info</a></li>
                        <li><a href="#generate" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">generate</a></li>
                        <li><a href="#plugin-list" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">plugin list</a></li>
                        <li><a href="#plugin-enable" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">plugin enable</a></li>
                        <li><a href="#plugin-configure" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">plugin configure</a></li>
                        <li><a href="#plugin-load" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">plugin load</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "CLI Reference - NextPy Docs"}}

default = CLIReference
