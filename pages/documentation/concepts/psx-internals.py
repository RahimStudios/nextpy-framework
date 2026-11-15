"""PSX Core Internals — NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def PsxInternals():
    pipeline_example = """# pages/index.py — what you write
@component
def Page():
    return psx(\"\"\"
        <div class=\"p-4\">
            <h1>Hello</h1>
        </div>
    \"\"\")"""

    island_example = """from nextpy.psx import interactive_component, useState, useEffect

# SSR renders the initial HTML; the browser then hydrates this island
@interactive_component(hydrate="visible")
def Chart():
    [data, setData] = useState(None)

    def setup():
        async def load():
            res = await fetch("/api/chart")
            setData(await res.json())
        load()
        return None

    useEffect(setup, [])

    if not data:
        return <div>Loading chart…</div>
    return <canvas id="chart" width="400" height="200"></canvas>"""

    bindings_example = """from nextpy.psx import interactive_component, useState

@interactive_component
def Nav():
    [active, set_active] = useState("home")
    [progress, set_progress] = useState(0)

    link_base = "px-3 py-2 rounded-lg transition-colors"
    link_on   = f"{link_base} bg-blue-600 text-white"
    link_off  = f"{link_base} text-zinc-400 hover:text-white"

    bar_style = f"width: {progress}%"

    return (
        <nav>
            <a href="#home" class={link_on if active == "home" else link_off}>Home</a>
            <a href="#docs" class={link_on if active == "docs" else link_off}>Docs</a>
            <div style={bar_style} class="h-1 bg-blue-500"></div>
        </nav>
    )"""

    derived_bad = """# WRONG — 'for' comprehensions and props are server-only;
# the client cannot evaluate them, so the binding is dropped.
items_html = "".join(<li>{x}</li> for x in items)
label = props.get("title", "Untitled")"""

    scrollspy_example = """from nextpy.psx import interactive_component, useState, useEffect

@interactive_component
def ScrollSpy():
    [active, set_active] = useState("top")
    [progress, set_progress] = useState(0)

    def setup():
        def on_scroll():
            doc_h = document.documentElement.scrollHeight - window.innerHeight
            if doc_h > 0:
                set_progress((window.scrollY / doc_h) * 100)
            # last section above the line — never misses short sections
            current = "top"
            for sid in ["top", "middle", "bottom"]:
                el = document.getElementById(sid)
                if el and el.getBoundingClientRect().top <= 160:
                    current = sid
            set_active(current)

        window.addEventListener("scroll", on_scroll)
        on_scroll()
        return lambda: window.removeEventListener("scroll", on_scroll)

    useEffect(setup, [])
    # ...render nav links with class={on if active == sid else off}..."""

    dom_attrs_example = """def setup():
    def on_scroll():
        # Mutate attributes directly when the target set is dynamic —
        # e.g. "whatever <a> currently points at the active section".
        for a in document.querySelectorAll("aside a[href^='#']"):
            if a.getAttribute("href") == "#" + current:
                a.setAttribute("data-toc-active", "")
            else:
                a.removeAttribute("data-toc-active")
    window.addEventListener("scroll", on_scroll)
    on_scroll()
    return lambda: window.removeEventListener("scroll", on_scroll)"""

    opacity_dict = '{"opacity": 0}'
    transition_dict = '{"duration": 0.3, "easing": "ease-out", "delay": 0}'
    ph_value = "{value}"
    ph_class_expr = "class={expr}"
    ph_style_expr = "style={expr}"
    ph_style_width = 'f"width: {n}%"'
    ph_attr_expr = "attr={expr}"
    ph_dots = "{...}"
    ph_link_on = 'link_on = f"{link_base} ..."'
    ph_scroll_progress = "{scroll_progress}"
    ph_user_name = "{user.name}"
    ph_items0 = "{items[0]}"

    motion_example = """from nextpy.psx import Motion, AnimatePresence, interactive_component, useState

@interactive_component
def Panel():
    [open_, set_open] = useState(True)

    card = Motion({
        "initial":     {"opacity": 0, "scale": 0.9},
        "animate":     {"opacity": 1, "scale": 1},
        "exit":        {"opacity": 0, "scale": 0.9},
        "transition":  {"duration": 0.25, "easing": "ease-out"},
        "whileHover":  {"scale": 1.03},
        "layout":      True,   # FLIP-animate position changes
        "className":   "p-6 bg-white rounded-2xl shadow",
        "children":    [<h3>Animated card</h3>],
    })

    return (
        <div>
            <button onclick={lambda e: set_open(not open_)}>Toggle</button>
            {if open_: {AnimatePresence({"children": [card]}).to_html()}}
        </div>
    )"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Core Concepts</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">PSX Core Internals</span>
                    </div>
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

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">PSX Core Internals</h1>
                    <p class="leading-relaxed text-zinc-300">
                        PSX (Python JSX) is the layer that turns your Python components into fast HTML on the server and reactive islands in the browser. This page explains what happens between <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> and the pixels.
                    </p>
                </header>

                <div id="what-is-psx" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">What PSX is</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        PSX has two halves. On the server, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> evaluates Python f-string expressions inside an HTML template and returns a string — your markup is built with full Python power. In the browser, the hydration engine scans the rendered HTML for interactive components, replays their state into a signal graph, and binds events — no virtual DOM diffing of the whole page.
                    </p>
                </div>

                <div id="server-side" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Server-side rendering</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        A plain <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@component</code> runs entirely on the server. Expressions inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> — conditionals, comprehensions, function calls — evaluate in Python before any bytes reach the client:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={pipeline_example} />
                </div>

                <div id="hydration" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Hydration islands</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        An <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@interactive_component</code> still renders on the server — the client receives real HTML, not a blank div. The runtime then attaches behavior to that DOM in place. The <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">hydrate</code> strategy controls when:
                    </p>
                    <div class="overflow-hidden rounded-xl border border-zinc-800/80 mt-4">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-400">
                                <tr><th class="text-left px-4 py-2.5 font-medium">Strategy</th><th class="text-left px-4 py-2.5 font-medium">When it hydrates</th></tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">eager</td><td class="px-4 py-2.5">Immediately on page load (default)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">visible</td><td class="px-4 py-2.5">When scrolled into the viewport</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">interaction</td><td class="px-4 py-2.5">On first click, scroll, or keypress</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">idle</td><td class="px-4 py-2.5">When the main thread is idle</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/chart.py" snippet={island_example} />
                </div>

                <div id="state-bridge" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">The state bridge</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Initial state is serialized into the page as <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">__PSX_DATA__</code> JSON. On hydration, each <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useState</code> becomes a signal; expressions that depend on state are re-evaluated through a pub-sub graph and batched with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">requestAnimationFrame</code> — scroll and mouse handlers never trigger layout thrash.
                    </p>
                </div>

                <div id="reactive-bindings" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Reactive bindings</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        When an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@interactive_component</code> renders, the hydration engine rewrites dynamic expressions into <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">data-bind-*</code> attributes. On the client, a signal graph re-evaluates only the expressions that depend on changed state and writes the result straight to the DOM — text, <code class="font-mono text-xs">class</code>, <code class="font-mono text-xs">style</code>, or any other attribute — batched through <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">requestAnimationFrame</code>. No virtual DOM diff, no full re-render.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">{ph_value}</code> in text → <code class="font-mono text-xs">data-bind="textContent:key"</code></li>
                        <li><code class="font-mono text-xs">{ph_class_expr}</code> → <code class="font-mono text-xs">data-bind-class="expr"</code></li>
                        <li><code class="font-mono text-xs">{ph_style_expr}</code> → <code class="font-mono text-xs">data-bind-style="expr"</code> — pass a CSS string like <code class="font-mono text-xs">{ph_style_width}</code>, not a dict</li>
                        <li><code class="font-mono text-xs">{ph_attr_expr}</code> on any other attribute → <code class="font-mono text-xs">data-bind-attr-name="expr"</code></li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="components/nav.py" snippet={bindings_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        The ternary inside <code class="font-mono text-xs">{ph_dots}</code> is a Python expression the client re-evaluates on every state change  the nav link swaps classes the moment <code class="font-mono text-xs">active</code> changes, and the bar's width tracks <code class="font-mono text-xs">progress</code> at 60fps.
                    </p>
                </div>

                <div id="derived-expressions" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Derived expressions</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Plain assignments in the component body <code class="font-mono text-xs">{ph_link_on}</code> are captured at SSR time as <em>derived expressions</em> and shipped to the browser inside the hydration payload. The client re-evaluates them whenever a state variable they depend on changes — including chains like <code class="font-mono text-xs">link_on → link_base</code>, resolved by fixpoint iteration.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        The capture rules decide what stays reactive:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><strong class="text-white">Captured:</strong> literals, ternaries, f-strings, comparisons, arithmetic — as long as every name resolves to state or an <em>earlier</em> derived variable. Define dependencies before dependents.</li>
                        <li><strong class="text-white">Skipped:</strong> anything touching <code class="font-mono text-xs">props</code>, comprehensions/generator expressions, and calls to functions defined inside the component — none of those exist in the browser.</li>
                        <li><strong class="text-white">f-string holes</strong> must each be a plain variable name (<code class="font-mono text-xs">{ph_scroll_progress}</code> works; <code class="font-mono text-xs">{ph_user_name}</code> or <code class="font-mono text-xs">{ph_items0}</code> does not).</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="components/bad.py" snippet={derived_bad} />
                    <p class="text-base leading-7 text-zinc-300">
                        If a binding references a variable the client can't resolve, the runtime keeps the SSR-rendered attribute rather than writing garbage — but the element stops being reactive, which is the bug that silently strips <code class="font-mono text-xs">class</code> attributes on hydrated pages. When in doubt, compute the final string in one derived variable and bind that.
                    </p>
                </div>

                <div id="effects-listeners" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Effects and DOM listeners</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useEffect(setup, deps)</code> runs after hydration. The setup function may return a cleanup callable that runs before re-runs and on unmount — always unsubscribe there.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">useEffect(fn, [])</code> — once on mount (scroll listeners, timers, measurements).</li>
                        <li><code class="font-mono text-xs">useEffect(fn, [dep])</code> — re-run when <code class="font-mono text-xs">dep</code> changes.</li>
                        <li>High-frequency events <code class="font-mono text-xs">scroll</code>, <code class="font-mono text-xs">mousemove</code>, <code class="font-mono text-xs">input</code> are rAF-batched by the runtime — set state freely, updates coalesce per frame.</li>
                        <li>Listen for <code class="font-mono text-xs">"nextpy:navigate"</code> on <code class="font-mono text-xs">document</code> to re-sync after SPA navigations.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="components/scrollspy.py" snippet={scrollspy_example} />
                </div>

                <div id="scroll-patterns" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Scroll-driven UI: bindings vs direct DOM</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        There are two ways to react to scroll, and they solve different problems:
                    </p>
                    <div class="overflow-hidden rounded-xl border border-zinc-800/80 mt-4">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-400">
                                <tr><th class="text-left px-4 py-2.5 font-medium">Pattern</th><th class="text-left px-4 py-2.5 font-medium">Use when</th><th class="text-left px-4 py-2.5 font-medium">Mechanism</th></tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr>
                                    <td class="px-4 py-2.5 font-medium text-white">Reactive state + bindings</td>
                                    <td class="px-4 py-2.5">A fixed set of elements whose class/style/text depends on scroll position — nav highlight, progress bar, section titles</td>
                                    <td class="px-4 py-2.5"><code class="font-mono text-xs">useState</code> + <code class="font-mono text-xs">{ph_dots}</code>/<code class="font-mono text-xs">style={ph_dots}</code></td>
                                </tr>
                                <tr>
                                    <td class="px-4 py-2.5 font-medium text-white">Direct DOM writes</td>
                                    <td class="px-4 py-2.5">The target set is dynamic or attribute-shaped — "whatever link points at the active section", reveal-on-scroll markers, third-party widgets</td>
                                    <td class="px-4 py-2.5"><code class="font-mono text-xs">setAttribute</code>/<code class="font-mono text-xs">classList</code> inside the scroll handler; CSS keys off the attributes</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="text-base leading-7 text-zinc-300">
                        Prefer bindings for anything the framework can express — they stay declarative and diff-free. Drop to direct DOM writes when the update is "find elements matching a selector and toggle an attribute" — that's exactly what the docs layout's <code class="font-mono text-xs">DocsScrollSpy</code> does for TOC links, sidebar routes and section reveals, and it lives once in <code class="font-mono text-xs">pages/documentation/layout.psx</code> instead of every page.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/direct.py" snippet={dom_attrs_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Whichever pattern you pick, compute the active section as <strong class="text-white">the last section whose top crossed your threshold</strong> — never require <code class="font-mono text-xs">rect.top &lt;= X and rect.bottom &gt;= X</code>, which silently fails on short sections and programmatic scroll jumps.
                    </p>
                </div>

                <div id="motion" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Motion and animations</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Motion</code> wraps an element with a JSON config emitted as <code class="font-mono text-xs">data-psx-motion</code>; the client runtime plays it with the Web Animations API — no animation library, no JS bundle.
                    </p>
                    <div class="overflow-hidden rounded-xl border border-zinc-800/80 mt-4">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-400">
                                <tr><th class="text-left px-4 py-2.5 font-medium">Prop</th><th class="text-left px-4 py-2.5 font-medium">Effect</th></tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">initial</td><td class="px-4 py-2.5">Styles applied before mount e.g. <code class="font-mono text-xs">{opacity_dict}</code></td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">animate</td><td class="px-4 py-2.5">Target styles — scalars or <code class="font-mono text-xs">[from, to]</code> keyframe arrays</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">exit</td><td class="px-4 py-2.5">Played before a conditional removes the element</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">transition</td><td class="px-4 py-2.5"><code class="font-mono text-xs">{transition_dict}</code> (seconds)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">whileHover / whileTap</td><td class="px-4 py-2.5">Pointer-state styles, auto-reverted on leave</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">layout</td><td class="px-4 py-2.5"><code class="font-mono text-xs">True</code> → FLIP-animate position/size changes (e.g. sidebar toggles)</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/panel.py" snippet={motion_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><strong class="text-white">AnimatePresence</strong> marks a subtree so exit animations play before conditional removal — wrap conditionally-rendered Motion trees in it.</li>
                        <li>Motion elements injected later (conditional swaps, innerHTML) are picked up automatically by a MutationObserver.</li>
                        <li>Entrance animations commit their end state as inline styles on finish — that's why <code class="font-mono text-xs">getAnimations()</code> reads empty afterwards; it doesn't mean they didn't run.</li>
                    </ul>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/concepts/architecture" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Architecture Overview
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/concepts/routing-engine" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Routing Engine
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
                        <li><a href="#what-is-psx" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What PSX is</a></li>
                        <li><a href="#server-side" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server-side rendering</a></li>
                        <li><a href="#hydration" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Hydration islands</a></li>
                        <li><a href="#state-bridge" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The state bridge</a></li>
                        <li><a href="#reactive-bindings" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Reactive bindings</a></li>
                        <li><a href="#derived-expressions" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Derived expressions</a></li>
                        <li><a href="#effects-listeners" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Effects and DOM listeners</a></li>
                        <li><a href="#scroll-patterns" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Scroll-driven UI</a></li>
                        <li><a href="#motion" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Motion and animations</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "PSX Core Internals - NextPy Docs"}}


default = PsxInternals

