"""Real-Time: WebSockets, State Sync & Multi-User - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def RealtimeGuide():
    server_broadcast = '''"""Publish to a channel from a server action or API route."""

from nextpy.server_actions import server_action
from nextpy.websocket import manager


@server_action()
async def broadcast_demo(message: str = "Hello from NextPy!"):
    """Fan an event out to every client subscribed to 'demo'."""
    await manager.publish("demo", {
        "type": "DEMO_EVENT",
        "payload": {"message": message},
    })
    return {"published": True, "channel": "demo"}'''

    client_js = '''/* Subscribe to a channel and render incoming events.
   Plain browser JS — drop it in public/js/ and load with <script src>. */
(function () {
    var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    var socket;
    var retryDelay = 1000;

    function connect() {
        socket = new WebSocket(protocol + '//' + window.location.host + '/ws');
        socket.addEventListener('open', function () {
            retryDelay = 1000;
            socket.send(JSON.stringify({ type: 'subscribe', channel: 'demo' }));
        });
        socket.addEventListener('close', function () {
            setTimeout(connect, Math.min(retryDelay * 2, 30000));
            retryDelay *= 2;
        });
        socket.addEventListener('message', function (event) {
            var msg = JSON.parse(event.data);
            if (msg.type === 'DEMO_EVENT') {
                console.log('Live event:', msg.payload);
            }
        });
    }
    connect();
})();'''

    state_sync = '''"""Server-driven state sync via StateManager / state_sync helpers."""

from nextpy.state_sync import set_state, get_state, update_state


async def on_vote(user_id: str, option: str):
    # set_state broadcasts a STATE_CHANGE message to all WebSocket clients
    await set_state(f"vote:{option}", {
        "option": option,
        "count": await get_state(f"vote:{option}", 0) + 1,
    })

    # update_state applies a function under a per-key asyncio lock
    await update_state("leaderboard", lambda board: {
        **board, user_id: board.get(user_id, 0) + 1,
    })'''

    connection_api = '''"""ConnectionManager server-side API — nextpy.websocket.manager."""

from nextpy.websocket import manager


async def admin_broadcast():
    # Send a raw structured event to every connected client
    await manager.broadcast({
        "type": "ANNOUNCEMENT",
        "payload": {"text": "Server restarting in 60s"},
    })

    # Targeted state broadcast for one component
    await manager.emit_state_update("poll-42", {"votes": {"a": 3, "b": 1}})

    # Server-driven UI mutation
    await manager.emit_ui_update("banner-7", "replace_content",
                                 {"html": "<b>Maintenance mode</b>"})

    # Component lifecycle event
    await manager.emit_component_event("chat-9", "new_message",
                                       {"from": "ada", "text": "hi"})

    # Introspection helpers
    clients = manager.get_connected_clients()
    meta = manager.get_client_metadata(clients[0]) if clients else {}
    state = manager.get_component_state("poll-42")'''

    reload_example = '''from nextpy import broadcast_hot_reload


def refresh_all():
    """Force every open tab to reload."""
    broadcast_hot_reload()'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Real-Time: WebSockets, State Sync &amp; Multi-User</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Real-Time: WebSockets, State Sync &amp; Multi-User
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        NextPy includes a built-in WebSocket endpoint at <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/ws</code>, a channel-based pub/sub <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ConnectionManager</code>, and a server-side state synchronization layer — everything you need for live feeds, collaborative UI, and multi-user state without extra infrastructure.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The real-time stack lives in three modules: <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.websocket</code> (connections, channels, structured events), <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.state_sync</code> (server-side state with broadcast and snapshots), and the client runtime injected into every page, which connects to <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/ws</code>, handles state updates, and dispatches component events as DOM <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CustomEvent</code>s.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        All messages are JSON objects with a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">type</code> field. Clients speak a small protocol — <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">subscribe</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">publish</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">broadcast</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">state_update</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">component_event</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">sync_request</code>, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ping</code> — documented below.
                    </p>
                </div>

                <div id="websocket-endpoint" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">How the /ws endpoint works</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The FastAPI app mounts a WebSocket route at <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/ws</code> during startup. Before accepting, it validates the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Origin</code> header against <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CSRF_TRUSTED_ORIGINS</code> and the request host; untrusted origins are closed with code <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">1008</code>. On connect, the server assigns a unique <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">client_id</code> and sends a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CONNECTION_ESTABLISHED</code> message containing the client ID, a timestamp, and the current <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">component_states</code> snapshot.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        Malformed JSON frames get an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ERROR</code> reply without killing the connection, and graceful disconnects clean up the client's channel subscriptions automatically.
                    </p>
                </div>

                <div id="pubsub" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Channels &amp; pub/sub</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ConnectionManager</code> maintains named channels: a client sends <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">{'{"type": "subscribe", "channel": "todos"}'}</code> and receives a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">SUBSCRIPTION_CONFIRMED</code> acknowledgement. Server code then calls <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">manager.publish(channel, event)</code> to reach only subscribers, or <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">manager.broadcast(event)</code> for every connected client. Clients can also publish directly with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">{'{"type": "publish", "channel": "chat", "payload": {...}}'}</code>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/live.py" snippet={server_broadcast} />
                </div>

                <div id="state-sync" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Component state sync</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Clients send <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">{'{"type": "state_update", "component_id": "...", "payload": {...}}'}</code> and the server rebroadcasts it as a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">STATE_UPDATE</code> event to every client — that is the multi-user sync loop. New joiners can request current state with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">{'{"type": "sync_request", "component_id": "..."}'}</code> and receive a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">SYNC_RESPONSE</code>; stored component states are capped at 5000 entries.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        On the server, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.state_sync</code> provides a global <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">StateManager</code> plus convenience coroutines <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_state</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">set_state</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">update_state</code>, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">delete_state</code>. Writes take a per-key <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">asyncio.Lock</code>, bump a version counter, keep the last 100 <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">StateSnapshot</code>s, and broadcast a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">STATE_CHANGE</code> message to all WebSocket clients.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/votes.py" snippet={state_sync} />
                </div>

                <div id="component-events" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Component events &amp; UI updates</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Clients report interactions with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">{'{"type": "component_event", "component_id": "...", "event_name": "...", "payload": {...}}'}</code>. The server rebroadcasts a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">COMPONENT_EVENT</code> envelope, and the client runtime re-dispatches it on <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">document</code> as a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">CustomEvent</code> named <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">{'nextpy:{component_id}:{event_name}'}</code> — listen for it with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">document.addEventListener</code>.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        Server-driven UI mutations go through <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">emit_ui_update</code>, which sends a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">UI_UPDATE</code> message with an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">update_type</code> the client understands: <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">replace_content</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">update_attributes</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">add_class</code>, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">remove_class</code>.
                    </p>
                </div>

                <div id="connection-manager" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">ConnectionManager server API</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Import the singleton with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">from nextpy.websocket import manager</code>. It tracks <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">active_connections</code>, per-client <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">connection_metadata</code>, channel <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">subscribers</code>, and stored <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">component_states</code>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/admin.py" snippet={connection_api} />
                </div>

                <div id="hmr" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">broadcast_hot_reload &amp; HMR</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">broadcast_hot_reload()</code> (also exported as <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.broadcast_hot_reload</code>) signals every connected browser tab to reload the page. It is safe to call from any thread or async context and never raises. In development mode a file watcher on <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/</code> and templates triggers it automatically via the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/__nextpy/hmr</code> SSE endpoint; call it yourself after mutations that change rendered output, such as admin edits or config reloads.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/reload.py" snippet={reload_example} />
                </div>

                <div id="client-usage" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Client-side usage patterns</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The injected client runtime connects automatically, retries with exponential backoff (up to 5 attempts), and speaks the same JSON protocol. For custom UI you can open your own socket — <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ws://</code> on HTTP, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">wss://</code> on HTTPS — subscribe to a channel, and handle your own message types. The framework's own live-feed helper uses exactly this pattern: subscribe on <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">open</code>, reconnect with backoff on <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">close</code>, and filter on <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">message.type</code>.
                    </p>
                    <EnhancedCodeBlock lang="javascript" filename="public/js/live-feed.js" snippet={client_js} />
                </div>

                <div id="scaling" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Scaling notes</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ConnectionManager</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">StateManager</code> are in-process singletons: connections, subscriptions, and component state live in one Python process. Run a single uvicorn worker (or ensure sticky sessions) so every client lands on the same process, or front the app with a shared pub/sub backplane. Channel names are plain strings — namespacing them per feature (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">todos</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">chat:room-1</code>) keeps fan-out cheap and predictable.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/background-tasks" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Background Tasks
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/admin-panel" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Admin Panel
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
                        <li><a href="#websocket-endpoint" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">How the /ws endpoint works</a></li>
                        <li><a href="#pubsub" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Channels &amp; pub/sub</a></li>
                        <li><a href="#state-sync" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Component state sync</a></li>
                        <li><a href="#component-events" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Component events &amp; UI updates</a></li>
                        <li><a href="#connection-manager" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">ConnectionManager server API</a></li>
                        <li><a href="#hmr" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">broadcast_hot_reload &amp; HMR</a></li>
                        <li><a href="#client-usage" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Client-side usage patterns</a></li>
                        <li><a href="#scaling" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Scaling notes</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Real-Time: WebSockets, State Sync & Multi-User - NextPy Docs"}}

default = RealtimeGuide
