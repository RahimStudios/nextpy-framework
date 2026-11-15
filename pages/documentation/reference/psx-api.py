"""PSX API Reference - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, psx
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def PSXAPIReference():
    psx_example = """from nextpy.psx import component

@component
def Welcome(props):
    name = props.get("name", "world")
    return (
        <div class="card">
            <h1>Hello, {name}!</h1>
            {if name == "world":
                <p>Try passing a name prop.</p>
            }
            {for item in ["a", "b", "c"]:
                <li key={item}>{item}</li>
            {/for}
            <button onclick={lambda e: print("clicked")}>Click</button>
        </div>
    )"""

    component_example = """from nextpy.psx import component, register_component, clsx

@component
def Badge(props):
    label = props.get("label", "")
    tone = props.get("tone", "blue")
    cls = clsx("badge", f"badge-{tone}", {"badge-active": props.get("active")})
    return <span class={cls}>{label}</span>

register_component("Badge", Badge)"""

    class_example = """from nextpy.psx import PSXComponent, PSXElement

class Card(PSXComponent):
    def render(self):
        return PSXElement(
            tag="div",
            props={"class": "card"},
            children=[
                PSXElement(tag="h3", props={}, children=[self.props.get("title", "")]),
                PSXElement(tag="div", props={"class": "card-body"},
                           children=self.props.get("children", [])),
            ],
        )"""

    fragment_example = """from nextpy.psx import psx, fragment, key

el = psx('''<ul>{for x in items:<li key={x}>{x}</li>{/for}</ul>''')

# fragment() joins children into one string
html = fragment([el.to_html(), "<hr/>"])

# key() stamps a reconciliation key on an element
item = psx("<li>one</li>")
keyed = key("row-1", item)
print(keyed.key)  # "row-1\""""

    vdom_example = """from nextpy.psx import create_element, render, update, get_vdom_metrics

# React.createElement-style API returning VNode trees
vnode = create_element("div", {"class": "box"},
                       create_element("span", {}, "Hello"))

render(vnode)          # mount into the DOM container
metrics = get_vdom_metrics()  # {'renders': ..., 'patches': ...}

# Diff + patch: returns scheduling info, applies minimal DOM updates
update(old_vnode, new_vnode)"""

    renderer_example = """from nextpy.psx import renderer, render_psx, render_psx_component, psx

el = psx("<p class='x'>{title}</p>")
html = renderer.render(el, {"title": "Hi"})   # -> "<p class='x'>Hi</p>"
html = render_psx(el, {"title": "Hi"})        # element.to_html() shortcut

# render_psx_component adds the client runtime scripts around the HTML
page_html = render_psx_component(el, {"title": "Hi"})"""

    safe_eval_example = """from nextpy.psx import SafeExpressionEngine

engine = SafeExpressionEngine({"items": [3, 1, 2], "name": "ada"})
engine.evaluate("name.upper()")        # "ADA"
engine.evaluate("sorted(items)[0]")    # 1
engine.evaluate("[x * 2 for x in items]")  # [6, 2, 4]

# Raises ValueError for anything outside the whitelist:
engine.evaluate("__import__('os')")   # dangerous AST node
engine.evaluate("open('/etc/passwd')") # non-whitelisted function
engine.evaluate("getattr(x, '__class__')")  # getattr not whitelisted"""

    compiler_example = """from nextpy.psx import compile_psx, PSXCompiler

# Render a PSX fragment string to HTML
html = compile_psx("<div class='x'>hello</div>")

# For context-aware compilation use the compiler class directly:
compiler = PSXCompiler()
html = compiler.compile_psx("<p>{name}</p>", {"name": "ada"})
html = compiler.compile_psx_file("pages/index.py", {"name": "ada"})

# (module-level compile_psx_file / is_psx_file shims exist but
#  currently delegate to missing PSXCompiler methods — prefer the class)

# Under the hood the JSX preprocessor rewrites:
#     return (<div>...</div>)
# into:
#     return psx(\"\"\"<div>...</div>\"\"\")"""

    action_example = """from nextpy.psx import component, callServerAction

@component
def Login():
    def handle_login(e):
        callServerAction("login", {"user": "ada"})

    return <button onclick={handle_login}>Log in</button>

# The compiler rewrites the call into a CALL_SERVER_ACTION action;
# the JS runtime POSTs to /__nextpy/actions/execute and stores the
# JSON result in the _server_result state key."""

    utilities_example = """from nextpy.psx import (
    conditional, ternary, and_condition, or_condition,
    map_list, filter_list, reduce_list, find_list, some_list, every_list,
    create_context, Provider, key_value,
)

Theme = create_context("theme", "light")

items = map_list([1, 2, 3], lambda x: x * 2)          # [2, 4, 6]
evens = filter_list(items, lambda x: x % 2 == 0)      # [2, 4, 6]
total = reduce_list(items, lambda acc, x: acc + x, 0) # 12
first = find_list(items, lambda x: x > 4)             # 6

label = conditional(len(items) > 0, "has items", "empty")
alt = ternary(True, "yes", "no")
shown = and_condition(True, "render me")   # None when falsy
fallback = or_condition("", "default")     # "default"

# Provider supplies a context value to its subtree;
# useContext(Theme) inside reads it (default: "light")
<Provider context={Theme} value="dark">
    ...
</Provider>"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>API Reference</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">PSX API Reference</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">PSX API Reference</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Reference for the PSX (Python-Syntax-JSX) surface exported from <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.psx</code>: the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">psx()</code> primitive, component system, VDOM, renderer, compiler, safe expression engine, and server-action bridge.
                    </p>
                </header>

                <div id="psx-function" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">psx() — the core primitive</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">psx(psx_str: str, context: Dict[str, Any] = None) -&gt; PSXElement</code> parses a JSX-in-string into a <code class="font-mono text-xs">PSXElement</code> tree. When <code class="font-mono text-xs">context</code> is omitted, the caller's frame globals and locals are captured automatically so component names, state variables, and helpers resolve inside the markup.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        Inside the string, <code class="font-mono text-xs">&#123;expr&#125;</code> interpolates a Python expression (evaluated by <code class="font-mono text-xs">SafeExpressionEngine</code>), <code class="font-mono text-xs">&#123;if cond: ... &#125;</code> renders conditionally, <code class="font-mono text-xs">&#123;for x in items: ... &#125;...&#123;/for&#125;</code> loops, and <code class="font-mono text-xs">on*</code> attributes attach event handlers. Capitalized tags like <code class="font-mono text-xs">&lt;Badge /&gt;</code> resolve to registered components.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/welcome.py" snippet={psx_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li>The parser is thread-local and cached; a parse timeout or syntax error degrades to a text node rather than raising.</li>
                        <li>Use <code class="font-mono text-xs">render_psx(el, context)</code> or <code class="font-mono text-xs">el.to_html()</code> to serialize the tree to HTML.</li>
                    </ul>
                </div>

                <div id="components" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Components</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The <code class="font-mono text-xs">@component</code> decorator turns a function into a PSX component. It supports three calling conventions — <code class="font-mono text-xs">**props</code>, a single <code class="font-mono text-xs">props</code> dict, or named parameters — and captures the function's locals into the expression context so <code class="font-mono text-xs">&#123;var&#125;</code> bindings resolve at render time.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/badge.py" snippet={component_example} />
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Symbol</th>
                                    <th class="text-left px-4 py-3 font-semibold">Signature / kind</th>
                                    <th class="text-left px-4 py-3 font-semibold">Purpose</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">component</td><td class="px-4 py-2.5 font-mono text-xs">decorator</td><td class="px-4 py-2.5">Wrap a function as a PSX component; manages hook state per render.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">class_component</td><td class="px-4 py-2.5 font-mono text-xs">decorator</td><td class="px-4 py-2.5">Register a <code class="font-mono text-xs">PSXComponent</code> subclass as a component.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">PSXComponent</td><td class="px-4 py-2.5 font-mono text-xs">class</td><td class="px-4 py-2.5">Base class; subclass overrides <code class="font-mono text-xs">render()</code> returning a <code class="font-mono text-xs">PSXElement</code>.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">ChildrenComponent</td><td class="px-4 py-2.5 font-mono text-xs">class</td><td class="px-4 py-2.5">PSXComponent base that accepts and renders <code class="font-mono text-xs">children</code> props.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">register_component</td><td class="px-4 py-2.5 font-mono text-xs">(name, component)</td><td class="px-4 py-2.5">Add a component to the global <code class="font-mono text-xs">component_registry</code> so <code class="font-mono text-xs">&lt;Name /&gt;</code> resolves in markup.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">clsx</td><td class="px-4 py-2.5 font-mono text-xs">(*classes)</td><td class="px-4 py-2.5">Join class names; accepts strings, lists/tuples, and <code class="font-mono text-xs">&#123;class: cond&#125;</code> dicts.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">Props / Children / Component</td><td class="px-4 py-2.5 font-mono text-xs">helpers</td><td class="px-4 py-2.5">Props dict base type; <code class="font-mono text-xs">Children(props)</code> extracts children; <code class="font-mono text-xs">Component</code> is a compatibility decorator.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="components/card.py" snippet={class_example} />
                </div>

                <div id="fragment-key" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">fragment() and key()</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">fragment(children)</code> concatenates children (list or single) into one HTML string — a React-style fragment with no wrapper element. <code class="font-mono text-xs">key(key_value, element)</code> stamps a reconciliation key onto a <code class="font-mono text-xs">PSXElement</code> so list updates diff correctly.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/list.py" snippet={fragment_example} />
                </div>

                <div id="vdom" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Virtual DOM</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The VDOM layer mirrors React's model: <code class="font-mono text-xs">VNode</code> trees are created with <code class="font-mono text-xs">create_element(tag, props, *children)</code> (or <code class="font-mono text-xs">create_vnode</code>), <code class="font-mono text-xs">VDOMDiff.diff</code> computes a minimal patch list, and <code class="font-mono text-xs">update()</code> schedules it through <code class="font-mono text-xs">VDOMScheduler</code>. Patch types cover create, remove, replace, prop/text updates, component updates, and keyed moves.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="vdom/example.py" snippet={vdom_example} />
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Symbol</th>
                                    <th class="text-left px-4 py-3 font-semibold">Signature</th>
                                    <th class="text-left px-4 py-3 font-semibold">Purpose</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">VNode</td><td class="px-4 py-2.5 font-mono text-xs">dataclass</td><td class="px-4 py-2.5">Virtual node: <code class="font-mono text-xs">type</code>, <code class="font-mono text-xs">props</code>, <code class="font-mono text-xs">children</code>, <code class="font-mono text-xs">key</code>, <code class="font-mono text-xs">ref</code>.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">create_element</td><td class="px-4 py-2.5 font-mono text-xs">(tag, props, *children)</td><td class="px-4 py-2.5">Build a VNode; children are auto-wrapped as text/component vnodes.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">render</td><td class="px-4 py-2.5 font-mono text-xs">(vnode, container=None)</td><td class="px-4 py-2.5">Mount a VNode tree via the global <code class="font-mono text-xs">VDOMRenderer</code>.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">update</td><td class="px-4 py-2.5 font-mono text-xs">(old, new, container=None)</td><td class="px-4 py-2.5">Diff two trees and schedule patches; returns scheduling info.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">get_vdom_metrics</td><td class="px-4 py-2.5 font-mono text-xs">()</td><td class="px-4 py-2.5">Renderer performance counters (renders, patches, timings).</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="renderer" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Renderer</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">PSXRenderer</code> converts a <code class="font-mono text-xs">PSXElement</code> to an AST node and renders it through <code class="font-mono text-xs">PSXRuntime</code>. The module-level <code class="font-mono text-xs">renderer</code> instance is shared; <code class="font-mono text-xs">render_psx_component(element, context)</code> additionally injects the enhanced client runtime (and legacy action runtime when handlers are present) so the returned HTML is interactive.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="render/example.py" snippet={renderer_example} />
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Symbol</th>
                                    <th class="text-left px-4 py-3 font-semibold">Signature</th>
                                    <th class="text-left px-4 py-3 font-semibold">Purpose</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">PSXParser</td><td class="px-4 py-2.5 font-mono text-xs">class</td><td class="px-4 py-2.5"><code class="font-mono text-xs">parse_psx(psx_str, context, timeout)</code> → AST; AST parse + validate + optimize pipeline.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">PSXElement</td><td class="px-4 py-2.5 font-mono text-xs">dataclass</td><td class="px-4 py-2.5">Legacy element tree (<code class="font-mono text-xs">tag</code>, <code class="font-mono text-xs">props</code>, <code class="font-mono text-xs">children</code>, <code class="font-mono text-xs">key</code>) with <code class="font-mono text-xs">to_ast()</code> / <code class="font-mono text-xs">to_html()</code>.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">PSXRenderer</td><td class="px-4 py-2.5 font-mono text-xs">class</td><td class="px-4 py-2.5"><code class="font-mono text-xs">render(element, context)</code> and <code class="font-mono text-xs">render_ast(node, context)</code> → HTML.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">renderer</td><td class="px-4 py-2.5 font-mono text-xs">instance</td><td class="px-4 py-2.5">Shared <code class="font-mono text-xs">PSXRenderer</code>.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">render_psx</td><td class="px-4 py-2.5 font-mono text-xs">(element, context=None)</td><td class="px-4 py-2.5">Serialize a <code class="font-mono text-xs">PSXElement</code> (or value) to HTML.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">render_psx_component</td><td class="px-4 py-2.5 font-mono text-xs">(element, context=None)</td><td class="px-4 py-2.5">Render + inject client runtime scripts; used by the app server for pages.</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="compiler" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Compiler</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        You rarely call these directly — the JSX preprocessor rewrites <code class="font-mono text-xs">return (&lt;jsx&gt;)</code> into a <code class="font-mono text-xs">return psx(&lt;jsx string&gt;)</code> triple-quoted call at build time, adds missing <code class="font-mono text-xs">psx</code>/<code class="font-mono text-xs">component</code> imports, and validates each JSX block. See <Link href="/documentation/concepts/compilation" className="text-blue-400 hover:text-blue-300 underline decoration-blue-400/30 hover:decoration-blue-400">Compilation</Link> for the full pipeline.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="compiler/example.py" snippet={compiler_example} />
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Symbol</th>
                                    <th class="text-left px-4 py-3 font-semibold">Signature</th>
                                    <th class="text-left px-4 py-3 font-semibold">Purpose</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">PSXCompiler</td><td class="px-4 py-2.5 font-mono text-xs">class</td><td class="px-4 py-2.5">Backed by <code class="font-mono text-xs">PSXCore</code>; <code class="font-mono text-xs">compile_psx</code> / <code class="font-mono text-xs">compile_psx_file</code> render PSX to HTML, returning an error comment on failure.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">compile_psx</td><td class="px-4 py-2.5 font-mono text-xs">(source_code)</td><td class="px-4 py-2.5">Module-level convenience wrapper — single argument only; use <code class="font-mono text-xs">PSXCompiler().compile_psx(str, context)</code> when you need a context.</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs text-blue-400">compile_psx_file / is_psx_file</td><td class="px-4 py-2.5 font-mono text-xs">(file_path)</td><td class="px-4 py-2.5">Module-level shims — currently delegate to missing <code class="font-mono text-xs">PSXCompiler</code> methods and raise <code class="font-mono text-xs">AttributeError</code>; prefer <code class="font-mono text-xs">PSXCompiler.compile_psx_file</code> directly.</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="runtime" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Runtime & safe expressions</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">process_python_logic(psx_str, context, substitute_expressions=True)</code> preprocesses PSX source: it expands <code class="font-mono text-xs">&#123;if&#125;</code>/<code class="font-mono text-xs">&#123;for&#125;</code>/<code class="font-mono text-xs">&#123;while&#125;</code>/<code class="font-mono text-xs">&#123;try&#125;</code> control-flow blocks and, unless disabled, substitutes simple <code class="font-mono text-xs">&#123;expr&#125;</code> text so the AST parser can turn them into reactive expression nodes. The module-level <code class="font-mono text-xs">runtime</code> is the shared <code class="font-mono text-xs">PSXRuntime</code> instance (expression cache, context stack, HTML escaping).
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">SafeExpressionEngine.evaluate(expression)</code> is the sandboxed evaluator behind every <code class="font-mono text-xs">&#123;expr&#125;</code>. It parses the expression to an AST and walks it — no <code class="font-mono text-xs">eval()</code>, no builtins exposure.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="eval/safe.py" snippet={safe_eval_example} />
                    <div class="overflow-hidden rounded-xl border border-zinc-800/80 mt-4">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-400">
                                <tr><th class="text-left px-4 py-2.5 font-medium">Allowed</th><th class="text-left px-4 py-2.5 font-medium">Forbidden (raises ValueError)</th></tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-300">
                                <tr><td class="px-4 py-2.5 font-mono text-xs">Arithmetic/bitwise/comparison/bool ops, ternary <code class="font-mono">x if c else y</code></td><td class="px-4 py-2.5 font-mono text-xs">lambda, comprehensions other than list-comp paths, dict/set/generator comps in validation</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs">Subscripting, slicing, literals, f-strings, list literals</td><td class="px-4 py-2.5 font-mono text-xs">Statements: if/for/while/try/def/class/import/assign/return</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs">Whitelisted functions: len, str, int, float, bool, abs, min, max, sum, sorted, range, enumerate, zip, list, dict, set, tuple, isinstance, type, iter, next, pow, ord, chr, hex, oct, bin, clsx…</td><td class="px-4 py-2.5 font-mono text-xs">Any other call — including getattr/hasattr (deliberately absent to block dunder escapes)</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs">Whitelisted attributes only: upper, lower, strip, split, replace, find, startswith, endswith, join, format, count, title, capitalize, keys, values, items, get, update, append, pop, extend, sort, reverse, now, today, strftime, year, month, day, hour, minute, second</td><td class="px-4 py-2.5 font-mono text-xs">Any other attribute — especially <code class="font-mono">__class__</code>/<code class="font-mono">__mro__</code> dunders</td></tr>
                                <tr><td class="px-4 py-2.5 font-mono text-xs">Names from the render context + safe builtins</td><td class="px-4 py-2.5 font-mono text-xs">Unknown names, <code class="font-mono">**kwargs</code> in calls</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="server-actions" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">callServerAction</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">callServerAction(action_name: str, params: dict = None, on_result=None, on_error=None)</code> is a compile-time marker: the handler compiler recognizes the call in an event handler and emits a <code class="font-mono text-xs">CALL_SERVER_ACTION</code> action. The JS runtime POSTs to <code class="font-mono text-xs">/__nextpy/actions/execute</code>; the JSON result lands in the <code class="font-mono text-xs">_server_result</code> state key and <code class="font-mono text-xs">_server_loading</code> toggles in flight. See <Link href="/documentation/reference/server-actions" className="text-blue-400 hover:text-blue-300 underline decoration-blue-400/30 hover:decoration-blue-400">Server Actions</Link> for the full contract.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/login.py" snippet={action_example} />
                </div>

                <div id="utilities" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Utilities &amp; context</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        PSX ships Python-side helpers that mirror common JSX patterns. The list helpers (<code class="font-mono text-xs">map_list</code>, <code class="font-mono text-xs">filter_list</code>, <code class="font-mono text-xs">reduce_list</code>, <code class="font-mono text-xs">find_list</code>, <code class="font-mono text-xs">some_list</code>, <code class="font-mono text-xs">every_list</code>) take a callable per element; the conditional helpers (<code class="font-mono text-xs">conditional</code>, <code class="font-mono text-xs">ternary</code>, <code class="font-mono text-xs">and_condition</code>, <code class="font-mono text-xs">or_condition</code>) pick values without inline <code class="font-mono text-xs">if/else</code> expressions. <code class="font-mono text-xs">create_context(name, default)</code> builds a <code class="font-mono text-xs">Context</code> and <code class="font-mono text-xs">&lt;Provider context=&#123;ctx&#125; value=&#123;v&#125;&gt;</code> supplies it to descendants — pair with <code class="font-mono text-xs">useContext(ctx)</code>. <code class="font-mono text-xs">key_value(k, v)</code> builds a single-prop dict. The full <code class="font-mono text-xs">create_on*</code> family (including <code class="font-mono text-xs">create_onfullscreenchange</code>/<code class="font-mono text-xs">create_onfullscreenerror</code>) is listed in <Link href="/documentation/reference/events" className="text-blue-400 hover:text-blue-300 underline decoration-blue-400/30 hover:decoration-blue-400">Events</Link>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="utils.py" snippet={utilities_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/server-actions" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Server Actions
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/hooks" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Hooks API
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
                        <li><a href="#psx-function" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">psx()</a></li>
                        <li><a href="#components" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Components</a></li>
                        <li><a href="#fragment-key" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">fragment() &amp; key()</a></li>
                        <li><a href="#vdom" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Virtual DOM</a></li>
                        <li><a href="#renderer" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Renderer</a></li>
                        <li><a href="#compiler" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Compiler</a></li>
                        <li><a href="#runtime" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Runtime &amp; safe expressions</a></li>
                        <li><a href="#server-actions" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">callServerAction</a></li>
                        <li><a href="#utilities" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Utilities &amp; context</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "PSX API Reference - NextPy Docs"}}


default = PSXAPIReference
