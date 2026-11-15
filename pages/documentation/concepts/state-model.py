"""State Management Model - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def StateModel():
    state_example = """from nextpy.psx import interactive_component, useState

@interactive_component
def Counter():
    [count, setCount] = useState(0)

    def increment():
        setCount(count + 1)

    return (
        <div>
            <p>Count: {count}</p>
            <button onclick={increment}>+1</button>
        </div>
    )"""

    hooks_example = """from nextpy.psx import interactive_component, useState, useReducer, useEffect


def cart_reducer(state, action):
    if action["type"] == "add":
        return {**state, "items": [*state["items"], action["text"]]}
    if action["type"] == "clear":
        return {"items": []}
    return state


@interactive_component
def Cart():
    # useState — [value, setter]; setter accepts values or updater functions
    [coupon, setCoupon] = useState("")

    # useReducer — [state, dispatch]; actions flow through your reducer
    [cart, dispatch] = useReducer(cart_reducer, {"items": []})

    def add_item():
        dispatch({"type": "add", "text": coupon})
        setCoupon("")

    def log_cart():
        print("cart:", cart["items"])

    # useEffect(effect, deps) — runs when deps change; deps=None runs every render
    useEffect(log_cart, [cart])

    return (
        <div>
            <p>Items: {len(cart["items"])}</p>
            <button onclick={add_item}>Add</button>
        </div>
    )"""

    server_example = """from nextpy.psx import interactive_component, useState, useEffect, callServerAction

@interactive_component
def TodoForm():
    [title, setTitle] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def submit(e):
        e.preventDefault()
        callServerAction("create_todo", {"title": title})

    def handle_result():
        if _server_result and _server_result.get("success"):
            setTitle("")

    useEffect(handle_result, [_server_result])"""

    manager_example = """import asyncio
from nextpy.state_sync import (
    get_state_manager, get_state, set_state, update_state, delete_state,
)

manager = get_state_manager()          # process-wide StateManager singleton

# Convenience helpers — all async, all broadcast by default
await set_state("game:score", 42)                  # broadcast=True
await update_state("game:score", lambda s: s + 1)  # atomic-ish via per-key lock
await get_state("game:score", default=0)
await delete_state("game:score")

# Direct manager API
async with manager.get_lock("game:score"):         # per-key asyncio.Lock
    pass

value = await manager.get("game:score")
await manager.set("game:score", 43, broadcast=False)  # silent write
snap = await manager.get_snapshot()                # {"state": ..., "version": N}
history = await manager.get_history(limit=10)      # last 10 StateSnapshots
version = manager.get_version()
blob = await manager.export_state()                # {"state", "version", "timestamp"}
await manager.import_state(blob, merge=True)       # or merge=False to replace

# Subscriptions — server-side callbacks + websocket broadcast
sub_id = await manager.subscribe(
    "leaderboard",
    lambda key, old, new: print(key, old, "->", new),
    filters={"key_pattern": r"^game:"},            # or &#123;"keys": [...]&#125;
)
await manager.unsubscribe(sub_id)"""

    serverstate_example = """import asyncio
from nextpy.state_sync import ServerState, DatabaseState

# ServerState — React-style hook over shared keys
score = ServerState("game:score", initial_value=0)

current, setter = await score.use()     # (value, set) tuple
await score.set(100)                    # writes through StateManager + notifies subscribers

unsub = score.subscribe(lambda v: print("new score:", v))
unsub()                                 # returned callable removes the callback

# DatabaseState — same idea persisted to SQL (requires nextpy db configured)
db_state = DatabaseState(table_name="app_state")
await db_state.initialize()             # CREATE TABLE IF NOT EXISTS
await db_state.set("feature_flags", {"dark_mode": True})
flags = await db_state.get("feature_flags")
await db_state.delete("feature_flags")"""

    sync_example = """# Server side: any set_state() reaches every connected /ws client
# as a {"type": "STATE_CHANGE", "key", "old_value", "new_value", ...} event.
# Clients subscribed to a channel only get targeted publishes:

from nextpy.websocket import manager

await manager.subscribe(client_id, "leaderboard")
await manager.publish("leaderboard", {"type": "SCORE", "user": "u_1", "score": 9000})

# Late joiners can pull current component state:
# client sends {"type": "sync_request", "component_id": ...}
# server replies {"type": "SYNC_RESPONSE", "component_id": ..., "payload": {...}}"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Core Concepts</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">State Management Model</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        State Management Model
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        How state flows through a NextPy page: server props, hydration, per-key signals, server actions, and the shared StateManager that syncs state to other clients over WebSocket.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy state has four layers. <strong class="text-zinc-200">Server props</strong> come from <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code> and render into the initial HTML. <strong class="text-zinc-200">Component state</strong> is declared with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useState</code>/<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useReducer</code> inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@interactive_component</code> and updates the DOM without a reload. <strong class="text-zinc-200">Server action state</strong> reports back through reserved <code class="font-mono text-xs">_server_*</code> keys. <strong class="text-zinc-200">Shared server state</strong> lives in the global <code class="font-mono text-xs">StateManager</code> and fans out to every connected client over <code class="font-mono text-xs">/ws</code>.
                    </p>
                </div>

                <div id="component-state" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Component-Local State</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Hooks are backed by <code class="font-mono text-xs">PSXHooks</code> in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx/components/component.py</code>. Each component owns an ordered <code class="font-mono text-xs">hooks</code> list and a <code class="font-mono text-xs">hook_index</code> cursor — the same call order on every render is what keeps hook state stable, exactly like React.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/cart.py" snippet={hooks_example} />
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300">
                        <li><strong class="text-white">useState(initial)</strong> returns <code class="font-mono text-xs">[value, setter]</code>. The setter doesn't mutate immediately — it appends the update (value or updater function) to a per-hook queue and flags the component <code class="font-mono text-xs">_needs_rerender</code>. On the next render every queued update is applied in order, so functional updaters compose correctly: two <code class="font-mono text-xs">set(c =&gt; c + 1)</code> calls yield +2.</li>
                        <li><strong class="text-white">useReducer(reducer, initial, init?)</strong> is the same machinery for complex state: <code class="font-mono text-xs">dispatch(action)</code> queues actions that are folded through your reducer on the next render. An optional third argument initializes state via <code class="font-mono text-xs">reducer(initial, init_action)</code>.</li>
                        <li><strong class="text-white">useEffect(effect, deps)</strong> compares a hash of the dependency list each render and re-runs the effect (with cleanup) when it changes; <code class="font-mono text-xs">deps=None</code> runs every render. Effects are skipped during SSR — there is no <code class="font-mono text-xs">window</code>/<code class="font-mono text-xs">document</code> on the server.</li>
                        <li>The full hook set is exported from <code class="font-mono text-xs">nextpy.psx</code>: <code class="font-mono text-xs">useState, useEffect, useContext, useReducer, useRef, useMemo, useCallback, useImperativeHandle, useLayoutEffect, useDebugValue, useTransition, useDeferredValue, useId</code>, plus custom hooks like <code class="font-mono text-xs">useFetch, useAction, useLocalStorage, useDebounce</code>.</li>
                        <li>Initial values must be JSON-serializable — they're embedded in the page as hydration state.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="components/counter.py" snippet={state_example} />
                </div>

                <div id="signals" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Signals &amp; Dependency Tracking</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        On the client, state isn't a render-everything model. The action runtime (<code class="font-mono text-xs">js_actions_runtime.js</code>) keeps a per-component <code class="font-mono text-xs">Map</code> of per-key <code class="font-mono text-xs">PSXSignal</code> objects. Every JSX binding — text, attributes, conditionals — subscribes to exactly the keys it reads.
                    </p>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300">
                        <li>When a setter writes key <code class="font-mono text-xs">count</code>, only expressions that read <code class="font-mono text-xs">count</code> are re-evaluated — siblings bound to other keys are untouched. This is the fine-grained update model that makes large pages cheap to update.</li>
                        <li><code class="font-mono text-xs">psxEffect</code>-style tracking works the same way: an effect records which signals it read, then re-runs only when one of those signals changes — not on every state write.</li>
                        <li>DOM writes are coalesced through <code class="font-mono text-xs">requestAnimationFrame</code> — all pending mutations flush in a single frame (with a <code class="font-mono text-xs">setTimeout</code> fallback when the tab is hidden), preventing layout thrash from rapid updates.</li>
                        <li>Legacy hydration components get the same treatment through a generated <code class="font-mono text-xs">StateManager</code> class whose <code class="font-mono text-xs">set()</code> notifies subscribers and mirrors values into <code class="font-mono text-xs">NextPyActionRuntime</code> state so server-action params stay in sync.</li>
                    </ul>
                </div>

                <div id="server-state" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Server Action State</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">callServerAction</code> is a compiler marker — the PSX handler compiler turns it into a <code class="font-mono text-xs">CALL_SERVER_ACTION</code> action, and the JS runtime POSTs to <code class="font-mono text-xs">/__nextpy/actions/execute</code>. Results land in reserved state keys you can bind and watch:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">_server_result</code> &mdash; the JSON response from the last action call.</li>
                        <li><code class="font-mono text-xs">_server_loading</code> &mdash; true while the request is in flight; use it to disable buttons.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/todos.py" snippet={server_example} />
                </div>

                <div id="state-manager" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Shared Server State — StateManager</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">state_sync.py</code> provides a process-wide, async <code class="font-mono text-xs">StateManager</code> for state that outlives a single request. Every <code class="font-mono text-xs">set()</code> bumps a global version, appends a <code class="font-mono text-xs">StateSnapshot</code> (history capped at 100), takes a per-key <code class="font-mono text-xs">asyncio.Lock</code>, and broadcasts a <code class="font-mono text-xs">STATE_CHANGE</code> event to all connected WebSocket clients.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="state/manager.py" snippet={manager_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">set(key, value, broadcast=True)</code> — pass <code class="font-mono text-xs">broadcast=False</code> for silent writes that skip both websocket and subscriber fan-out.</li>
                        <li><code class="font-mono text-xs">update(key, updater)</code> — reads then writes under the key's lock; <code class="font-mono text-xs">delete(key, broadcast=True)</code> removes and notifies with <code class="font-mono text-xs">new_value=None</code>.</li>
                        <li><code class="font-mono text-xs">subscribe(channel, callback, filters)</code> — server-side callbacks fire on every change; filters accept <code class="font-mono text-xs">&#123;"key_pattern": regex&#125;</code> or <code class="font-mono text-xs">&#123;"keys": [...]&#125;</code>. Returns a subscription id for <code class="font-mono text-xs">unsubscribe()</code>.</li>
                        <li><code class="font-mono text-xs">get_snapshot(version)</code>, <code class="font-mono text-xs">get_history(limit)</code>, <code class="font-mono text-xs">get_version()</code>, <code class="font-mono text-xs">export_state()</code>/<code class="font-mono text-xs">import_state(data, merge)</code> — inspection, history, and migration helpers.</li>
                    </ul>
                </div>

                <div id="serverstate-databasestate" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">ServerState vs DatabaseState</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Two convenience wrappers sit on top of the primitives:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="state/persistent.py" snippet={serverstate_example} />
                    <div class="grid sm:grid-cols-2 gap-4">
                        <div class="p-4 rounded-xl border border-blue-500/30 bg-blue-500/5">
                            <div class="text-sm font-semibold text-blue-400 mb-2">ServerState</div>
                            <p class="text-sm leading-6 text-zinc-400">React-style hook: <code class="font-mono text-xs">ServerState(key, initial)</code> → <code class="font-mono text-xs">.get()/.set()/.use()/.subscribe()</code>. Reads fall back to <code class="font-mono text-xs">initial_value</code>; writes go through the shared StateManager so they broadcast like any other key.</p>
                        </div>
                        <div class="p-4 rounded-xl border border-emerald-500/30 bg-emerald-500/5">
                            <div class="text-sm font-semibold text-emerald-400 mb-2">DatabaseState</div>
                            <p class="text-sm leading-6 text-zinc-400"><code class="font-mono text-xs">DatabaseState(table_name)</code> persists JSON values to a SQL table (<code class="font-mono text-xs">key/value/updated_at</code>) via <code class="font-mono text-xs">nextpy.db</code>, with an in-memory read cache. Table names are validated as simple SQL identifiers.</p>
                        </div>
                    </div>
                </div>

                <div id="realtime-sync" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Syncing to Other Clients</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The <code class="font-mono text-xs">/ws</code> endpoint (<code class="font-mono text-xs">websocket.py</code>) is guarded by the same trusted-origin check as CSRF. Its <code class="font-mono text-xs">ConnectionManager</code> assigns each socket a client id, supports named channels (<code class="font-mono text-xs">subscribe</code>/<code class="font-mono text-xs">publish</code>), and understands structured client messages — including <code class="font-mono text-xs">state_update</code> for multi-user component sync and <code class="font-mono text-xs">sync_request</code> for late joiners.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="realtime/sync.py" snippet={sync_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        The full loop looks like this — one component's write fans out through signals locally and through the WebSocket globally:
                    </p>
                    <div class="rounded-xl border border-zinc-800 bg-zinc-950/40 p-6 space-y-1 font-mono text-xs">
                        <div class="grid sm:grid-cols-2 gap-2">
                            <div class="p-3 rounded-lg border border-blue-500/30 bg-blue-500/5">
                                <div class="text-blue-400 font-semibold mb-2">Browser A — the writer</div>
                                <div class="text-zinc-400 space-y-1">
                                    <div>button click → handler runs</div>
                                    <div>↓ setCount(41) queues update</div>
                                    <div>↓ PSXSignal("count") notifies subscribers</div>
                                    <div>↓ dependent bindings re-evaluate</div>
                                    <div>↓ rAF flush patches DOM</div>
                                </div>
                            </div>
                            <div class="p-3 rounded-lg border border-emerald-500/30 bg-emerald-500/5">
                                <div class="text-emerald-400 font-semibold mb-2">Server → Browser B — other clients</div>
                                <div class="text-zinc-400 space-y-1">
                                    <div>await set_state("game:score", 41)</div>
                                    <div>↓ StateManager.set → version++, snapshot</div>
                                    <div>↓ manager.broadcast STATE_CHANGE</div>
                                    <div>↓ /ws delivers to all clients</div>
                                    <div>↓ client applies key update → signals → DOM</div>
                                </div>
                            </div>
                        </div>
                        <div class="text-center text-zinc-500 pt-2">↑ server actions and shared keys are the bridge between the two halves</div>
                    </div>
                </div>

                <div id="props-state" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Props Become State</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        JSON-safe props passed to a component are merged into its hydration state (underscore-prefixed and non-serializable values are filtered out), so <code class="font-mono text-xs">props.get("title")</code> values are readable in event handlers and bindings after hydration. Keep props JSON-safe — never pass DB sessions, request objects, or other server-only values.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/concepts/rendering" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Rendering (SSR, SSG, ISR)
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/concepts/compilation" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Compilation Pipeline
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
                        <li><a href="#component-state" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Component-Local State</a></li>
                        <li><a href="#signals" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Signals &amp; Tracking</a></li>
                        <li><a href="#server-state" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server Action State</a></li>
                        <li><a href="#state-manager" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">StateManager API</a></li>
                        <li><a href="#serverstate-databasestate" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">ServerState vs DatabaseState</a></li>
                        <li><a href="#realtime-sync" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Syncing to Clients</a></li>
                        <li><a href="#props-state" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Props Become State</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "State Management Model - NextPy Docs"}}


default = StateModel
