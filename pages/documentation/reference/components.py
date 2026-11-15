"""Components API - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def ComponentsAPI():
    builtins_example = """from nextpy.psx import (
    component, Link, Head, Meta, Title, Script, Image,
    Motion, AnimatePresence, Form, Input, Button, Card,
)

@component
def Example():
    return (
        <div>
            <Head>
                <Title>My Page</Title>
                <Meta name="description" content="..." />
            </Head>
            <Link href="/about">About</Link>
            <Motion initial={{"opacity": 0}} animate={{"opacity": 1}}>
                <Card>Hello</Card>
            </Motion>
        </div>
    )"""

    custom_example = """from nextpy.psx import component, register_component, Props

@component
def Badge(props):
    return <span class="badge">{props.get("label", "")} </span>

register_component("Badge", Badge)"""

    navigation_example = """from nextpy.psx import Link, NavItem

@component
def Nav():
    return (
        <nav class="flex gap-4">
            <Link href="/">Home</Link>
            <Link href="/about" prefetch={False} replace>About</Link>
            <Link href="https://example.com" target="_blank">External</Link>
            <NavItem href="/contact">Contact</NavItem>
        </nav>
    )"""

    head_example = """from nextpy.psx import Head, Title, Meta, Layout

@component
def Page():
    return (
        <Layout title="Dashboard" description="User dashboard" lang="en">
            <Head>
                <Title>Dashboard - My App</Title>
                <Meta name="description" content="User dashboard" />
                <Meta property="og:title" content="Dashboard" />
            </Head>
            <main>Page content</main>
        </Layout>
    )"""

    media_example = """from nextpy.psx import Script, Image

@component
def Media():
    return (
        <div>
            <Script src="https://cdn.example.com/lib.js" />
            <Image src="/logo.png" alt="Logo" width={120} height={40} />
        </div>
    )"""

    forms_example = """from nextpy.psx import Form, Input, Button

@component
def Signup():
    return (
        <Form action="/signup" method="POST">
            <Input type="email" name="email" placeholder="you@example.com" required />
            <Input type="password" name="password" placeholder="Password" required />
            <Button type="submit">Sign up</Button>
        </Form>
    )"""

    composite_example = """from nextpy.psx import Card, List, Navbar, NavItem

@component
def Page():
    return (
        <div>
            <Navbar brand="MyApp">
                <NavItem href="/">Home</NavItem>
                <NavItem href="/docs">Docs</NavItem>
            </Navbar>
            <Card title="Welcome" footer="v1.0">
                <p>Card body content.</p>
            </Card>
            <List items={["one", "two", "three"]} ordered />
        </div>
    )"""

    control_example = """from nextpy.psx import Conditional, Loop, ErrorBoundary, Suspense

@component
def Feed(props):
    items = props.get("items", [])
    return (
        <ErrorBoundary>
            <Suspense>
                <Conditional condition={len(items) > 0}>
                    <Loop items={items} render=lambda item: <li>{item}</li>} />
                </Conditional>
            </Suspense>
        </ErrorBoundary>
    )"""

    motion_example = """from nextpy.psx import Motion, AnimatePresence

@component
def Animated(props):
    show = props.get("show", True)
    return (
        <AnimatePresence>
            {show && (
                <Motion
                    as="div"
                    initial={{"opacity": 0, "y": 10}}
                    animate={{"opacity": 1, "y": 0}}
                    exit={{"opacity": 0}}
                    transition={{"duration": 0.3, "easing": "ease-out"}}
                    className="card"
                >
                    Hello
                </Motion>
            )}
        </AnimatePresence>
    )"""

    crud_example = """from nextpy.psx import component, useState, useCrudEvent, interactive_component

@interactive_component
def Todos():
    [_todos, _setTodos] = useState([])
    event = useCrudEvent(resource="todos")

    return (
        <div data-nextpy-crud={{
            "resource": "todos",
            "createAction": "create_todo",
            "updateAction": "update_todo",
            "deleteAction": "delete_todo",
        }}>
            <form data-nextpy-action="create">
                <input data-nextpy-field="title" placeholder="New todo" />
                <button type="submit">Add</button>
            </form>
            <ul data-nextpy-list>
                {_todos.map(lambda t: (
                    <li data-nextpy-item={t["id"]} key={t["id"]}>
                        <span data-nextpy-field="title">{t["title"]}</span>
                        <button data-nextpy-delete={t["id"]}>Delete</button>
                    </li>
                ))}
            </ul>
            <p data-nextpy-error class="hidden"></p>
            <span data-nextpy-status></span>
        </div>
    )"""

    helpers_example = """from nextpy.psx import fragment, key, clsx, conditional, ternary

@component
def Helpers(props):
    items = props.get("items", [])
    return (
        <ul class={clsx("list", {"list-active": len(items) > 0})}>
            {conditional(len(items) > 0, <li>has items</li>, <li>empty</li>)}
            {ternary(len(items) > 3, "many", "few")}
        </ul>
    )

# fragment() and key() are also available from nextpy.psx.core.parser"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Reference API</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Components API</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Components API</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Reference for NextPy built-in components, custom components, and the hooks they expose.
                    </p>
                </header>

                <div id="builtins" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Built-in components</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Import everything from <code class="font-mono text-xs">nextpy.psx</code>. All HTML elements are available as tags; these are the framework-provided components:
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Component</th>
                                    <th class="text-left px-4 py-3 font-semibold">Purpose</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Link</td><td class="px-4 py-3">Client-side navigation with prefetching and SPA routing.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Head / Title / Meta</td><td class="px-4 py-3">Per-page metadata injected into the document head.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Script / Image</td><td class="px-4 py-3">Script tags and optimized image rendering.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Motion / AnimatePresence</td><td class="px-4 py-3">Declarative animations and exit transitions.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Form / Input / Button</td><td class="px-4 py-3">Form primitives wired to the event system.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Card / Navbar / NavItem</td><td class="px-4 py-3">Layout and navigation helpers.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Conditional / Loop / ErrorBoundary / Suspense</td><td class="px-4 py-3">Control-flow and resilience primitives.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/example.py" snippet={builtins_example} />
                </div>

                <div id="navigation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Navigation</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">Link</code> renders an <code class="font-mono text-xs">&lt;a&gt;</code> tag wired into the client-side router. Internal links get <code class="font-mono text-xs">data-nextpy-link</code> and prefetch automatically; setting <code class="font-mono text-xs">target</code> disables router navigation.
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Prop</th>
                                    <th class="text-left px-4 py-3 font-semibold">Type</th>
                                    <th class="text-left px-4 py-3 font-semibold">Default</th>
                                    <th class="text-left px-4 py-3 font-semibold">Description</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">href</td><td class="px-4 py-3 font-mono text-xs">string</td><td class="px-4 py-3 font-mono text-xs">"#"</td><td class="px-4 py-3">Destination URL.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">className</td><td class="px-4 py-3 font-mono text-xs">string</td><td class="px-4 py-3 font-mono text-xs">—</td><td class="px-4 py-3">Emitted as the HTML <code class="font-mono text-xs">class</code> attribute.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">target</td><td class="px-4 py-3 font-mono text-xs">string</td><td class="px-4 py-3 font-mono text-xs">—</td><td class="px-4 py-3">When set (e.g. <code class="font-mono text-xs">_blank</code>), skips client-side routing.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">prefetch</td><td class="px-4 py-3 font-mono text-xs">bool</td><td class="px-4 py-3 font-mono text-xs">true</td><td class="px-4 py-3">Adds <code class="font-mono text-xs">data-nextpy-prefetch</code> so the router prefetches the page.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">replace</td><td class="px-4 py-3 font-mono text-xs">bool</td><td class="px-4 py-3 font-mono text-xs">false</td><td class="px-4 py-3">Replaces the history entry instead of pushing a new one.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">scroll</td><td class="px-4 py-3 font-mono text-xs">bool</td><td class="px-4 py-3 font-mono text-xs">true</td><td class="px-4 py-3">Set to <code class="font-mono text-xs">False</code> to preserve scroll position.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">NavItem</code> is a thin wrapper that renders a <code class="font-mono text-xs">Link</code>; it accepts <code class="font-mono text-xs">href</code> and children.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/nav.py" snippet={navigation_example} />
                </div>

                <div id="document-head" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Document head &amp; metadata</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">Head</code> renders a <code class="font-mono text-xs">&lt;head&gt;</code> element for per-page metadata.</li>
                        <li><code class="font-mono text-xs">Title</code> renders <code class="font-mono text-xs">&lt;title&gt;</code>; children become the page title text.</li>
                        <li><code class="font-mono text-xs">Meta</code> renders <code class="font-mono text-xs">&lt;meta&gt;</code> and forwards every prop as an attribute (<code class="font-mono text-xs">name</code>, <code class="font-mono text-xs">content</code>, <code class="font-mono text-xs">property</code>, <code class="font-mono text-xs">charset</code>, ...).</li>
                        <li><code class="font-mono text-xs">Layout</code> renders a full <code class="font-mono text-xs">&lt;html&gt;</code> document with a default head (charset, viewport, title, description meta) and your children in <code class="font-mono text-xs">&lt;body&gt;</code>.</li>
                    </ul>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Layout prop</th>
                                    <th class="text-left px-4 py-3 font-semibold">Default</th>
                                    <th class="text-left px-4 py-3 font-semibold">Description</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">lang</td><td class="px-4 py-3 font-mono text-xs">"en"</td><td class="px-4 py-3">Value of the <code class="font-mono text-xs">lang</code> attribute on <code class="font-mono text-xs">&lt;html&gt;</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">title</td><td class="px-4 py-3 font-mono text-xs">"NextPy App"</td><td class="px-4 py-3">Default document title.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">description</td><td class="px-4 py-3 font-mono text-xs">"NextPy Application"</td><td class="px-4 py-3">Default meta description.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={head_example} />
                </div>

                <div id="media" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Media &amp; scripts</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">Script</code> renders <code class="font-mono text-xs">&lt;script src="..."&gt;</code> from the <code class="font-mono text-xs">src</code> prop; inline children are supported too.</li>
                        <li><code class="font-mono text-xs">Image</code> renders <code class="font-mono text-xs">&lt;img&gt;</code> with <code class="font-mono text-xs">src</code>, <code class="font-mono text-xs">alt</code>, <code class="font-mono text-xs">width</code>, and <code class="font-mono text-xs">height</code> props.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="components/media.py" snippet={media_example} />
                </div>

                <div id="layout-components" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Layout &amp; forms</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Simple structural components render plain HTML with a <code class="font-mono text-xs">className</code> prop (emitted as <code class="font-mono text-xs">class</code>):
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Component</th>
                                    <th class="text-left px-4 py-3 font-semibold">Renders</th>
                                    <th class="text-left px-4 py-3 font-semibold">Props</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Container</td><td class="px-4 py-3"><code class="font-mono text-xs">&lt;div class="container"&gt;</code></td><td class="px-4 py-3 font-mono text-xs">className</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Row</td><td class="px-4 py-3"><code class="font-mono text-xs">&lt;div class="row"&gt;</code></td><td class="px-4 py-3 font-mono text-xs">className</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Col</td><td class="px-4 py-3"><code class="font-mono text-xs">&lt;div class="col"&gt;</code></td><td class="px-4 py-3 font-mono text-xs">className</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Form</td><td class="px-4 py-3"><code class="font-mono text-xs">&lt;form&gt;</code></td><td class="px-4 py-3 font-mono text-xs">action, method (&quot;GET&quot; default)</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Input</td><td class="px-4 py-3"><code class="font-mono text-xs">&lt;input&gt;</code></td><td class="px-4 py-3 font-mono text-xs">type, name, value, placeholder, required</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Button</td><td class="px-4 py-3"><code class="font-mono text-xs">&lt;button&gt;</code></td><td class="px-4 py-3 font-mono text-xs">type (&quot;button&quot; default), disabled</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/signup.py" snippet={forms_example} />
                </div>

                <div id="composite" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Composite components</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Component</th>
                                    <th class="text-left px-4 py-3 font-semibold">Props</th>
                                    <th class="text-left px-4 py-3 font-semibold">Description</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Navbar</td><td class="px-4 py-3 font-mono text-xs">brand, className</td><td class="px-4 py-3">Renders <code class="font-mono text-xs">&lt;nav&gt;</code> with a <code class="font-mono text-xs">nav-brand</code> div and a <code class="font-mono text-xs">nav-links</code> container for children.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">Card</td><td class="px-4 py-3 font-mono text-xs">title, footer, className</td><td class="px-4 py-3">Card with optional <code class="font-mono text-xs">card-header</code> (h3 title), <code class="font-mono text-xs">card-body</code>, and <code class="font-mono text-xs">card-footer</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">List</td><td class="px-4 py-3 font-mono text-xs">items, ordered</td><td class="px-4 py-3">Renders <code class="font-mono text-xs">&lt;ul&gt;</code> (or <code class="font-mono text-xs">&lt;ol&gt;</code> when <code class="font-mono text-xs">ordered</code>) from an <code class="font-mono text-xs">items</code> list; dict items use their <code class="font-mono text-xs">text</code> key.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/home.py" snippet={composite_example} />
                </div>

                <div id="control-flow" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Control flow &amp; resilience</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">Conditional</code> renders its children only when the <code class="font-mono text-xs">condition</code> prop is truthy (default <code class="font-mono text-xs">True</code>).</li>
                        <li><code class="font-mono text-xs">Loop</code> maps over the <code class="font-mono text-xs">items</code> prop, calling the <code class="font-mono text-xs">render</code> callable for each item.</li>
                        <li><code class="font-mono text-xs">ErrorBoundary</code> and <code class="font-mono text-xs">Suspense</code> are structural wrappers that render their children inside a plain <code class="font-mono text-xs">&lt;div&gt;</code>; they mark regions for error/loading handling in the runtime.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="components/feed.py" snippet={control_example} />
                </div>

                <div id="motion" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Motion &amp; AnimatePresence</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">Motion</code> is a Framer-Motion-style wrapper. It SSR-renders children tagged with animation config; the client runtime plays animations with the Web Animations API — no JS bundle required.
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Prop</th>
                                    <th class="text-left px-4 py-3 font-semibold">Type</th>
                                    <th class="text-left px-4 py-3 font-semibold">Description</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">as</td><td class="px-4 py-3 font-mono text-xs">string</td><td class="px-4 py-3">HTML tag to render (default <code class="font-mono text-xs">div</code>).</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">initial</td><td class="px-4 py-3 font-mono text-xs">dict</td><td class="px-4 py-3">Style dict applied before mount, e.g. <code class="font-mono text-xs">&#123;"opacity": 0&#125;</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">animate</td><td class="px-4 py-3 font-mono text-xs">dict</td><td class="px-4 py-3">Target style dict; values may be scalars or <code class="font-mono text-xs">[from, to, ...]</code> keyframes.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">exit</td><td class="px-4 py-3 font-mono text-xs">dict</td><td class="px-4 py-3">Style dict played before conditional removal.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">transition</td><td class="px-4 py-3 font-mono text-xs">dict</td><td class="px-4 py-3"><code class="font-mono text-xs">&#123;"duration": 0.3, "easing": "ease-out", "delay": 0&#125;</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">layout</td><td class="px-4 py-3 font-mono text-xs">bool</td><td class="px-4 py-3">True → FLIP-animate layout changes.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">whileHover / whileTap</td><td class="px-4 py-3 font-mono text-xs">dict</td><td class="px-4 py-3">Style dicts for pointer states.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">className / style / id</td><td class="px-4 py-3 font-mono text-xs">—</td><td class="px-4 py-3">Standard attributes forwarded to the rendered element.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">AnimatePresence</code> is a layout-neutral marker (<code class="font-mono text-xs">display:contents</code> span) that keeps descendant <code class="font-mono text-xs">Motion</code> elements mounted long enough to play their <code class="font-mono text-xs">exit</code> animation when a conditional removes them.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/animated.py" snippet={motion_example} />
                </div>

                <div id="crud" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">CRUD runtime &amp; useCrudEvent</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Any element carrying a <code class="font-mono text-xs">data-nextpy-crud</code> attribute (JSON config) is hydrated by the built-in CRUD runtime. It wires create forms, toggle checkboxes, and delete buttons to server actions, and keeps the list in sync over a WebSocket channel.
                    </p>
                    <h3 class="text-lg font-semibold text-white tracking-tight">Config keys (data-nextpy-crud)</h3>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Key</th>
                                    <th class="text-left px-4 py-3 font-semibold">Default</th>
                                    <th class="text-left px-4 py-3 font-semibold">Description</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">resource</td><td class="px-4 py-3 font-mono text-xs">—</td><td class="px-4 py-3">Resource name; used for <code class="font-mono text-xs">messageType</code>/<code class="font-mono text-xs">wsChannel</code> defaults.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">createAction</td><td class="px-4 py-3 font-mono text-xs">"create"</td><td class="px-4 py-3">Server action invoked by the create form.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">updateAction</td><td class="px-4 py-3 font-mono text-xs">"update"</td><td class="px-4 py-3">Server action invoked by <code class="font-mono text-xs">data-nextpy-toggle</code> controls.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">deleteAction</td><td class="px-4 py-3 font-mono text-xs">"delete"</td><td class="px-4 py-3">Server action invoked by <code class="font-mono text-xs">data-nextpy-delete</code> buttons.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">idParam</td><td class="px-4 py-3 font-mono text-xs">"id"</td><td class="px-4 py-3">Parameter name used to send the item id.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">updateFields</td><td class="px-4 py-3 font-mono text-xs">—</td><td class="px-4 py-3">Extra fields merged into every update payload.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">deleteConfirm</td><td class="px-4 py-3 font-mono text-xs">true</td><td class="px-4 py-3"><code class="font-mono text-xs">false</code> disables confirmation; <code class="font-mono text-xs">"psx"</code> uses a PSX-rendered modal (<code class="font-mono text-xs">data-delete-modal</code>); a string becomes the confirm message.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">createReset</td><td class="px-4 py-3 font-mono text-xs">true</td><td class="px-4 py-3">Reset the create form after a successful submit.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">wsChannel / messageType</td><td class="px-4 py-3 font-mono text-xs">resource / RESOURCE_CHANGED</td><td class="px-4 py-3">WebSocket channel and message type driving live updates.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <h3 class="text-lg font-semibold text-white tracking-tight">DOM hooks</h3>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">data-nextpy-list</code> — container that receives newly created items.</li>
                        <li><code class="font-mono text-xs">data-nextpy-item="&#123;id&#125;"</code> — identifies a row; <code class="font-mono text-xs">data-nextpy-field="name"</code> children are filled from item data on create/update.</li>
                        <li><code class="font-mono text-xs">data-nextpy-action="create"</code> — form submitted to <code class="font-mono text-xs">createAction</code>; each <code class="font-mono text-xs">data-nextpy-field</code> becomes a param.</li>
                        <li><code class="font-mono text-xs">data-nextpy-toggle="&#123;id&#125;"</code> — checkbox/radio that calls <code class="font-mono text-xs">updateAction</code> on change.</li>
                        <li><code class="font-mono text-xs">data-nextpy-delete="&#123;id&#125;"</code> — button that confirms then calls <code class="font-mono text-xs">deleteAction</code>.</li>
                        <li><code class="font-mono text-xs">data-nextpy-error</code> / <code class="font-mono text-xs">data-nextpy-status</code> — surfaces for error messages and connection status.</li>
                    </ul>
                    <h3 class="text-lg font-semibold text-white tracking-tight">useCrudEvent</h3>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">useCrudEvent(resource=None)</code> subscribes an interactive component to <code class="font-mono text-xs">nextpy:crud:changed</code> window events and returns <code class="font-mono text-xs">&#123;"data": ..., "_eventKey": ...&#125;</code>. Pass a <code class="font-mono text-xs">resource</code> to filter events by <code class="font-mono text-xs">config.resource</code>; the event detail contains <code class="font-mono text-xs">action</code> (<code class="font-mono text-xs">created</code>/<code class="font-mono text-xs">updated</code>/<code class="font-mono text-xs">deleted</code>), <code class="font-mono text-xs">item</code>, <code class="font-mono text-xs">config</code>, and <code class="font-mono text-xs">root</code>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/todos.py" snippet={crud_example} />
                </div>

                <div id="helpers" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Template &amp; utility helpers</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">fragment(...)</code> and <code class="font-mono text-xs">key(...)</code> — exported from <code class="font-mono text-xs">nextpy.psx.core.parser</code> for grouping children and assigning keys in loops.</li>
                        <li><code class="font-mono text-xs">clsx(*classes)</code> — conditionally joins class names; accepts strings, lists/tuples, and dicts of <code class="font-mono text-xs">&#123;"class": bool&#125;</code>.</li>
                        <li><code class="font-mono text-xs">conditional(cond, a, b)</code> / <code class="font-mono text-xs">ternary(cond, a, b)</code> / <code class="font-mono text-xs">and_condition</code> / <code class="font-mono text-xs">or_condition</code> — expression helpers for JSX interpolation.</li>
                        <li>List/object/math/string utilities such as <code class="font-mono text-xs">map_list</code>, <code class="font-mono text-xs">filter_list</code>, <code class="font-mono text-xs">object_keys</code>, <code class="font-mono text-xs">string_upper</code>, <code class="font-mono text-xs">math_max</code>, and type checks (<code class="font-mono text-xs">is_string</code>, <code class="font-mono text-xs">is_array</code>, ...) are available on the component module.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="components/helpers.py" snippet={helpers_example} />
                </div>

                <div id="custom-components" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Custom components</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Define components with <code class="font-mono text-xs">@component</code>, receive props as a dict, and register them for use in JSX:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="components/badge.py" snippet={custom_example} />
                </div>

                <div id="hooks" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Hooks</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        React-style hooks are exported from <code class="font-mono text-xs">nextpy.psx</code>:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><strong class="text-zinc-200">Core:</strong> <code class="font-mono text-xs">useState</code>, <code class="font-mono text-xs">useEffect</code>, <code class="font-mono text-xs">useRef</code>, <code class="font-mono text-xs">useMemo</code>, <code class="font-mono text-xs">useCallback</code>, <code class="font-mono text-xs">useReducer</code>, <code class="font-mono text-xs">useContext</code></li>
                        <li><strong class="text-zinc-200">Custom:</strong> <code class="font-mono text-xs">useCounter</code>, <code class="font-mono text-xs">useToggle</code>, <code class="font-mono text-xs">useLocalStorage</code>, <code class="font-mono text-xs">useFetch</code>, <code class="font-mono text-xs">useAction</code>, <code class="font-mono text-xs">useCrudEvent</code>, <code class="font-mono text-xs">useDebounce</code>, <code class="font-mono text-xs">useInterval</code>, <code class="font-mono text-xs">usePrevious</code>, <code class="font-mono text-xs">useAsync</code>, <code class="font-mono text-xs">useMediaQuery</code>, <code class="font-mono text-xs">useGeolocation</code>, <code class="font-mono text-xs">usePerformance</code></li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-300">
                        See the <Link href="/documentation/reference/hooks" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">Hooks API</Link> page for details.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/config" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Configuration
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
                        <li><a href="#builtins" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Built-in components</a></li>
                        <li><a href="#navigation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Navigation</a></li>
                        <li><a href="#document-head" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Document head &amp; metadata</a></li>
                        <li><a href="#media" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Media &amp; scripts</a></li>
                        <li><a href="#layout-components" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Layout &amp; forms</a></li>
                        <li><a href="#composite" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Composite components</a></li>
                        <li><a href="#control-flow" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Control flow &amp; resilience</a></li>
                        <li><a href="#motion" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Motion &amp; AnimatePresence</a></li>
                        <li><a href="#crud" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">CRUD runtime &amp; useCrudEvent</a></li>
                        <li><a href="#helpers" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Template &amp; utility helpers</a></li>
                        <li><a href="#custom-components" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Custom components</a></li>
                        <li><a href="#hooks" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Hooks</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Components API - NextPy Docs"}}


default = ComponentsAPI

