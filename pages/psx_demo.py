"""PSX Reactivity Smoke Test — exercises every layer built so far:

* rAF-batched scroll updates + scroll-spy (client runtime reactivity)
* ``Motion`` WAAPI enter animations, ``layout`` FLIP, ``AnimatePresence`` exits
* ``ref={...}`` → ``data-psx-ref`` → ``window.nextpy.getRef``
* per-key state signals via ``window.nextpy.signal``
* island hydration via ``@interactive_component(hydrate='visible')``
"""

from nextpy.psx import (
    interactive_component,
    interactive_component as component,
    useState,
    useEffect,
    Motion,
    AnimatePresence,
    clsx,
)


@interactive_component(hydrate="visible")
def LazyWidget(props=None):
    """Island-hydrated component: listeners attach only when scrolled into view."""
    props = props or {}
    [clicks, set_clicks] = useState(0)

    def HandleClick():
        set_clicks(clicks + 1)

    return (
        <div class="p-8 bg-gradient-to-br from-violet-600 to-indigo-700 rounded-3xl text-white shadow-xl">
            <span class="text-xs font-bold tracking-widest uppercase text-violet-200">
                Island · lazy hydration
            </span>
            <h3 class="mt-2 text-2xl font-extrabold">Lazy Hydration Widget</h3>
            <p class="mt-2 text-sm text-violet-100">
                This component's event listeners were NOT attached on page load.
                An IntersectionObserver hydrated it when you scrolled here.
            </p>
            <button
                onclick={HandleClick}
                class="mt-4 px-5 py-2.5 font-semibold rounded-xl bg-white text-indigo-700 cursor-pointer hover:bg-violet-50 active:scale-95 transition"
            >
                Island Clicks: {clicks}
            </button>
        </div>
    )


@interactive_component
def Home(props=None):
    props = props or {}

    # ------------------------------------------------------------ state
    [scroll_progress, set_scroll_progress] = useState(0)
    [active_section, set_active_section] = useState("overview")
    [panel_open, set_panel_open] = useState(True)
    [sidebar_open, set_sidebar_open] = useState(True)
    [tap_count, set_tap_count] = useState(0)
    [signal_val, set_signal_val] = useState("idle")
    [ref_found, set_ref_found] = useState("pending")

    # ----------------------------------------------------------- effects
    def SetupScroll():
        def OnScroll():
            scroll_top = window.scrollY
            doc_height = document.documentElement.scrollHeight - window.innerHeight
            if doc_height > 0:
                set_scroll_progress((scroll_top / doc_height) * 100)

            for sec_id in ["overview", "motion", "panel", "island"]:
                el = document.getElementById(sec_id)
                if el:
                    rect = el.getBoundingClientRect()
                    if rect.top <= 200 and rect.bottom >= 200:
                        set_active_section(sec_id)

        window.addEventListener("scroll", OnScroll)
        OnScroll()
        return lambda: window.removeEventListener("scroll", OnScroll)

    useEffect(SetupScroll, [])

    # --------------------------------------------------------- handlers
    def TogglePanel():
        set_panel_open(not panel_open)

    def ToggleSidebar():
        set_sidebar_open(not sidebar_open)

    def HandleTap():
        set_tap_count(tap_count + 1)

    def CheckRef():
        el = window.nextpy.getRef(window.nextpy._componentId, "hero_card_ref")
        set_ref_found("found" if el else "missing")

    def ProbeSignal():
        set_signal_val("ok")

    # ------------------------------------------- derived (client-reactive) vars
    # Simple-name expressions become data-bind targets and are re-evaluated
    # client-side through the derived_expressions mechanism.
    sidebar_label = "Hide Sidebar" if sidebar_open else "Show Sidebar"
    panel_label = "Close Panel (exit anim)" if panel_open else "Open Panel"
    ref_label = "found" if ref_found == "found" else ref_found
    progress_pct = int(scroll_progress)
    progress_style = f"width: {scroll_progress}%"

    # ---------------------------------------------------- motion elements
    # WAAPI entrance + layout FLIP: when the sidebar toggles, this card's
    # position changes and the runtime animates the delta automatically.
    hero_card = Motion({
        "className": (
            "relative overflow-hidden p-8 md:p-10 bg-white border border-slate-200 "
            "rounded-3xl shadow-sm"
        ),
        "initial": {"opacity": 0, "transform": "translateY(28px)"},
        "animate": {"opacity": 1, "transform": "translateY(0px)"},
        "transition": {"duration": 0.6, "easing": "ease-out"},
        "layout": True,
        "children": [
            '<div class="absolute -top-10 -right-10 w-40 h-40 bg-blue-100 rounded-full blur-2xl"></div>',
            '<span class="relative inline-block px-3 py-1 text-xs font-bold tracking-wider text-blue-700 uppercase rounded-full bg-blue-50">Motion + FLIP</span>',
            '<h2 class="relative mt-3 text-3xl font-extrabold tracking-tight text-slate-900">WAAPI Animations, No JS Bundle</h2>',
            '<p class="relative mt-2 max-w-xl text-slate-600">',
            "This card animated in with the Web Animations API on mount, and its ",
            "position is FLIP-animated whenever the sidebar resizes the layout.",
            "</p>",
        ],
    })

    # AnimatePresence: exit animation plays before the conditional removes it.
    panel_card = Motion({
        "className": "p-6 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl text-white shadow-lg",
        "initial": {"opacity": 0, "scale": 0.85},
        "animate": {"opacity": 1, "scale": 1},
        "exit": {"opacity": 0, "scale": 0.8, "transform": "translateY(-10px)"},
        "transition": {"duration": 0.35, "easing": "ease-in"},
        "children": [
            '<h3 class="text-lg font-bold">Animated Panel</h3>',
            '<p class="mt-1 text-sm text-emerald-50">Closing this plays the WAAPI exit animation before removal.</p>',
        ],
    })
    panel_html = AnimatePresence({"children": [panel_card]}).to_html()

    # Island widget rendered through the hydration pipeline.
    lazy_widget = LazyWidget({})

    # --------------------------------------------------------- derived css
    nav_base = "flex items-center justify-between px-4 py-3 rounded-xl font-medium transition-all duration-300"
    nav_active = f"{nav_base} bg-blue-600 text-white shadow-lg shadow-blue-600/30 translate-x-1"
    nav_idle = f"{nav_base} text-slate-400 hover:text-white hover:bg-slate-800/70"

    section_title = "text-3xl font-extrabold tracking-tight md:text-4xl text-slate-900"

    # ------------------------------------------------------------ render
    return (
        <div class="flex min-h-screen font-sans antialiased text-slate-900 bg-slate-50">

            {/* rAF-batched scroll progress */}
            <div class="fixed top-0 left-0 right-0 z-50 h-1 bg-slate-200">
                <div
                    style={progress_style}
                    class="h-full bg-gradient-to-r from-blue-600 via-indigo-500 to-cyan-400"
                ></div>
            </div>

            {/* Sidebar — fixed positioning pins it to viewport */}
            <aside
                class={
                    "sticky top-0 h-screen bg-slate-900 text-white flex flex-col justify-between overflow-hidden transition-all duration-300 ease-out w-72 p-6 opacity-100"
                    if sidebar_open
                    else "sticky top-0 h-screen bg-slate-900 text-white flex flex-col justify-between overflow-hidden transition-all duration-300 ease-out w-0 p-0 opacity-0"
                }
            >
                <div class="flex flex-col h-full overflow-hidden">
                    <h2 class="text-xl font-bold pb-6 mb-6 border-b border-slate-800">PSX Reactivity Lab</h2>
                    <nav class="flex flex-col space-y-2">
                        <a href="#overview" class={nav_active if active_section == "overview" else nav_idle}>
                            <span>Overview</span><span class="font-mono text-xs">01</span>
                        </a>
                        <a href="#motion" class={nav_active if active_section == "motion" else nav_idle}>
                            <span>Motion / FLIP</span><span class="font-mono text-xs">02</span>
                        </a>
                        <a href="#panel" class={nav_active if active_section == "panel" else nav_idle}>
                            <span>AnimatePresence</span><span class="font-mono text-xs">03</span>
                        </a>
                        <a href="#island" class={nav_active if active_section == "island" else nav_idle}>
                            <span>Lazy Island</span><span class="font-mono text-xs">04</span>
                        </a>
                    </nav>
                    <div class="mt-auto p-4 space-y-2 text-xs text-slate-400 border rounded-xl bg-slate-800/80 border-slate-700/60">
                        <div>Section: <span class="font-mono text-blue-400">#{active_section}</span></div>
                        <div>Progress: <span class="font-mono text-blue-400">{progress_pct}%</span></div>
                    </div>
                </div>
            </aside>

            <main
                class={
                    "flex-1 px-6 py-12 space-y-24 md:px-12 transition-[margin] duration-300 ease-out "
                    if sidebar_open else "ml-0"
                }
            >

                {/* controls */}
                <div class="flex flex-wrap items-center gap-3 p-4 bg-white border rounded-2xl border-slate-200 shadow-sm">
                    <button
                        onclick={ToggleSidebar}
                        class="px-4 py-2 text-sm font-semibold text-white rounded-lg cursor-pointer bg-slate-900 hover:bg-slate-700 active:scale-95 transition"
                    >
                        {sidebar_label}
                    </button>
                    <button
                        onclick={TogglePanel}
                        class="px-4 py-2 text-sm font-semibold text-white rounded-lg cursor-pointer bg-emerald-600 hover:bg-emerald-500 active:scale-95 transition"
                    >
                        {panel_label}
                    </button>
                    <button
                        onclick={HandleTap}
                        class="px-4 py-2 text-sm font-semibold text-white rounded-lg cursor-pointer bg-blue-600 hover:bg-blue-500 active:scale-95 transition"
                    >
                        Tap Counter: {tap_count}
                    </button>
                    <button
                        onclick={CheckRef}
                        class="px-4 py-2 text-sm font-semibold text-white rounded-lg cursor-pointer bg-violet-600 hover:bg-violet-500 active:scale-95 transition"
                    >
                        Check data-psx-ref
                    </button>
                    <button
                        onclick={ProbeSignal}
                        class="px-4 py-2 text-sm font-semibold text-white rounded-lg cursor-pointer bg-amber-600 hover:bg-amber-500 active:scale-95 transition"
                    >
                        Probe State Signal
                    </button>
                    <span class="text-sm font-semibold text-slate-600">
                        ref={ref_label} • signal={signal_val}
                    </span>
                </div>

                {/* 01 overview — hero card: WAAPI enter + FLIP layout */}
                <section id="overview" class="min-h-[70vh] flex flex-col justify-center">
                    <div ref={hero_card_ref} id="hero-card">
                        {hero_card}
                    </div>
                    <p class="mt-4 text-sm text-slate-500">
                        The div above carries <code>ref={"{hero_card_ref}"}</code> →
                        <code> data-psx-ref="hero_card_ref"</code>. "Check data-psx-ref" resolves it
                        through <code>window.nextpy.getRef</code>.
                    </p>
                </section>

                {/* 02 motion section */}
                <section id="motion" class="min-h-[60vh]">
                    <span class="inline-block px-3 py-1 mb-4 text-xs font-semibold tracking-wider text-blue-700 uppercase rounded-full bg-blue-50">
                        Section 02 • Web Animations API
                    </span>
                    <h2 class={section_title}>Motion Primitive</h2>
                    <div class="grid gap-6 mt-8 md:grid-cols-2">
                        <Motion
                            className="p-6 bg-white border border-slate-200 rounded-2xl shadow-sm"
                            initial={{"opacity": 0, "transform": "translateX(-30px)"}}
                            animate={{"opacity": 1, "transform": "translateX(0px)"}}
                            transition={{"duration": 0.5, "delay": 0.1, "easing": "ease-out"}}
                        >
                            <h3 class="font-bold text-slate-900">Declarative &lt;Motion&gt;</h3>
                            <p class="mt-2 text-sm text-slate-600">
                                initial → animate keyframes via WAAPI. Try scrolling — the
                                MutationObserver initializes motion injected by conditionals.
                            </p>
                        </Motion>
                        <Motion
                            className="p-6 bg-white border border-slate-200 rounded-2xl shadow-sm"
                            initial={{"opacity": 0, "transform": "scale(0.8)"}}
                            animate={{"opacity": 1, "transform": "scale(1)"}}
                            whileHover={{"scale": 1.04}}
                            transition={{"duration": 0.25}}
                        >
                            <h3 class="font-bold text-slate-900">whileHover + whileTap</h3>
                            <p class="mt-2 text-sm text-slate-600">
                                Hover or press this card — gesture animations run on the
                                compositor with zero React.
                            </p>
                        </Motion>
                    </div>
                </section>

                {/* 03 AnimatePresence */}
                <section id="panel" class="min-h-[50vh]">
                    <span class="inline-block px-3 py-1 mb-4 text-xs font-semibold tracking-wider text-blue-700 uppercase rounded-full bg-blue-50">
                        Section 03 • Exit Animations
                    </span>
                    <h2 class={section_title}>AnimatePresence</h2>
                    <p class="max-w-2xl mt-2 text-slate-600">
                        Toggle the panel above. On close, the runtime plays the exit keyframes,
                        <em> then</em> swaps the DOM — no layout snap.
                    </p>
                    <div class="mt-8 max-w-md">
                        {if panel_open: {panel_html}}
                    </div>
                </section>

                {/* 04 lazy island */}
                <section id="island" class="min-h-[60vh]">
                    <span class="inline-block px-3 py-1 mb-4 text-xs font-semibold tracking-wider text-blue-700 uppercase rounded-full bg-blue-50">
                        Section 04 • Island Hydration
                    </span>
                    <h2 class={section_title}>Selective Hydration</h2>
                    <div class="mt-8 max-w-xl">
                        {lazy_widget}
                    </div>
                </section>

            </main>
        </div>
    )


default = Home
