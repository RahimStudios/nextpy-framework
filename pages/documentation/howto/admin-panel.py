"""Auto-Generated Admin Panel - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def AdminPanelGuide():
    setup_example = '''"""main.py — enable the admin panel"""

import nextpy as nx
from nextpy.admin import AdminSite
from nextpy.db import init_db, User, Post

init_db("sqlite:///nextpy.db")

admin_site = AdminSite(title="My App Admin")
admin_site.register(User)
admin_site.register(Post)

app = nx.create_app(
    pages_dir="pages",
    admin_site=admin_site,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)'''

    register_example = '''"""Register models with admin options"""

from nextpy.admin import AdminSite
from nextpy.db import User, Post

admin_site = AdminSite()

admin_site.register(
    Post,
    name="blog-posts",           # URL slug under /admin/blog-posts
    list_display=["id", "title", "author", "created_at"],
    search_fields=["title", "content"],
    list_filter=["author", "is_published"],
)

admin_site.register(User)
admin_site.unregister(Post)      # remove a model later'''

    custom_admin_example = '''"""Using the global admin site + create_app integration"""

from nextpy.admin import admin, register  # pre-built AdminSite instance
from nextpy.db import User, Post

register(User)
register(Post, list_display=["id", "username", "email"])

app = nx.create_app(
    pages_dir="pages",
    admin_site=admin,             # mounted automatically at /admin
)'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Admin Panel</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Auto-Generated Admin Panel
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        Get a Django-style admin interface for your SQLAlchemy models with zero extra code — list, search, filter, create, edit, and delete records from the browser.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy ships a built-in admin site in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.admin</code>. The <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">AdminSite</code> class registers SQLAlchemy declarative models and generates a protected, server-rendered CRUD interface on top of your existing database session. Pass the configured site to <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nx.create_app()</code> via the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">admin_site</code> argument and the routes are mounted automatically.
                    </p>
                </div>

                <div id="enabling" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Enabling the admin</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Instantiate <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">AdminSite</code>, register your models, and hand it to <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">create_app</code>. Models must be SQLAlchemy declarative models — anything else raises a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">TypeError</code> at registration time.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="main.py" snippet={setup_example} />
                </div>

                <div id="registering-models" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Registering models</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">admin_site.register()</code> accepts keyword options that control the generated views. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">list_display</code> picks the columns shown in the table (defaults to all columns), <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">search_fields</code> enables case-insensitive search, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">list_filter</code> renders exact-match filters. Additional options include <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">actions</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">inlines</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">form_fields</code>, and a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">template</code> override.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="main.py" snippet={register_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        If you prefer not to manage an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">AdminSite</code> instance yourself, the module-level <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">admin</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">register()</code> helpers wrap a pre-built site:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="main.py" snippet={custom_admin_example} />
                </div>

                <div id="what-you-get" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">What you get</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Every registered model gets a complete admin experience out of the box:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li>A <strong class="text-white">dashboard</strong> listing all registered models.</li>
                        <li>A <strong class="text-white">list view</strong> with column sorting (click a header to toggle asc/desc), case-insensitive search over <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">search_fields</code>, exact-match filters from <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">list_filter</code>, and pagination (25 records per page by default, adjustable via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">per_page</code> up to 100).</li>
                        <li><strong class="text-white">Bulk actions</strong> — select rows with checkboxes and run a custom action or the built-in bulk delete.</li>
                        <li><strong class="text-white">Create, edit, and delete</strong> forms with type coercion for booleans, numbers, dates, and datetimes.</li>
                        <li><strong class="text-white">JSON endpoints</strong> at <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin/&#123;model&#125;/records</code> (GET/POST) for programmatic access.</li>
                    </ul>
                </div>

                <div id="securing-access" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Securing access</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Every admin route is protected by HTTP Basic authentication. You have two ways to grant access:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li>Set the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NEXTPY_ADMIN_USERNAME</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NEXTPY_ADMIN_PASSWORD</code> environment variables.</li>
                        <li>Or create a superuser with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy createsuperuser</code> — users whose role is <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">superuser</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">admin</code>, or <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">staff</code> can log in with their app credentials.</li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-300">
                        If neither is configured the admin returns <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">503</code>; bad credentials return <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">401</code> with a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">WWW-Authenticate</code> challenge. Optionally call <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">admin_site.set_log_model(...)</code> to record a history of admin actions.
                    </p>
                </div>

                <div id="url-structure" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">URL structure</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The admin router defaults to the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin</code> prefix (changeable via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">AdminSite.mount(app, prefix=...)</code> or by calling <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">admin_site.router(prefix)</code> yourself). Inside that prefix:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin</code> — dashboard.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin/&#123;model&#125;</code> — paginated, searchable list view.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin/&#123;model&#125;/new</code> — create form (GET renders, POST submits).</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin/&#123;model&#125;/&#123;id&#125;</code> — record detail.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin/&#123;model&#125;/&#123;id&#125;/edit</code> — edit form.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin/&#123;model&#125;/&#123;id&#125;/delete</code> — delete (POST).</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin/&#123;model&#125;/bulk-delete</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin/&#123;model&#125;/bulk-action</code> — bulk operations (POST).</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/admin/&#123;model&#125;/records</code> — JSON list/create endpoints.</li>
                    </ul>
                </div>

                <div id="sqlalchemy-models" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">With SQLAlchemy models</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The admin works with any SQLAlchemy declarative model — including the built-in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.db</code> models like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">User</code>, or your own models defined with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">declarative_base()</code>. Primary-key columns and columns with server defaults are read-only in the edit form; everything else is editable. List, create, and delete operations run inside the app's <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_session()</code> context, so the admin shares the same database as the rest of your app.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/realtime" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Real-Time
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/middleware-guide" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Middleware
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
                        <li><a href="#enabling" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Enabling the admin</a></li>
                        <li><a href="#registering-models" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Registering models</a></li>
                        <li><a href="#what-you-get" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What you get</a></li>
                        <li><a href="#securing-access" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Securing access</a></li>
                        <li><a href="#url-structure" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">URL structure</a></li>
                        <li><a href="#sqlalchemy-models" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">With SQLAlchemy models</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Auto-Generated Admin Panel - NextPy Docs"}}

default = AdminPanelGuide
