"""Events API - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, useState
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def EventsAPI():
    click_example = """from nextpy.psx import component, useState

@component
def Counter():
    [count, set_count] = useState(0)

    def increment():
        set_count(count + 1)

    return (
        <button onclick={increment}>
            Count: {count}
        </button>
    )"""

    input_example = """from nextpy.psx import component, useState

@component
def Search():
    [query, set_query] = useState("")

    return (
        <input
            value={query}
            oninput={lambda e: set_query(e.target.value)}
            placeholder="Search..."
        />
    )"""

    submit_example = """from nextpy.psx import component, useState, callServerAction

@component
def LoginForm():
    [email, set_email] = useState("")
    [password, set_password] = useState("")

    def handle_submit(e):
        e.preventDefault()
        callServerAction("login", {"email": email, "password": password})

    return (
        <form onsubmit={handle_submit}>
            <input value={email} oninput={lambda e: set_email(e.target.value)} />
            <input type="password" value={password} oninput={lambda e: set_password(e.target.value)} />
            <button type="submit">Sign in</button>
        </form>
    )"""

    loading_example = """<button type="submit" disabled={_server_loading}>
    {"Signing in..." if _server_loading else "Sign in"}
</button>"""

    create_on_example = """from nextpy.psx import interactive_component, useState, create_onclick, create_onkeydown

@interactive_component
def Panel():
    [open_, set_open] = useState(False)

    # create_on* factories return a handler placeholder string that the
    # hydration compiler registers and wires to the named DOM event.
    toggle = create_onclick(lambda e: set_open(not open_))
    on_escape = create_onkeydown(lambda e: set_open(False) if e.key == "Escape" else None)

    return (
        <div onclick={toggle} onkeydown={on_escape} tabindex="0">
            {"open" if open_ else "closed"}
        </div>
    )"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>API Reference</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Events API</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Events API</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Attach Python handlers to DOM events with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">on*</code> attributes — either directly (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">onclick=&#123;handler&#125;</code>) or via the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">create_on*</code> factory functions. Handlers run client-side, update state reactively, and can call server actions.
                    </p>
                </header>

                <div id="basics" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Basics</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Any attribute starting with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">on</code> is compiled into a delegated event listener. The handler receives the DOM event as its argument:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/counter.py" snippet={click_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Inline lambdas work too: <code class="font-mono text-xs">oninput=&#123;lambda e: set_query(e.target.value)&#125;</code>. For reusable handlers, define a <code class="font-mono text-xs">def</code> in the component body — its name is captured by the hydration compiler.
                    </p>
                </div>

                <div id="create-on" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">create_on* factories</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Each <code class="font-mono text-xs">create_on*</code> function takes a callable and returns a deterministic placeholder string (<code class="font-mono text-xs">python_call_&lt;name&gt;</code> or a hash for lambdas). Assign the result to a variable and bind it to the matching <code class="font-mono text-xs">on*</code> attribute — the hydration compiler registers the Python function and emits a <code class="font-mono text-xs">data-handler-&lt;event&gt;</code> attribute the client runtime dispatches.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/panel.py" snippet={create_on_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Sixty-four factories are exported from <code class="font-mono text-xs">nextpy.psx</code> (and re-exported from <code class="font-mono text-xs">nextpy</code>), covering every DOM event family below. The factory name is always <code class="font-mono text-xs">create_</code> + the attribute name with a capitalized first letter stripped — e.g. <code class="font-mono text-xs">create_ontouchstart</code> → <code class="font-mono text-xs">ontouchstart</code>.
                    </p>
                </div>

                <div id="mouse-events" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Mouse events</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Factory</th>
                                    <th class="text-left px-4 py-3 font-semibold">Attribute</th>
                                    <th class="text-left px-4 py-3 font-semibold">Fires when</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onclick</td><td class="px-4 py-2.5 font-mono text-xs">onclick</td><td class="px-4 py-2.5">Primary button click (press + release on same element)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ondblclick</td><td class="px-4 py-2.5 font-mono text-xs">ondblclick</td><td class="px-4 py-2.5">Double-click</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onmousedown / create_onmouseup</td><td class="px-4 py-2.5 font-mono text-xs">onmousedown / onmouseup</td><td class="px-4 py-2.5">Mouse button pressed / released over the element</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onmouseover / create_onmouseout</td><td class="px-4 py-2.5 font-mono text-xs">onmouseover / onmouseout</td><td class="px-4 py-2.5">Pointer enters / leaves the element or its descendants</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onmouseenter / create_onmouseleave</td><td class="px-4 py-2.5 font-mono text-xs">onmouseenter / onmouseleave</td><td class="px-4 py-2.5">Pointer enters / leaves the element itself (no descendant bubbling)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onmousemove</td><td class="px-4 py-2.5 font-mono text-xs">onmousemove</td><td class="px-4 py-2.5">Pointer moves over the element</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="keyboard-events" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Keyboard events</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Factory</th>
                                    <th class="text-left px-4 py-3 font-semibold">Attribute</th>
                                    <th class="text-left px-4 py-3 font-semibold">Fires when</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onkeydown</td><td class="px-4 py-2.5 font-mono text-xs">onkeydown</td><td class="px-4 py-2.5">Key pressed down (repeat while held)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onkeyup</td><td class="px-4 py-2.5 font-mono text-xs">onkeyup</td><td class="px-4 py-2.5">Key released</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onkeypress</td><td class="px-4 py-2.5 font-mono text-xs">onkeypress</td><td class="px-4 py-2.5">Printable key pressed (deprecated in modern browsers; prefer onkeydown)</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="form-events" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Forms &amp; inputs</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Factory</th>
                                    <th class="text-left px-4 py-3 font-semibold">Attribute</th>
                                    <th class="text-left px-4 py-3 font-semibold">Fires when</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onchange</td><td class="px-4 py-2.5 font-mono text-xs">onchange</td><td class="px-4 py-2.5">Value committed (blur/enter for text inputs; instant for selects)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_oninput</td><td class="px-4 py-2.5 font-mono text-xs">oninput</td><td class="px-4 py-2.5">Value changes on every keystroke — the controlled-input event</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onsubmit</td><td class="px-4 py-2.5 font-mono text-xs">onsubmit</td><td class="px-4 py-2.5">Form submitted; call <code class="font-mono text-xs">e.preventDefault()</code> to handle client-side</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onreset</td><td class="px-4 py-2.5 font-mono text-xs">onreset</td><td class="px-4 py-2.5">Form reset to default values</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onfocus / create_onblur</td><td class="px-4 py-2.5 font-mono text-xs">onfocus / onblur</td><td class="px-4 py-2.5">Element gains / loses focus</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_oninvalid</td><td class="px-4 py-2.5 font-mono text-xs">oninvalid</td><td class="px-4 py-2.5">Form control fails constraint validation on submit</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onselect</td><td class="px-4 py-2.5 font-mono text-xs">onselect</td><td class="px-4 py-2.5">Text selected inside an input/textarea</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/login.py" snippet={submit_example} />
                    <EnhancedCodeBlock lang="python" filename="pages/search.py" snippet={input_example} />
                </div>

                <div id="touch-events" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Touch events</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Factory</th>
                                    <th class="text-left px-4 py-3 font-semibold">Attribute</th>
                                    <th class="text-left px-4 py-3 font-semibold">Fires when</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ontouchstart / create_ontouchend</td><td class="px-4 py-2.5 font-mono text-xs">ontouchstart / ontouchend</td><td class="px-4 py-2.5">Finger touches / lifts off the element</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ontouchmove</td><td class="px-4 py-2.5 font-mono text-xs">ontouchmove</td><td class="px-4 py-2.5">Finger moves while touching</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ontouchcancel</td><td class="px-4 py-2.5 font-mono text-xs">ontouchcancel</td><td class="px-4 py-2.5">Touch interrupted by the browser (e.g. scroll takeover)</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="window-events" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Window &amp; document events</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Factory</th>
                                    <th class="text-left px-4 py-3 font-semibold">Attribute</th>
                                    <th class="text-left px-4 py-3 font-semibold">Fires when</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onload</td><td class="px-4 py-2.5 font-mono text-xs">onload</td><td class="px-4 py-2.5">Element (img/script) or window finishes loading</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onunload</td><td class="px-4 py-2.5 font-mono text-xs">onunload</td><td class="px-4 py-2.5">Page is being unloaded (window only)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onresize</td><td class="px-4 py-2.5 font-mono text-xs">onresize</td><td class="px-4 py-2.5">Viewport or element resized</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onscroll</td><td class="px-4 py-2.5 font-mono text-xs">onscroll</td><td class="px-4 py-2.5">Element or document scrolled</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="drag-events" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Drag &amp; drop</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Factory</th>
                                    <th class="text-left px-4 py-3 font-semibold">Attribute</th>
                                    <th class="text-left px-4 py-3 font-semibold">Fires when</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ondrag</td><td class="px-4 py-2.5 font-mono text-xs">ondrag</td><td class="px-4 py-2.5">Element or selected text is being dragged</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ondragstart</td><td class="px-4 py-2.5 font-mono text-xs">ondragstart</td><td class="px-4 py-2.5">Drag operation begins — set drag data here</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ondragend</td><td class="px-4 py-2.5 font-mono text-xs">ondragend</td><td class="px-4 py-2.5">Drag finished (drop or cancel), on the source</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ondragenter</td><td class="px-4 py-2.5 font-mono text-xs">ondragenter</td><td class="px-4 py-2.5">Dragged item enters a valid drop target</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ondragleave</td><td class="px-4 py-2.5 font-mono text-xs">ondragleave</td><td class="px-4 py-2.5">Dragged item leaves a drop target</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ondragover</td><td class="px-4 py-2.5 font-mono text-xs">ondragover</td><td class="px-4 py-2.5">Dragged item moves over a drop target (call preventDefault to allow drop)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ondrop</td><td class="px-4 py-2.5 font-mono text-xs">ondrop</td><td class="px-4 py-2.5">Item dropped on the target</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="media-events" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Media events</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Factory</th>
                                    <th class="text-left px-4 py-3 font-semibold">Attribute</th>
                                    <th class="text-left px-4 py-3 font-semibold">Fires when</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onplay / create_onpause</td><td class="px-4 py-2.5 font-mono text-xs">onplay / onpause</td><td class="px-4 py-2.5">Playback starts / pauses</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onended</td><td class="px-4 py-2.5 font-mono text-xs">onended</td><td class="px-4 py-2.5">Playback reaches the end</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onvolumechange</td><td class="px-4 py-2.5 font-mono text-xs">onvolumechange</td><td class="px-4 py-2.5">Volume or mute state changes</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ontimeupdate</td><td class="px-4 py-2.5 font-mono text-xs">ontimeupdate</td><td class="px-4 py-2.5">Playback position updates (frequent — throttle heavy work)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onseeking / create_onseeked</td><td class="px-4 py-2.5 font-mono text-xs">onseeking / onseeked</td><td class="px-4 py-2.5">Seek starts / completes</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onloadstart</td><td class="px-4 py-2.5 font-mono text-xs">onloadstart</td><td class="px-4 py-2.5">Browser starts fetching media data</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onprogress</td><td class="px-4 py-2.5 font-mono text-xs">onprogress</td><td class="px-4 py-2.5">Media download progress (also fires on &lt;progress&gt; elements)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onerror</td><td class="px-4 py-2.5 font-mono text-xs">onerror</td><td class="px-4 py-2.5">Media fails to load or decode</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onabort</td><td class="px-4 py-2.5 font-mono text-xs">onabort</td><td class="px-4 py-2.5">Media loading aborted before completion</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="animation-events" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Animation &amp; transition events</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Factory</th>
                                    <th class="text-left px-4 py-3 font-semibold">Attribute</th>
                                    <th class="text-left px-4 py-3 font-semibold">Fires when</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onanimationstart / create_onanimationend / create_onanimationiteration</td><td class="px-4 py-2.5 font-mono text-xs">onanimationstart / onanimationend / onanimationiteration</td><td class="px-4 py-2.5">CSS animation starts / finishes / repeats a cycle</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_ontransitionrun / create_ontransitionstart / create_ontransitionend</td><td class="px-4 py-2.5 font-mono text-xs">ontransitionrun / ontransitionstart / ontransitionend</td><td class="px-4 py-2.5">CSS transition created / actually starts / finishes</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="misc-events" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Clipboard, print, storage &amp; app events</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Factory</th>
                                    <th class="text-left px-4 py-3 font-semibold">Attribute</th>
                                    <th class="text-left px-4 py-3 font-semibold">Fires when</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onwheel</td><td class="px-4 py-2.5 font-mono text-xs">onwheel</td><td class="px-4 py-2.5">Mouse wheel / trackpad scroll over the element</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_oncopy / create_oncut / create_onpaste</td><td class="px-4 py-2.5 font-mono text-xs">oncopy / oncut / onpaste</td><td class="px-4 py-2.5">Clipboard copy / cut / paste on the element</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onbeforeprint / create_onafterprint</td><td class="px-4 py-2.5 font-mono text-xs">onbeforeprint / onafterprint</td><td class="px-4 py-2.5">Print dialog opens / closes (window only)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onstorage</td><td class="px-4 py-2.5 font-mono text-xs">onstorage</td><td class="px-4 py-2.5"><code class="font-mono text-xs">localStorage</code> changes in another tab (window only)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_onopen / create_onmessage / create_onclose</td><td class="px-4 py-2.5 font-mono text-xs">onopen / onmessage / onclose</td><td class="px-4 py-2.5">WebSocket-style lifecycle: connection opens / message arrives / closes</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_oninstall / create_onactivate</td><td class="px-4 py-2.5 font-mono text-xs">oninstall / onactivate</td><td class="px-4 py-2.5">Service-worker lifecycle events (PWA install / activation)</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">create_onfullscreenchange</code> and <code class="font-mono text-xs">create_onfullscreenerror</code> exist in <code class="font-mono text-xs">nextpy.psx.components.component</code> but are <strong class="text-white">not</strong> re-exported from <code class="font-mono text-xs">nextpy.psx</code> — import them from the submodule if needed.
                    </p>
                </div>

                <div id="server-actions" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Calling server actions</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">callServerAction(name, payload)</code> inside a handler to invoke a server-side function. The result lands in the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_result</code> state key, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">_server_loading</code> toggles while the request is in flight &mdash; bind it to disable submit buttons:
                    </p>
                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/login.py"
                        snippet={loading_example}
                    />
                </div>

                <div id="best-practices" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Best practices</h2>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-300">
                        <li>Keep handlers small &mdash; they compile to client-side JavaScript.</li>
                        <li>Use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useEffect</code> for subscriptions (scroll, timers, sockets) instead of inline listeners.</li>
                        <li>Prefer state-driven UI via data-state bindings and ternary expressions over manual DOM writes.</li>
                        <li>Remember <code class="font-mono text-xs">ontimeupdate</code>, <code class="font-mono text-xs">onmousemove</code>, and <code class="font-mono text-xs">onscroll</code> fire rapidly — debounce or throttle expensive work inside the handler.</li>
                    </ul>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/router" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Router API
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/utils" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Utilities
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
                        <li><a href="#basics" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Basics</a></li>
                        <li><a href="#create-on" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">create_on* factories</a></li>
                        <li><a href="#mouse-events" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Mouse events</a></li>
                        <li><a href="#keyboard-events" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Keyboard events</a></li>
                        <li><a href="#form-events" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Forms &amp; inputs</a></li>
                        <li><a href="#touch-events" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Touch events</a></li>
                        <li><a href="#window-events" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Window &amp; document</a></li>
                        <li><a href="#drag-events" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Drag &amp; drop</a></li>
                        <li><a href="#media-events" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Media events</a></li>
                        <li><a href="#animation-events" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Animation &amp; transition</a></li>
                        <li><a href="#misc-events" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Clipboard, print &amp; app</a></li>
                        <li><a href="#server-actions" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server actions</a></li>
                        <li><a href="#best-practices" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Best practices</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Events API - NextPy Docs"}}


default = EventsAPI
