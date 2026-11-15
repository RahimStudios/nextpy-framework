"""In-Memory Cache (MemoryCache) - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def CachingReference():
    decorator_example = """from nextpy.cache import cached


@cached(ttl=300, key=lambda user_id: f"profile:{user_id}")
def get_profile(user_id):
    db = get_session()
    return serialize_model(db.get(User, user_id))


# First call hits the DB; repeats return the cached dict
profile = get_profile(42)

# Clear only this function's entries
get_profile.cache_clear()"""

    manual_example = """from nextpy.cache import get_cache, invalidate, make_cache_key

cache = get_cache()

# Manual get/set with TTL in seconds
cache.set("stats:users", {"count": 1200}, ttl=60)
stats = cache.get("stats:users")

# Derive a stable key from arbitrary parts
key = make_cache_key("report", "2024", {"region": "eu"})
cache.set(key, report_data, ttl=3600)

# Invalidate by key prefix — returns number of entries removed
removed = invalidate("stats:")
removed = invalidate("default:pages.index.get_dashboard")"""

    stats_example = """from nextpy.cache import get_cache

cache = get_cache()
print(len(cache))            # current entry count
print(cache.stats.to_dict()) # {'hits': ..., 'misses': ..., 'sets': ..., 'evictions': ..., 'expirations': ...}"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>API Reference</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">In-Memory Cache</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">In-Memory Cache (MemoryCache)</h1>
                    <p class="leading-relaxed text-zinc-300">
                        A small, dependency-free, thread-safe TTL cache in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.cache</code>. It is intentionally in-process: entries live in the worker's memory and are not shared between processes or restarts. Use it for pages, server actions, data loaders, and background jobs that benefit from short-lived memoization.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The module provides a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">MemoryCache</code> class, a process-wide singleton accessed via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_cache()</code>, a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@cached</code> decorator for sync and async functions, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">invalidate()</code> for prefix-based deletion, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">make_cache_key()</code> / <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CacheStats</code> helpers. <code class="font-mono text-xs">MemoryCache</code>, <code class="font-mono text-xs">cached</code>, <code class="font-mono text-xs">get_cache</code>, and <code class="font-mono text-xs">invalidate</code> are re-exported at the top level of <code class="font-mono text-xs">nextpy</code>.
                    </p>
                </div>

                <div id="memorycache" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">MemoryCache</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">MemoryCache(maxsize=2048)</code> stores entries as <code class="font-mono text-xs">(value, expires_at, created_at)</code> tuples guarded by a <code class="font-mono text-xs">threading.RLock</code>. All times are seconds (TTL is relative; <code class="font-mono text-xs">ttl=0</code> expires immediately).
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get(key, default=None) -&gt; Any</code> &mdash; returns the value, or <code class="font-mono text-xs">default</code> if missing/expired. Expired entries are evicted lazily on read.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_entry(key) -&gt; Optional[tuple]</code> &mdash; returns <code class="font-mono text-xs">(value, expires_at, created_at)</code> or <code class="font-mono text-xs">None</code>; useful for inspecting freshness.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">set(key, value, ttl=60) -&gt; None</code> &mdash; stores a value for <code class="font-mono text-xs">ttl</code> seconds. When the cache is at <code class="font-mono text-xs">maxsize</code>, the oldest-created entry is evicted first (FIFO-ish, by creation time).</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">delete(key) -&gt; bool</code> &mdash; removes one entry; returns whether it existed.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">clear(prefix=None) -&gt; int</code> &mdash; removes all entries, or only keys starting with <code class="font-mono text-xs">prefix</code>; returns the count removed.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">cleanup() -&gt; int</code> &mdash; sweeps expired entries eagerly; returns how many were removed.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">stats</code> (property) &mdash; a <code class="font-mono text-xs">CacheStats</code> object; <code class="font-mono text-xs">len(cache)</code> returns the live entry count.</li>
                    </ul>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><strong class="text-white">TTL &amp; max-size semantics</strong> &mdash; entries expire after their TTL but are only physically removed on read, <code class="font-mono text-xs">cleanup()</code>, or capacity eviction. Expired-but-unread entries still count toward <code class="font-mono text-xs">len(cache)</code> until touched.</li>
                        <li><strong class="text-white">Thread-safety</strong> &mdash; all mutating and reading operations take the internal <code class="font-mono text-xs">RLock</code>, so the cache is safe to share across threads within one process. It is not shared across worker processes.</li>
                    </ul>
                </div>

                <div id="get-cache" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">get_cache()</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_cache() -&gt; MemoryCache</code> returns the module-level singleton (<code class="font-mono text-xs">maxsize=2048</code>), also used by the <code class="font-mono text-xs">@cached</code> decorator by default. Create your own <code class="font-mono text-xs">MemoryCache(maxsize=N)</code> instance when you want isolation.
                    </p>
                </div>

                <div id="cached-decorator" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">@cached decorator</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">cached(ttl=60, *, key=None, namespace="default", cache=None)</code> wraps a sync or async function so identical calls return the cached result instead of re-executing.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">ttl</code> &mdash; seconds each result is cached (default <code class="font-mono text-xs">60</code>).</li>
                        <li><code class="font-mono text-xs">key</code> &mdash; optional callable <code class="font-mono text-xs">key(*args, **kwargs) -&gt; str</code> that produces the cache-key suffix; when omitted, the key is a hash of the function's module, qualified name, args, and kwargs via <code class="font-mono text-xs">make_cache_key</code>.</li>
                        <li><code class="font-mono text-xs">namespace</code> &mdash; string prepended to every key (default <code class="font-mono text-xs">"default"</code>), handy for grouping and for <code class="font-mono text-xs">invalidate()</code> prefixes.</li>
                        <li><code class="font-mono text-xs">cache</code> &mdash; optional <code class="font-mono text-xs">MemoryCache</code> instance; defaults to the shared singleton.</li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-300">
                        Results of <code class="font-mono text-xs">None</code> are never cached. The wrapper preserves the function signature (<code class="font-mono text-xs">functools.wraps</code>) and gains a <code class="font-mono text-xs">cache_clear()</code> attribute that deletes all of that function's entries.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/dashboard.py" snippet={decorator_example} />
                </div>

                <div id="invalidation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">invalidate() &amp; stats</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">invalidate(prefix="", cache=None) -&gt; int</code> deletes entries whose keys start with <code class="font-mono text-xs">prefix</code> on the shared cache (or a supplied one) and returns the number removed. An empty prefix clears everything. Because decorated functions namespace their keys as <code class="font-mono text-xs">&lt;namespace&gt;:&lt;module&gt;.&lt;qualname&gt;:...</code>, you can invalidate one function with its prefix — or just call <code class="font-mono text-xs">func.cache_clear()</code>.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">make_cache_key(*parts) -&gt; str</code> builds a stable, bounded key: parts are serialized (JSON for dicts/lists, <code class="font-mono text-xs">repr</code> otherwise) and hashed with SHA-256, truncated to 32 hex chars. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CacheStats</code> tracks <code class="font-mono text-xs">hits</code>, <code class="font-mono text-xs">misses</code>, <code class="font-mono text-xs">sets</code>, <code class="font-mono text-xs">evictions</code>, and <code class="font-mono text-xs">expirations</code>, exposed via <code class="font-mono text-xs">cache.stats.to_dict()</code>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/admin.py" snippet={stats_example} />
                </div>

                <div id="examples" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Manual cache example</h2>
                    <EnhancedCodeBlock lang="python" filename="pages/api/report.py" snippet={manual_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/api-router" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                API Router
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/performance" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Performance
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
                        <li><a href="#memorycache" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">MemoryCache</a></li>
                        <li><a href="#get-cache" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">get_cache()</a></li>
                        <li><a href="#cached-decorator" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">@cached decorator</a></li>
                        <li><a href="#invalidation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">invalidate() &amp; stats</a></li>
                        <li><a href="#examples" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Manual cache example</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "In-Memory Cache - NextPy Docs"}}


default = CachingReference
