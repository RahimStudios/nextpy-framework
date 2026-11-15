"""Hooks API - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def HooksAPI():
    usestate_example = """from nextpy.psx import component, useState

@component
def Counter():
    [count, set_count] = useState(0)

    def increment():
        set_count(count + 1)

    return (
        <div>
            <p>Count: {count}</p>
            <button onclick={increment}>+1</button>
        </div>
    )"""

    useeffect_example = """from nextpy.psx import component, useState, useEffect

@component
def ScrollSpy():
    [progress, set_progress] = useState(0)

    def setup():
        def on_scroll():
            doc_height = document.documentElement.scrollHeight - window.innerHeight
            if doc_height > 0:
                set_progress((window.scrollY / doc_height) * 100)

        window.addEventListener("scroll", on_scroll)
        on_scroll()
        return lambda: window.removeEventListener("scroll", on_scroll)

    useEffect(setup, [])

    progress_style = f"width: {progress}%; height: 4px; background: blue"
    return <div style={progress_style}></div>"""

    server_effect_example = """useEffect(handle_result, [_server_result])"""

    ref_shape = '{"current": initial}'
    ph_ref = 'ref={"name"}'
    ph_if_cond = "{if cond: ...}"

    useref_example = """from nextpy.psx import interactive_component, useRef, useEffect

@interactive_component
def Drawer():
    # Mutable box that survives re-renders without triggering them
    count = useRef(0)

    def setup():
        # ref={...} renders data-psx-ref; resolve the node via getRef
        el = window.nextpy.getRef(window.nextpy._componentId, "panel")
        if el:
            el.style.maxHeight = "0px"
        return None

    useEffect(setup, [])

    def bump(e):
        count.current += 1   # no re-render — read it imperatively
        return None

    return (
        <div>
            <button onclick={bump}>Clicks: {count.current}</button>
            <div ref={"panel"} class="overflow-hidden">...</div>
        </div>
    )"""

    derived_example = """from nextpy.psx import interactive_component, useState

@interactive_component
def Search():
    [query, set_query] = useState("")
    [items, set_items] = useState([])

    # Derived values: captured at SSR, re-evaluated on the client
    # whenever a dependency changes. Order matters — define
    # dependencies before dependents.
    q = query.strip().lower()
    has_q = bool(q)
    empty_msg = "No results" if has_q and not items else ""
    input_cls = "border-blue-500" if has_q else "border-zinc-700"

    return (
        <input value={query} oninput={lambda e: set_query(e.target.value)}
               class={input_cls} />
        <p>{empty_msg}</p>
    )"""

    usefetch_example = """from nextpy.psx import component, useFetch

@component
def UserList():
    fetch = useFetch("/api/users")
    data = fetch["data"]

    return (
        <div>
            {fetch["loading"] and <p>Loading...</p>}
            {fetch["error"] and <p>{fetch["error"]}</p>}
            <ul>
                {for user in (data or []):
                    <li>{user["name"]}</li>
                }
            </ul>
        </div>
    )"""

    reducer_example = """from nextpy.psx import interactive_component, useReducer

@interactive_component
def Todos():
    def reducer(state, action):
        kind = action["type"]
        if kind == "add":
            return {"items": state["items"] + [action["text"]]}
        if kind == "clear":
            return {"items": []}
        return state

    [state, dispatch] = useReducer(reducer, {"items": []}, None)

    return (
        <button onclick={lambda e: dispatch({"type": "clear"})}>
            Clear {len(state["items"])}
        </button>
    )"""

    context_example = """from nextpy.psx import component, useContext, create_context, Provider

Theme = create_context("theme", "light")

@component
def Themed():
    theme = useContext(Theme)   # "dark" inside a Provider, else "light"
    return <p class={f"theme-{theme}">Themed</p>

@component
def Page():
    return (
        <Provider context={Theme} value="dark">
            <Themed />
        </Provider>
    )"""

    memo_example = """from nextpy.psx import interactive_component, useState, useMemo, useCallback

@interactive_component
def Expensive():
    [query, set_query] = useState("")
    [items, set_items] = useState([3, 1, 2, 5, 4])

    # Recomputes only when `items` changes (deps hashed by JSON)
    sorted_items = useMemo(lambda: sorted(items), [items])

    # Stable callback identity while `sorted_items` is unchanged
    on_pick = useCallback(lambda i: set_query(f"picked {i}"), [sorted_items])

    return (
        <ul>
            {for i in sorted_items:
                <li onclick={lambda e, i=i: on_pick(i)}>{i}</li>
            {/for}
        </ul>
    )"""

    misc_hooks_example = """from nextpy.psx import interactive_component, useImperativeHandle, useLayoutEffect, useDebugValue, useTransition, useDeferredValue, useId

@interactive_component
def Demo():
    [is_pending, start] = useTransition()
    deferred = useDeferredValue(query)
    uid = useId()                       # "psx-<crc32>-<n>" — SSR-stable

    def effect():
        ...   # runs like useEffect (not truly synchronous)
    useLayoutEffect(effect, [])

    useDebugValue(uid)                  # stored for devtools only

    ref = useRef(None)
    useImperativeHandle(ref, lambda: {"focus": lambda: None}, [])"""

    custom_example = """from nextpy.psx import interactive_component, useCounter, useToggle

@interactive_component
def Controls():
    [count, inc, dec, reset, set_value] = useCounter(10, step=2)
    [open, toggle, set_true, set_false] = useToggle(False)

    return (
        <div>
            <button onclick={inc}>+2</button>
            <button onclick={dec}>-2</button>
            <button onclick={reset}>Reset</button>
            <button onclick={toggle}>{"Close" if open else "Open"}</button>
        </div>
    )"""

    storage_example = """from nextpy.psx import interactive_component, useLocalStorage, useDebounce

@interactive_component
def Settings():
    [theme, set_theme] = useLocalStorage("theme", "light")
    [draft, set_draft] = useState("")
    debounced = useDebounce(draft, 400)   # updates 400ms after typing stops

    return (
        <div>
            <button onclick={lambda e: set_theme("dark")}>Dark mode</button>
            <input value={draft} oninput={lambda e: set_draft(e.target.value)} />
            <p>Searching for: {debounced}</p>
        </div>
    )"""

    action_example = """from nextpy.psx import interactive_component, useAction, useCrudEvent

@interactive_component
def Todos():
    save = useAction("save_todo", {"id": 1})   # lazy — call save["run"] in a handler
    crud = useCrudEvent(resource="todos")      # latest nextpy:crud:changed event

    return (
        <button onclick={lambda e: save["run"]} disabled={save["loading"]}>
            Save
        </button>
    )"""

    interval_example = """from nextpy.psx import interactive_component, useState, useInterval, usePrevious

@interactive_component
def Clock():
    [tick, set_tick] = useState(0)
    prev = usePrevious(tick)          # value from the previous render

    [start, stop, toggle, running] = useInterval(
        lambda: set_tick(tick + 1), 1000, immediate=False
    )

    return <p>tick={tick} prev={prev} running={running}</p>"""

    async_example = """from nextpy.psx import interactive_component, useAsync, useState

@interactive_component
def Profile():
    async def load():
        return {"name": "Ada"}        # awaited client-side; SSR skips effects

    state = useAsync(load, [])
    data = state["data"]

    return <p>{data["name"] if data else "loading"}</p>"""

    browser_example = """from nextpy.psx import interactive_component, useMediaQuery, useGeolocation, usePerformance

@interactive_component
def Sensors():
    dark = useMediaQuery("(prefers-color-scheme: dark)")
    geo = useGeolocation()             # {position, error, loading, get_location}
    perf = usePerformance()            # {fps, memory, render_time, available}

    return (
        <div>
            <p>Dark mode: {dark}</p>
            <p>Location: {geo["position"]}</p>
            <p>FPS: {perf["fps"]} (available={perf["available"]})</p>
        </div>
    )"""

    legacy_example = """# Deprecated back-compat aliases from nextpy.hooks
from nextpy import (
    legacy_useState, legacy_useEffect, legacy_useContext,
    legacy_useReducer, legacy_useCallback, legacy_useMemo,
    legacy_useRef, legacy_useCounter, legacy_useToggle,
    legacy_useLocalStorage, legacy_useFetch, legacy_useDebounce,
)

# Prefer the canonical hooks from nextpy.psx — the legacy
# implementations differ in several ways (see "Legacy aliases")."""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>API Reference</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Hooks API</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Hooks API</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Reference for every NextPy hook: React-style hooks (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useState</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useEffect</code>, …), custom hooks (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useFetch</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useAction</code>, …), and deprecated <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">legacy_*</code> aliases. Each entry notes where behavior deviates from React — especially SSR, where several hooks honestly degrade or no-op.
                    </p>
                </header>

                <div id="usestate" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">useState</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Declares reactive state. Destructure into a value and a setter &mdash; updates re-render only the bound DOM nodes, not the whole page.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">useState(initial_value) -&gt; (value, setter)</code>
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li>Initial value can be any JSON-serializable Python value (a callable is invoked lazily).</li>
                        <li>Setters accept a value or an updater function: <code class="font-mono text-xs">set_count(lambda c: c + 1)</code>. Queued updates compose in order — two functional increments yield +2.</li>
                        <li>Multiple <code class="font-mono text-xs">useState</code> calls per component are fine &mdash; each is tracked independently by hook order.</li>
                        <li><strong class="text-white">SSR:</strong> state initializes normally; the setter only queues updates — the re-render happens client-side.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/counter.py" snippet={usestate_example} />
                </div>

                <div id="useeffect" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">useEffect</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Runs side effects after render. Pass a dependency list to control re-runs; return a cleanup function to unsubscribe.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">useEffect(effect: Callable, deps: Optional[List] = None) -&gt; None</code>
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">useEffect(fn, [])</code> &mdash; run once on mount.</li>
                        <li><code class="font-mono text-xs">useEffect(fn, [dep])</code> &mdash; re-run when <code class="font-mono text-xs">dep</code> changes (deps are hashed via JSON).</li>
                        <li><code class="font-mono text-xs">deps=None</code> re-runs every render.</li>
                        <li>Async effects are detected (<code class="font-mono text-xs">async def</code>) and scheduled on the event loop; async cleanups are awaited or scheduled, never silently dropped.</li>
                        <li><strong class="text-white">SSR:</strong> effects are skipped entirely when <code class="font-mono text-xs">window</code>/<code class="font-mono text-xs">document</code> are absent — the hook marks itself run without executing. Browser APIs must live inside effects.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/clock.py" snippet={useeffect_example} />
                    <EnhancedCodeBlock lang="python" filename="pages/effect_dep.py" snippet={server_effect_example} />
                </div>

                <div id="usermisc" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">More React-style hooks</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The remaining hooks follow React naming. Signatures and honest behavior notes below — several deviate from React semantics.
                    </p>

                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold text-white">useReducer</h3>
                        <p class="text-base leading-7 text-zinc-300"><code class="font-mono text-xs">useReducer(reducer, initial_state, init_action=None) -&gt; (state, dispatch)</code>. Actions queue and fold through <code class="font-mono text-xs">reducer(state, action)</code> on the next render; dispatching <code class="font-mono text-xs">None</code> raises. <strong class="text-white">SSR:</strong> returns the initial state — queued actions only apply client-side.</p>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/todos.py" snippet={reducer_example} />

                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold text-white">useContext</h3>
                        <p class="text-base leading-7 text-zinc-300"><code class="font-mono text-xs">useContext(context) -&gt; Any</code>. Create contexts with <code class="font-mono text-xs">create_context(name, default_value)</code> and supply values with <code class="font-mono text-xs">&lt;Provider context=&#123;ctx&#125; value=&#123;v&#125;&gt;</code> — <code class="font-mono text-xs">useContext</code> resolves the nearest enclosing provider during SSR render (nested providers shadow outer ones; siblings see the default). <strong class="text-white">SSR:</strong> provider lookup is render-time only — there is no client-side subscription, so context changes after hydration do not propagate.</p>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/theme.py" snippet={context_example} />

                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold text-white">useMemo / useCallback</h3>
                        <p class="text-base leading-7 text-zinc-300"><code class="font-mono text-xs">useMemo(factory, deps=None) -&gt; value</code>; <code class="font-mono text-xs">useCallback(callback, deps=None)</code> is implemented as <code class="font-mono text-xs">useMemo(lambda: callback, deps)</code>. Dependencies are JSON-hashed for comparison; <code class="font-mono text-xs">deps=None</code> recomputes every render. On factory error the previous value is kept. <strong class="text-white">SSR:</strong> factories run during SSR like normal Python — memoization only helps repeated client renders.</p>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/expensive.py" snippet={memo_example} />

                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold text-white">useImperativeHandle / useLayoutEffect / useDebugValue / useTransition / useDeferredValue / useId</h3>
                        <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                            <li><code class="font-mono text-xs">useImperativeHandle(ref, create_handle, deps=None)</code> — runs <code class="font-mono text-xs">create_handle()</code> and writes the result to <code class="font-mono text-xs">ref.current</code> (dict-style <code class="font-mono text-xs">ref['current']</code> refs also work) when deps change; <code class="font-mono text-xs">deps=None</code> re-runs every render.</li>
                            <li><code class="font-mono text-xs">useLayoutEffect(effect, deps=None)</code> — currently an alias of <code class="font-mono text-xs">useEffect</code>; not truly synchronous/pre-paint.</li>
                            <li><code class="font-mono text-xs">useDebugValue(value, formatter=None)</code> — stores a formatted value in hook state only; no devtools integration.</li>
                            <li><code class="font-mono text-xs">useTransition() -&gt; (is_pending, start_transition)</code> — <code class="font-mono text-xs">start_transition(cb)</code> executes <code class="font-mono text-xs">cb()</code> inline (no concurrent scheduler) and reports <code class="font-mono text-xs">is_pending=True</code> for the render pass that follows the transition.</li>
                            <li><code class="font-mono text-xs">useDeferredValue(value) -&gt; value</code> — keeps returning the previous value for one render after the input changes, then commits the new value (intermediate values may be skipped). <strong class="text-white">SSR:</strong> deferral only manifests across in-process re-renders.</li>
                            <li><code class="font-mono text-xs">useId() -&gt; str</code> — deterministic <code class="font-mono text-xs">psx-&lt;crc32&gt;-&lt;n&gt;</code> per component, stable across SSR/CSR so hydration matches.</li>
                        </ul>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/misc_hooks.py" snippet={misc_hooks_example} />
                </div>

                <div id="useref" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">useRef</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">useRef(initial=None)</code> returns a mutable ref object with a live <code class="font-mono text-xs">.current</code> property that persists across renders without triggering them — for values you mutate imperatively (counters, caches, previous values). Writing to it never re-renders; reading it in JSX gives you the SSR-time value only.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        For DOM nodes, prefer <code class="font-mono text-xs">{ph_ref}</code> on the element — it renders <code class="font-mono text-xs">data-psx-ref</code>, and the client runtime resolves it through <code class="font-mono text-xs">window.nextpy.getRef(componentId, name)</code> inside effects and handlers.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/drawer.py" snippet={useref_example} />
                </div>

                <div id="usefetch" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">useFetch</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">useFetch(url: str, options: Dict = None) -&gt; Dict</code> registers a <code class="font-mono text-xs">FETCH_DATA</code> mount action that runs <code class="font-mono text-xs">fetch(url, options)</code> in the browser and stores the response in component state.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        Returns a dict with <code class="font-mono text-xs">data</code>, <code class="font-mono text-xs">loading</code> (starts <code class="font-mono text-xs">True</code>), <code class="font-mono text-xs">error</code>, a <code class="font-mono text-xs">refetch</code> action descriptor, and internal <code class="font-mono text-xs">_dataKey</code>/<code class="font-mono text-xs">_loadingKey</code>/<code class="font-mono text-xs">_errorKey</code> state keys.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">SSR:</strong> no fetch happens server-side — <code class="font-mono text-xs">data</code> is <code class="font-mono text-xs">None</code> and <code class="font-mono text-xs">loading</code> stays <code class="font-mono text-xs">True</code> until the client runtime executes the mount action.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/users.py" snippet={usefetch_example} />
                </div>

                <div id="custom-hooks" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Custom hooks</h2>

                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold text-white">useCounter / useToggle</h3>
                        <p class="text-base leading-7 text-zinc-300">
                            <code class="font-mono text-xs">useCounter(initial_value=0, step=1) -&gt; (count, increment, decrement, reset, set_value)</code> — five-tuple; note the extra <code class="font-mono text-xs">set_value</code> vs. the legacy three-tuple.<br />
                            <code class="font-mono text-xs">useToggle(initial_value=False) -&gt; (value, toggle, set_true, set_false)</code>.
                        </p>
                        <p class="text-base leading-7 text-zinc-300"><strong class="text-white">SSR:</strong> pure <code class="font-mono text-xs">useState</code> wrappers — safe on the server.</p>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/controls.py" snippet={custom_example} />

                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold text-white">useLocalStorage / useDebounce</h3>
                        <p class="text-base leading-7 text-zinc-300">
                            <code class="font-mono text-xs">useLocalStorage(key: str, initial_value) -&gt; (value, set_value)</code> — loads the stored JSON value in a mount effect and saves with a 300ms debounce.<br />
                            <code class="font-mono text-xs">useDebounce(value, delay: int) -&gt; debounced_value</code> — returns <code class="font-mono text-xs">value</code> unchanged until <code class="font-mono text-xs">delay</code> ms after the last change.
                        </p>
                        <p class="text-base leading-7 text-zinc-300"><strong class="text-white">SSR:</strong> <code class="font-mono text-xs">useLocalStorage</code> degrades to plain <code class="font-mono text-xs">useState</code> — no <code class="font-mono text-xs">localStorage</code> exists server-side, so the initial value is returned and nothing persists. <code class="font-mono text-xs">useDebounce</code> schedules via <code class="font-mono text-xs">threading.Timer</code> during SSR.</p>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/settings.py" snippet={storage_example} />

                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold text-white">useAction / useCrudEvent</h3>
                        <p class="text-base leading-7 text-zinc-300">
                            <code class="font-mono text-xs">useAction(action_name: str, params: Dict = None, *, immediate: bool = False) -&gt; Dict</code> — compiles to a <code class="font-mono text-xs">CALL_SERVER_ACTION</code> action. Returns <code class="font-mono text-xs">&#123;data, loading, error, run, action&#125;</code>; call <code class="font-mono text-xs">result["run"]</code> from a handler (it's an action descriptor, not a plain callable). <code class="font-mono text-xs">immediate=True</code> fires on mount.<br />
                            <code class="font-mono text-xs">useCrudEvent(resource: Optional[str] = None) -&gt; Dict</code> — subscribes to <code class="font-mono text-xs">nextpy:crud:changed</code>; returns <code class="font-mono text-xs">&#123;data, _eventKey&#125;</code> where <code class="font-mono text-xs">_eventKey</code> is the state key to data-bind.
                        </p>
                        <p class="text-base leading-7 text-zinc-300"><strong class="text-white">SSR:</strong> actions are client-side only; <code class="font-mono text-xs">loading</code> starts <code class="font-mono text-xs">True</code> only when <code class="font-mono text-xs">immediate</code>.</p>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/todos_action.py" snippet={action_example} />

                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold text-white">useInterval / usePrevious</h3>
                        <p class="text-base leading-7 text-zinc-300">
                            <code class="font-mono text-xs">useInterval(callback, delay: int, immediate: bool = False) -&gt; [start, stop, toggle, is_running]</code> — reschedules via <code class="font-mono text-xs">threading.Timer</code> chains; <code class="font-mono text-xs">immediate=True</code> invokes the callback once up front.<br />
                            <code class="font-mono text-xs">usePrevious(value) -&gt; previous_value</code> — stores the last value in a ref inside an effect.
                        </p>
                        <p class="text-base leading-7 text-zinc-300"><strong class="text-white">SSR / deviation:</strong> <code class="font-mono text-xs">useInterval</code> uses Python timer threads server-side rather than <code class="font-mono text-xs">setInterval</code> — treat it as best-effort; the client runtime drives real intervals. <code class="font-mono text-xs">usePrevious</code> returns the initial value on first render and only updates after effects run (client-side).</p>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/clock.py" snippet={interval_example} />

                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold text-white">useAsync</h3>
                        <p class="text-base leading-7 text-zinc-300">
                            <code class="font-mono text-xs">useAsync(async_func: Callable, deps: Optional[List] = None) -&gt; Dict</code> — awaits <code class="font-mono text-xs">async_func()</code> inside an effect and returns <code class="font-mono text-xs">&#123;data, loading, error, execute&#125;</code>.
                        </p>
                        <p class="text-base leading-7 text-zinc-300"><strong class="text-white">SSR:</strong> effects don't run server-side, so <code class="font-mono text-xs">data</code> stays <code class="font-mono text-xs">None</code>, <code class="font-mono text-xs">loading</code> stays <code class="font-mono text-xs">False</code>, and the coroutine never executes during SSR.</p>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/profile.py" snippet={async_example} />

                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold text-white">useMediaQuery / useGeolocation / usePerformance</h3>
                        <p class="text-base leading-7 text-zinc-300">
                            <code class="font-mono text-xs">useMediaQuery(query: str) -&gt; bool</code> — intended to mirror <code class="font-mono text-xs">window.matchMedia</code>.<br />
                            <code class="font-mono text-xs">useGeolocation(options: Dict = None) -&gt; Dict</code> — returns <code class="font-mono text-xs">&#123;position, error, loading, get_location&#125;</code> backed by <code class="font-mono text-xs">navigator.geolocation</code>.<br />
                            <code class="font-mono text-xs">usePerformance() -&gt; Dict</code> — returns <code class="font-mono text-xs">&#123;fps, memory, render_time, available&#125;</code>.
                        </p>
                        <p class="text-base leading-7 text-zinc-300"><strong class="text-white">SSR — honest degradation:</strong> <code class="font-mono text-xs">useMediaQuery</code> conservatively returns <code class="font-mono text-xs">False</code>; <code class="font-mono text-xs">useGeolocation</code> reports <code class="font-mono text-xs">error="Geolocation is only available in the browser"</code>; <code class="font-mono text-xs">usePerformance</code> returns zeros with <code class="font-mono text-xs">available=False</code>. None fabricate browser data during SSR.</p>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/sensors.py" snippet={browser_example} />
                </div>

                <div id="server-state" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Server state keys</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Server actions write results into reserved state keys you can bind directly:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">_server_result</code> &mdash; the JSON payload returned by the last <code class="font-mono text-xs">callServerAction</code>.</li>
                        <li><code class="font-mono text-xs">_server_loading</code> &mdash; boolean, true while the request is in flight.</li>
                    </ul>
                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/login.py"
                        snippet={server_effect_example}
                    />
                </div>

                <div id="derived-values" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Derived values</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Assignments in the component body become <em>derived expressions</em>: evaluated once at SSR, then re-evaluated on the client whenever a state variable they depend on changes — including chains resolved by fixpoint. Use them for anything bound into JSX: class strings, style strings, labels, filtered lists rendered through bindings.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li>Every name in the expression must be state or an <strong class="text-white">earlier</strong> derived variable — order matters.</li>
                        <li>f-string holes must be plain variable names; <code class="font-mono text-xs">props.*</code>, comprehensions and local function calls are server-only and silently drop the binding.</li>
                        <li>For conditional rendering prefer <code class="font-mono text-xs">{ph_if_cond}</code> inline expressions or dedicated conditional components — a skipped derived variable freezes at its SSR value.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="components/search.py" snippet={derived_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        For the full capture rules, scroll-driven UI patterns and Motion animations, see <Link href="/documentation/concepts/psx-internals" className="text-blue-400 hover:text-blue-300 underline decoration-blue-400/30 hover:decoration-blue-400">PSX Core Internals</Link>.
                    </p>
                </div>

                <div id="legacy-aliases" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Legacy aliases</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">nextpy</code> re-exports the older <code class="font-mono text-xs">nextpy.hooks</code> implementations under <code class="font-mono text-xs">legacy_*</code> names for backward compatibility. They are deprecated — always import the canonical hooks from <code class="font-mono text-xs">nextpy.psx</code> instead.
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Alias</th>
                                    <th class="text-left px-4 py-3 font-semibold">Use instead</th>
                                    <th class="text-left px-4 py-3 font-semibold">Key difference</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useState</td><td class="px-4 py-2.5 font-mono text-xs">useState</td><td class="px-4 py-2.5">Applies only the last queued update; functional updaters don't compose.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useEffect</td><td class="px-4 py-2.5 font-mono text-xs">useEffect</td><td class="px-4 py-2.5">Runs the effect during SSR too — no window/document guard.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useContext</td><td class="px-4 py-2.5 font-mono text-xs">useContext</td><td class="px-4 py-2.5">Same — returns the context default only.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useReducer</td><td class="px-4 py-2.5 font-mono text-xs">useReducer</td><td class="px-4 py-2.5">No init_action third parameter; dispatch applies immediately.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useCallback / legacy_useMemo</td><td class="px-4 py-2.5 font-mono text-xs">useCallback / useMemo</td><td class="px-4 py-2.5">Element-wise <code class="font-mono text-xs">!=</code> dep comparison instead of JSON hashing.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useRef</td><td class="px-4 py-2.5 font-mono text-xs">useRef</td><td class="px-4 py-2.5">Returns a plain <code class="font-mono text-xs">&#123;"current": ...&#125;</code> dict rather than a <code class="font-mono text-xs">.current</code> object.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useCounter</td><td class="px-4 py-2.5 font-mono text-xs">useCounter</td><td class="px-4 py-2.5">Three-tuple <code class="font-mono text-xs">(count, inc, dec)</code> — no step/reset/set_value.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useToggle</td><td class="px-4 py-2.5 font-mono text-xs">useToggle</td><td class="px-4 py-2.5">Two-tuple <code class="font-mono text-xs">(value, toggle)</code> — no set_true/set_false.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useLocalStorage</td><td class="px-4 py-2.5 font-mono text-xs">useLocalStorage</td><td class="px-4 py-2.5">Plain <code class="font-mono text-xs">useState</code> — no persistence at all.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useFetch</td><td class="px-4 py-2.5 font-mono text-xs">useFetch</td><td class="px-4 py-2.5">Simulates fetch with <code class="font-mono text-xs">time.sleep</code> — no real HTTP request.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">legacy_useDebounce</td><td class="px-4 py-2.5 font-mono text-xs">useDebounce</td><td class="px-4 py-2.5">Relies on module-level timer shims; less robust cleanup.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/legacy.py"
                        snippet={legacy_example}
                    />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/components" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Components API
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/data-fetching" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Data Fetching
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
                        <li><a href="#usestate" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">useState</a></li>
                        <li><a href="#useeffect" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">useEffect</a></li>
                        <li><a href="#usermisc" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">More React-style hooks</a></li>
                        <li><a href="#useref" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">useRef</a></li>
                        <li><a href="#usefetch" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">useFetch</a></li>
                        <li><a href="#custom-hooks" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Custom hooks</a></li>
                        <li><a href="#server-state" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server state keys</a></li>
                        <li><a href="#derived-values" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Derived values</a></li>
                        <li><a href="#legacy-aliases" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Legacy aliases</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Hooks API - NextPy Docs"}}


default = HooksAPI
