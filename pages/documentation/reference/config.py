"""Configuration - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def ConfigAPI():
    env_example = """# .env
APP_NAME="My App"
PORT=8000
DATABASE_URL="sqlite:///./myapp.db"
SECRET_KEY="super-secret"
JWT_SECRET="jwt-secret"
DEBUG=True
NEXTPY_HOT_RELOAD=True"""

    code_example = """from nextpy.config import settings

app_name = settings["app_name"]
port = settings["port"]
db_url = settings["database_url"]"""

    helpers_example = """from nextpy.config import (
    reload_settings,
    get_setting,
    is_development,
    is_production,
)

# Re-read the project's .env and refresh settings in place
reload_settings()

# Read a single key with an optional fallback
log_level = get_setting("nextpy_log_level", "info")

# Environment helpers
if is_development():
    ...
if is_production():
    ..."""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Reference API</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Configuration</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Configuration</h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy configuration lives in a <code class="font-mono text-sm">.env</code> file and is exposed through <code class="font-mono text-sm">nextpy.config.settings</code>.
                    </p>
                </header>

                <div id="env-file" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The .env file</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Every setting can be overridden with an environment variable. Values are read at startup via <code class="font-mono text-xs">python-dotenv</code>; boolean values accept <code class="font-mono text-xs">1</code>, <code class="font-mono text-xs">true</code>, <code class="font-mono text-xs">yes</code>, or <code class="font-mono text-xs">on</code>.
                    </p>
                    <EnhancedCodeBlock lang="bash" filename=".env" snippet={env_example} />
                </div>

                <div id="settings-table" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Settings reference</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Key</th>
                                    <th class="text-left px-4 py-3 font-semibold">Type</th>
                                    <th class="text-left px-4 py-3 font-semibold">Env var</th>
                                    <th class="text-left px-4 py-3 font-semibold">Default</th>
                                    <th class="text-left px-4 py-3 font-semibold">Purpose</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">app_name</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">APP_NAME</td><td class="px-4 py-3 font-mono text-xs">"NextPy App"</td><td class="px-4 py-3">Application display name.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">debug</td><td class="px-4 py-3 font-mono text-xs">bool</td><td class="px-4 py-3 font-mono text-xs">DEBUG</td><td class="px-4 py-3 font-mono text-xs">True</td><td class="px-4 py-3">Verbose errors and debug UI.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">host</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">HOST</td><td class="px-4 py-3 font-mono text-xs">0.0.0.0</td><td class="px-4 py-3">Bind address for the dev server.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">port</td><td class="px-4 py-3 font-mono text-xs">int</td><td class="px-4 py-3 font-mono text-xs">PORT</td><td class="px-4 py-3 font-mono text-xs">5000</td><td class="px-4 py-3">Server port.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">domain</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">DOMAIN</td><td class="px-4 py-3 font-mono text-xs">localhost:5000</td><td class="px-4 py-3">Public domain used for absolute URLs.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">development</td><td class="px-4 py-3 font-mono text-xs">bool</td><td class="px-4 py-3 font-mono text-xs">DEVELOPMENT</td><td class="px-4 py-3 font-mono text-xs">True</td><td class="px-4 py-3">Whether the app runs in development mode (see <code class="font-mono text-xs">is_development()</code>).</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy_debug</td><td class="px-4 py-3 font-mono text-xs">bool</td><td class="px-4 py-3 font-mono text-xs">NEXTPY_DEBUG</td><td class="px-4 py-3 font-mono text-xs">True</td><td class="px-4 py-3">Framework debug overlay.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy_debug_icon</td><td class="px-4 py-3 font-mono text-xs">bool</td><td class="px-4 py-3 font-mono text-xs">NEXTPY_DEBUG_ICON</td><td class="px-4 py-3 font-mono text-xs">True</td><td class="px-4 py-3">Show the NextPy debug icon/widget.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy_hot_reload</td><td class="px-4 py-3 font-mono text-xs">bool</td><td class="px-4 py-3 font-mono text-xs">NEXTPY_HOT_RELOAD</td><td class="px-4 py-3 font-mono text-xs">True</td><td class="px-4 py-3">Reload modules when files change.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy_log_level</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">NEXTPY_LOG_LEVEL</td><td class="px-4 py-3 font-mono text-xs">"info"</td><td class="px-4 py-3">Framework log verbosity (e.g. <code class="font-mono text-xs">debug</code>, <code class="font-mono text-xs">warning</code>).</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">database_url</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">DATABASE_URL</td><td class="px-4 py-3 font-mono text-xs">sqlite:///./nextpy.db</td><td class="px-4 py-3">SQLAlchemy connection string.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">db_echo</td><td class="px-4 py-3 font-mono text-xs">bool</td><td class="px-4 py-3 font-mono text-xs">DB_ECHO</td><td class="px-4 py-3 font-mono text-xs">False</td><td class="px-4 py-3">Log SQL statements.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">secret_key</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">SECRET_KEY</td><td class="px-4 py-3 font-mono text-xs">change-me-in-production</td><td class="px-4 py-3">App secret for sessions.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">jwt_secret</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">JWT_SECRET</td><td class="px-4 py-3 font-mono text-xs">change-me</td><td class="px-4 py-3">JWT signing key for API tokens.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">jwt_algorithm</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">—</td><td class="px-4 py-3 font-mono text-xs">HS256</td><td class="px-4 py-3">JWT signing algorithm (fixed; no env override).</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">jwt_expiration_hours</td><td class="px-4 py-3 font-mono text-xs">int</td><td class="px-4 py-3 font-mono text-xs">JWT_EXPIRATION_HOURS</td><td class="px-4 py-3 font-mono text-xs">24</td><td class="px-4 py-3">Token lifetime in hours.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">session_secret</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">SESSION_SECRET</td><td class="px-4 py-3 font-mono text-xs">change-me</td><td class="px-4 py-3">Secret used for session cookies.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">mail_server</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">MAIL_SERVER</td><td class="px-4 py-3 font-mono text-xs">smtp.gmail.com</td><td class="px-4 py-3">SMTP server for outbound email.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">mail_port</td><td class="px-4 py-3 font-mono text-xs">int</td><td class="px-4 py-3 font-mono text-xs">MAIL_PORT</td><td class="px-4 py-3 font-mono text-xs">587</td><td class="px-4 py-3">SMTP server port.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">mail_username</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">MAIL_USERNAME</td><td class="px-4 py-3 font-mono text-xs">""</td><td class="px-4 py-3">SMTP username.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">mail_password</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">MAIL_PASSWORD</td><td class="px-4 py-3 font-mono text-xs">""</td><td class="px-4 py-3">SMTP password.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">api_key</td><td class="px-4 py-3 font-mono text-xs">str | None</td><td class="px-4 py-3 font-mono text-xs">API_KEY</td><td class="px-4 py-3 font-mono text-xs">None</td><td class="px-4 py-3">General-purpose API key.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">stripe_key</td><td class="px-4 py-3 font-mono text-xs">str | None</td><td class="px-4 py-3 font-mono text-xs">STRIPE_KEY</td><td class="px-4 py-3 font-mono text-xs">None</td><td class="px-4 py-3">Stripe secret key for payments.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">openai_api_key</td><td class="px-4 py-3 font-mono text-xs">str | None</td><td class="px-4 py-3 font-mono text-xs">OPENAI_API_KEY</td><td class="px-4 py-3 font-mono text-xs">None</td><td class="px-4 py-3">OpenAI API key.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">frontend_url</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">FRONTEND_URL</td><td class="px-4 py-3 font-mono text-xs">http://localhost:5000</td><td class="px-4 py-3">Public frontend URL used in links and redirects.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">backend_url</td><td class="px-4 py-3 font-mono text-xs">str</td><td class="px-4 py-3 font-mono text-xs">BACKEND_URL</td><td class="px-4 py-3 font-mono text-xs">http://localhost:5000</td><td class="px-4 py-3">Public backend API URL.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="text-base leading-7 text-zinc-300">
                        Keys without an environment variable (such as <code class="font-mono text-xs">jwt_algorithm</code>) are fixed in the <code class="font-mono text-xs">settings</code> dict and cannot be overridden via <code class="font-mono text-xs">.env</code>.
                    </p>
                </div>

                <div id="accessing" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Accessing settings</h2>
                    <EnhancedCodeBlock lang="python" filename="pages/example.py" snippet={code_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Settings are only available on the server. Never pass secrets into page props or client state.
                    </p>
                </div>

                <div id="helpers" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Helper functions</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy.config</code> also exposes helper functions for reloading settings and checking the environment:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">reload_settings(project_dir=None) -&gt; dict</code> — Reloads the project <code class="font-mono text-xs">.env</code> (with override) and refreshes every key of <code class="font-mono text-xs">settings</code> in place. The CLI calls this before commands that touch the database so values added after import are picked up. Returns the updated <code class="font-mono text-xs">settings</code> dict.</li>
                        <li><code class="font-mono text-xs">get_setting(key, default=None)</code> — Returns <code class="font-mono text-xs">settings[key]</code> or <code class="font-mono text-xs">default</code> if the key is missing.</li>
                        <li><code class="font-mono text-xs">is_development()</code> — Returns <code class="font-mono text-xs">True</code> when the <code class="font-mono text-xs">development</code> setting is enabled.</li>
                        <li><code class="font-mono text-xs">is_production()</code> — Returns <code class="font-mono text-xs">not is_development()</code>.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="app.py" snippet={helpers_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/cli" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                CLI Reference
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
                        <li><a href="#env-file" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The .env file</a></li>
                        <li><a href="#settings-table" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Settings reference</a></li>
                        <li><a href="#accessing" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Accessing settings</a></li>
                        <li><a href="#helpers" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Helper functions</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Configuration - NextPy Docs"}}


default = ConfigAPI
