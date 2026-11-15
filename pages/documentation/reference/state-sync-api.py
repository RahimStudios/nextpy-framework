"""State Sync API - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def StateSyncApiReference():
    overview_example = '''from nextpy import (
    StateManager, get_state_manager,
    get_state, set_state, update_state, delete_state,
    ServerState, DatabaseState,
)

# All server-side, all async — the global manager is shared
# process-wide and broadcasts changes over the /ws WebSocket.
await set_state("online_users", 42)
count = await get_state("online_users")
await update_state("online_users", lambda n: n + 1)
await delete_state("online_users")'''

    manager_example = '''from nextpy import get_state_manager

manager = get_state_manager()   # process-wide singleton StateManager

# Key-value store with per-key asyncio.Lock serialization
await manager.set("cart:42", {"items": [1, 2, 3]}, broadcast=True)
await manager.get("cart:42", default={})
await manager.delete("cart:42")

# Functional update — runs under the same lock as set()
await manager.update("counter", lambda v: (v or 0) + 1)

# Versioned snapshots (last 100 kept) for sync/debugging
snap = await manager.get_snapshot()          # full state + version
hist = await manager.get_history(limit=10)   # recent StateSnapshots
ver  = manager.get_version()

# Export/import for persistence or migration
blob = await manager.export_state()
await manager.import_state(blob, merge=False)'''

    subscribe_example = '''import asyncio
from nextpy import get_state_manager

manager = get_state_manager()

async def on_change(key, old_value, new_value):
    print(f"{key}: {old_value} -> {new_value}")

# Subscribe to a channel; filters narrow which keys fire the callback
sub_id = await manager.subscribe(
    "orders",
    on_change,
    filters={"key_pattern": "order:.*"},   # or {"keys": ["order:1"]}
)

# ... later
await manager.unsubscribe(sub_id)'''

    serverstate_example = '''from nextpy import ServerState

# React-useState-like facade over a named global key
cart = ServerState("cart:session-1", initial_value=[])

items, setter = await cart.use()     # (value, set function)
await cart.set([1, 2, 3])            # broadcasts + notifies subscribers

# Local (in-process) subscriber callbacks
unsub = cart.subscribe(lambda v: print("cart changed", v))
unsub()'''

    dbstate_example = '''from nextpy import DatabaseState

state = DatabaseState("app_state")   # table name must be a simple SQL identifier
await state.initialize()             # CREATE TABLE IF NOT EXISTS

await state.set("feature_flags", {"dark_mode": True})
flags = await state.get("feature_flags")   # JSON round-trip, in-memory cache
await state.delete("feature_flags")'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>API Reference</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">State Sync API</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">State Sync API</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Server-side key-value state with WebSocket propagation, shipped in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.state_sync</code> and re-exported from top-level <code class="font-mono text-xs">nextpy</code>. This is <strong class="text-white">not</strong> component state &mdash; it is a process-wide store for server actions, API routes, and background jobs that need to share or broadcast values. For component-local state see <Link href="/documentation/howto/state" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">State how-to</Link> and the <Link href="/documentation/concepts/state-model" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">State model concepts</Link> page; for live examples see <Link href="/documentation/howto/realtime" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">Realtime how-to</Link>.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The module centers on <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">StateManager</code>, an async dict-backed store where every key has its own <code class="font-mono text-xs">asyncio.Lock</code>. Writes bump a global version counter, append a <code class="font-mono text-xs">StateSnapshot</code> to a 100-entry history ring, and &mdash; unless <code class="font-mono text-xs">broadcast=False</code> &mdash; push a <code class="font-mono text-xs">STATE_CHANGE</code> message to every connected client through the shared WebSocket manager in <code class="font-mono text-xs">nextpy.websocket</code>.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><strong class="text-white">In-memory only</strong> &mdash; state does not survive restarts; use <code class="font-mono text-xs">DatabaseState</code> for persistence.</li>
                        <li><strong class="text-white">Thread/task safety</strong> &mdash; mutations are serialized per key via <code class="font-mono text-xs">asyncio.Lock</code>; safe across coroutines in one event loop, but the store is a single process-wide instance (not shared across worker processes).</li>
                        <li><strong class="text-white">No TTL</strong> &mdash; keys persist until <code class="font-mono text-xs">delete()</code>; there is no expiry mechanism.</li>
                        <li><strong class="text-white">Broadcast payload</strong> &mdash; <code class="font-mono text-xs">&#123;'type': 'STATE_CHANGE', 'key', 'old_value', 'new_value', 'timestamp', 'version'&#125;</code> sent to all WebSocket clients.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/api/counter.py" snippet={overview_example} />
                </div>

                <div id="manager" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">StateManager</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Instantiate directly for isolated stores, or use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_state_manager()</code> for the process-wide singleton (created lazily on first call).
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Method</th>
                                    <th class="text-left px-4 py-3 font-semibold">Signature</th>
                                    <th class="text-left px-4 py-3 font-semibold">Notes</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">get</td><td class="px-4 py-3 font-mono text-xs">(key, default=None) -&gt; Any</td><td class="px-4 py-3">Plain dict lookup; no lock taken.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">set</td><td class="px-4 py-3 font-mono text-xs">(key, value, broadcast=True)</td><td class="px-4 py-3">Locked write; snapshots, bumps version, broadcasts + notifies subscribers unless broadcast=False.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">update</td><td class="px-4 py-3 font-mono text-xs">(key, updater) -&gt; Any</td><td class="px-4 py-3">Applies <code class="font-mono text-xs">updater(current)</code> and sets the result; always broadcasts.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">delete</td><td class="px-4 py-3 font-mono text-xs">(key, broadcast=True)</td><td class="px-4 py-3">Removes key if present; notifies with new_value=None.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">subscribe</td><td class="px-4 py-3 font-mono text-xs">(channel, callback, filters=None) -&gt; str</td><td class="px-4 py-3">Registers a local callback; returns subscription id <code class="font-mono text-xs">channel_N</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">unsubscribe</td><td class="px-4 py-3 font-mono text-xs">(subscription_id)</td><td class="px-4 py-3">Removes by id; silently ignores malformed ids.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">get_snapshot / get_history / get_version</td><td class="px-4 py-3 font-mono text-xs">(...)</td><td class="px-4 py-3">Versioned <code class="font-mono text-xs">StateSnapshot</code> access; history keeps the last 100 entries.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">export_state / import_state</td><td class="px-4 py-3 font-mono text-xs">(merge=True)</td><td class="px-4 py-3">Serialize/restore the whole store; import can merge or replace.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">get_lock</td><td class="px-4 py-3 font-mono text-xs">(key) -&gt; asyncio.Lock</td><td class="px-4 py-3">Per-key lock, created on demand; useful for custom multi-step mutations.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/api/state.py" snippet={manager_example} />
                </div>

                <div id="channels" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Channels, filters &amp; WebSocket propagation</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Every <code class="font-mono text-xs">set</code>/<code class="font-mono text-xs">delete</code> with <code class="font-mono text-xs">broadcast=True</code> (the default) does two things in <code class="font-mono text-xs">_notify_subscribers</code>: (1) broadcasts a <code class="font-mono text-xs">STATE_CHANGE</code> JSON message to <em>all</em> connected WebSocket clients via <code class="font-mono text-xs">nextpy.websocket.manager.broadcast</code>, and (2) invokes each registered subscription callback. Broadcast failures are caught and printed, so a dead socket never breaks a write.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><strong class="text-white">Channels</strong> are just string labels grouping subscriptions; they do not partition the state itself &mdash; any subscriber on any channel is notified of every change that passes its filters.</li>
                        <li><strong class="text-white">Filters</strong> accept <code class="font-mono text-xs">&#123;'key_pattern': regex&#125;</code> (matched with <code class="font-mono text-xs">re.match</code>) or <code class="font-mono text-xs">&#123;'keys': [...]&#125;</code> (exact membership).</li>
                        <li><strong class="text-white">Callbacks</strong> may be sync or async; they receive <code class="font-mono text-xs">(key, old_value, new_value)</code> and exceptions are logged, not raised.</li>
                        <li><strong class="text-white">Note:</strong> WebSocket clients receive <em>all</em> changes &mdash; per-client filtering must happen client-side; subscription filters only gate server-side callbacks.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/api/notify.py" snippet={subscribe_example} />
                </div>

                <div id="helpers" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Module-level helpers</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_state(key, default=None)</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">set_state(key, value, broadcast=True)</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">update_state(key, updater)</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">delete_state(key, broadcast=True)</code> &mdash; thin async wrappers over the global manager; use these for the common case.</li>
                    </ul>
                </div>

                <div id="server-state" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">ServerState</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        A React-<code class="font-mono text-xs">useState</code>-style facade bound to a named global key. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ServerState(key, initial_value=None)</code> provides <code class="font-mono text-xs">get()</code>, <code class="font-mono text-xs">set(value)</code> (always broadcasts and notifies local subscribers), <code class="font-mono text-xs">subscribe(callback) -&gt; unsubscribe_fn</code>, and <code class="font-mono text-xs">use() -&gt; (value, setter)</code>. Subscriber callbacks are in-process only &mdash; they do not cross the WebSocket.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/cart.py" snippet={serverstate_example} />
                </div>

                <div id="database-state" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">DatabaseState</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Persistent key-value store backed by a SQL table (default <code class="font-mono text-xs">app_state</code> with <code class="font-mono text-xs">key / value TEXT / updated_at</code> columns). Values are JSON-serialized and cached in a per-instance dict on read. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">table_name</code> must match <code class="font-mono text-xs">[A-Za-z_][A-Za-z0-9_]*</code> or construction raises <code class="font-mono text-xs">ValueError</code>. Call <code class="font-mono text-xs">await initialize()</code> once before first use. Methods: <code class="font-mono text-xs">get(key, default)</code>, <code class="font-mono text-xs">set(key, value)</code>, <code class="font-mono text-xs">delete(key)</code> &mdash; all async. No broadcasting or versioning.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/flags.py" snippet={dbstate_example} />
                </div>

                <div id="vs-usestate" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">State Sync vs component useState</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold"></th>
                                    <th class="text-left px-4 py-3 font-semibold">useState (components)</th>
                                    <th class="text-left px-4 py-3 font-semibold">State Sync API</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-semibold text-zinc-200">Scope</td><td class="px-4 py-3">One component instance</td><td class="px-4 py-3">Process-wide, shared by all server code</td></tr>
                                <tr><td class="px-4 py-3 font-semibold text-zinc-200">Sync</td><td class="px-4 py-3">Automatic client&rarr;server state sync per component</td><td class="px-4 py-3">Manual; explicit WebSocket STATE_CHANGE broadcast</td></tr>
                                <tr><td class="px-4 py-3 font-semibold text-zinc-200">Persistence</td><td class="px-4 py-3">In-memory per session</td><td class="px-4 py-3">In-memory; optional via DatabaseState</td></tr>
                                <tr><td class="px-4 py-3 font-semibold text-zinc-200">API style</td><td class="px-4 py-3">React-style hook in components</td><td class="px-4 py-3">Async Python functions/classes in server code</td></tr>
                                <tr><td class="px-4 py-3 font-semibold text-zinc-200">Best for</td><td class="px-4 py-3">UI state: forms, toggles, lists</td><td class="px-4 py-3">Cross-request coordination: presence, counters, feature flags, job progress</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/auth-api" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Authentication API
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/security-api" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Security API
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
                        <li><a href="#manager" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">StateManager</a></li>
                        <li><a href="#channels" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Channels &amp; WebSocket</a></li>
                        <li><a href="#helpers" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Module helpers</a></li>
                        <li><a href="#server-state" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">ServerState</a></li>
                        <li><a href="#database-state" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">DatabaseState</a></li>
                        <li><a href="#vs-usestate" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">vs useState</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "State Sync API - NextPy Docs"}}


default = StateSyncApiReference
