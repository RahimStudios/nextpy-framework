"""Interactive NextPy Page: Scroll-Spy Sidebar & Pure Tailwind PSX Animations"""

from nextpy.psx import interactive_component, interactive_component as component, useState, useEffect


@interactive_component
def Home(props=None):
    props = props or {}
    title = props.get("title", "NextPy Interactive Motion")
    message = props.get(
        "message",
        "Scroll down to watch the sidebar links, progress bar, and cards react instantly "
        "with pure Tailwind classes in PSX.",
    )

    # ------------------------------------------------------------------ state
    [activeSection, setActiveSection] = useState("overview")
    [scrollProgress, setScrollProgress] = useState(0)
    [sidebarOpen, setSidebarOpen] = useState(True)

    [count, setCounter] = useState(0)
    [isToggled, setIsToggled] = useState(False)
    [activeTab, setActiveTab] = useState(0)
    [cardsVisible, setCardsVisible] = useState(False)
    [openAccordion, setOpenAccordion] = useState(0)

    # --------------------------------------------------------------- effects
    def SetupScrollEffects():
        def OnScroll():
            scrollTop = window.scrollY
            docHeight = document.documentElement.scrollHeight - window.innerHeight
            if docHeight > 0:
                setScrollProgress((scrollTop / docHeight) * 100)

            for sec_id in ["overview", "tabs", "cards", "accordion"]:
                el = document.getElementById(sec_id)
                if el:
                    rect = el.getBoundingClientRect()
                    if rect.top <= 220 and rect.bottom >= 220:
                        setActiveSection(sec_id)

            cards_el = document.getElementById("cards")
            if cards_el:
                crect = cards_el.getBoundingClientRect()
                if crect.top <= window.innerHeight * 0.8:
                    setCardsVisible(True)

        window.addEventListener("scroll", OnScroll)
        OnScroll()
        return lambda: window.removeEventListener("scroll", OnScroll)

    useEffect(SetupScrollEffects, [])

    # -------------------------------------------------------------- handlers
    def ToggleSidebar():
        setSidebarOpen(not sidebarOpen)

    def HandleCount():
        setCounter(count + 5)

    def ResetCounter():
        setCounter(0)

    def HandleToggle():
        setIsToggled(not isToggled)

    def SelectTab0():
        setActiveTab(0)

    def SelectTab1():
        setActiveTab(1)

    def SelectTab2():
        setActiveTab(2)

    def ToggleAcc0():
        setOpenAccordion(-1 if openAccordion == 0 else 0)

    def ToggleAcc1():
        setOpenAccordion(-1 if openAccordion == 1 else 1)

    def ToggleAcc2():
        setOpenAccordion(-1 if openAccordion == 2 else 2)

    def GoOverview():
        setActiveSection("overview")

    def GoTabs():
        setActiveSection("tabs")

    def GoCards():
        setActiveSection("cards")

    def GoAccordion():
        setActiveSection("accordion")

    # --------------------------------------------------------- derived values
    tab_title = (
        "Instant State Sync"
        if activeTab == 0
        else ("Hardware-Accelerated Motion" if activeTab == 1 else "Scroll-Spy Observer")
    )
    tab_stat = (
        "0ms Latency"
        if activeTab == 0
        else ("60+ FPS" if activeTab == 1 else "Native DOM")
    )
    tab_desc = (
        "NextPy PSX updates the DOM immediately on click with zero server round-trips, "
        "driving smooth Tailwind transitions."
        if activeTab == 0
        else (
            "Animating transform and opacity runs directly on the browser GPU compositor "
            "thread without dropping frames."
            if activeTab == 1
            else "Tracks section bounding boxes natively on scroll to highlight the "
            "matching sidebar link automatically."
        )
    )

    nav_link_base = "flex items-center justify-between px-4 py-3 rounded-xl font-medium transition-all duration-300"
    nav_link_active = f"{nav_link_base} bg-blue-600 text-white shadow-lg shadow-blue-600/30 translate-x-1"
    nav_link_idle = f"{nav_link_base} text-slate-400 hover:text-white hover:bg-slate-800/70"

    tab_pill_base = (
        "absolute top-1.5 bottom-1.5 w-[calc(33.333%-4px)] bg-blue-600 rounded-xl "
        "shadow-md transition-transform duration-300 ease-out"
    )
    tab_pill_class = (
        f"{tab_pill_base} translate-x-0"
        if activeTab == 0
        else (
            f"{tab_pill_base} translate-x-[calc(100%+4px)]"
            if activeTab == 1
            else f"{tab_pill_base} translate-x-[calc(200%+8px)]"
        )
    )

    tab_btn_base = "relative z-10 py-3 text-sm md:text-base font-semibold rounded-xl cursor-pointer transition-colors duration-200"
    tab_btn_active = f"{tab_btn_base} text-white"
    tab_btn_idle = f"{tab_btn_base} text-slate-600 hover:text-slate-900"

    card_base = "p-6 rounded-2xl border border-slate-200 bg-slate-50 transition-all duration-500 ease-out"
    card_visible = f"{card_base} hover:bg-white hover:shadow-xl hover:-translate-y-1.5 opacity-100 translate-y-0 scale-100"
    card_hidden = f"{card_base} opacity-0 translate-y-8 scale-95"

    acc_panel = "grid transition-all duration-300 ease-in-out"
    acc_panel_open = f"{acc_panel} grid-rows-[1fr] opacity-100"
    acc_panel_closed = f"{acc_panel} grid-rows-[0fr] opacity-0"

    acc_icon = "ml-4 text-blue-600 font-bold text-xl transition-transform duration-300"

    # ---------------------------------------------------------------- render
    return (
        <div class="flex min-h-screen font-sans antialiased text-slate-900 bg-slate-50 selection:bg-blue-600 selection:text-white">

            {/* Scroll progress bar */}
            <div class="fixed top-0 left-0 right-0 z-50 h-1 bg-slate-200">
                <div
                    style={{"width": f"{scrollProgress}%"}}
                    class="h-full bg-gradient-to-r from-blue-600 via-indigo-500 to-cyan-400 transition-all duration-150 ease-out"
                ></div>
            </div>

            {/* Sidebar */}
            <aside
                class={
                    "sticky top-0 h-screen bg-slate-900 text-white flex flex-col justify-between overflow-hidden transition-all duration-300 ease-out w-72 p-6 opacity-100"
                    if sidebarOpen
                    else "sticky top-0 h-screen bg-slate-900 text-white flex flex-col justify-between overflow-hidden transition-all duration-300 ease-out w-0 p-0 opacity-0"
                }
            >
                <div>
                    <div class="flex items-center justify-between pb-6 mb-6 border-b border-slate-800">
                        <div>
                            <h2 class="text-xl font-bold tracking-tight text-white">NextPy Docs</h2>
                            <p class="mt-1 text-xs text-slate-400">Scroll-Spy &amp; Instant UI</p>
                        </div>
                        <button
                            onclick={ToggleSidebar}
                            class="px-2.5 py-1 text-xs font-semibold text-white bg-slate-800 rounded-lg cursor-pointer hover:bg-slate-700"
                        >
                            X
                        </button>
                    </div>

                    <nav class="flex flex-col space-y-2">
                        <a href="#overview" onclick={GoOverview}
                           class={nav_link_active if activeSection == "overview" else nav_link_idle}>
                            <span>Overview</span>
                            <span class="font-mono text-xs">01</span>
                        </a>
                        <a href="#tabs" onclick={GoTabs}
                           class={nav_link_active if activeSection == "tabs" else nav_link_idle}>
                            <span>Animated Tabs</span>
                            <span class="font-mono text-xs">02</span>
                        </a>
                        <a href="#cards" onclick={GoCards}
                           class={nav_link_active if activeSection == "cards" else nav_link_idle}>
                            <span>Reveal Cards</span>
                            <span class="font-mono text-xs">03</span>
                        </a>
                        <a href="#accordion" onclick={GoAccordion}
                           class={nav_link_active if activeSection == "accordion" else nav_link_idle}>
                            <span>Accordion</span>
                            <span class="font-mono text-xs">04</span>
                        </a>
                    </nav>
                </div>

                <div class="p-4 space-y-3 border rounded-xl bg-slate-800/80 border-slate-700/60">
                    <div class="flex items-center justify-between text-xs text-slate-400">
                        <span>Active Section</span>
                        <span class="font-mono text-blue-400 uppercase">#{activeSection}</span>
                    </div>
                    <button
                        onclick={ResetCounter}
                        class="w-full py-2 text-xs font-semibold text-white transition rounded-lg cursor-pointer bg-slate-700 hover:bg-slate-600 active:scale-95"
                    >
                        Reset Counter ({count})
                    </button>
                </div>
            </aside>

            {/* Main content */}
            <main class="flex-1 px-6 py-12 space-y-32 md:px-12">

                <div class="flex items-center justify-between p-4 bg-white border rounded-2xl border-slate-200 shadow-sm">
                    <button
                        onclick={ToggleSidebar}
                        class="px-4 py-2 text-sm font-semibold text-white transition-transform rounded-lg cursor-pointer bg-slate-900 active:scale-95"
                    >
                        {"Hide Sidebar" if sidebarOpen else "Show Sidebar"}
                    </button>
                    <span class="text-sm font-bold text-slate-700">Active: #{activeSection}</span>
                </div>

                {/* ---------------------------------------------------- 01 Overview */}
                <section id="overview"
                         class="min-h-[85vh] flex flex-col justify-center p-8 md:p-12 bg-white border border-slate-200 rounded-3xl shadow-sm">
                    <span class="inline-block px-3 py-1 mb-4 text-xs font-semibold tracking-wider text-blue-700 uppercase rounded-full w-fit bg-blue-50">
                        Section 01 • Scroll Spy Active
                    </span>
                    <h1 class="text-4xl font-extrabold tracking-tight md:text-5xl text-slate-900">{title}</h1>
                    <p class="max-w-2xl mt-4 text-lg leading-relaxed text-slate-600">{message}</p>

                    <div class="flex flex-wrap items-center gap-4 mt-8">
                        <button
                            onclick={HandleCount}
                            class="px-6 py-3.5 font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-md shadow-blue-600/20 cursor-pointer transition-all duration-200 hover:-translate-y-0.5 active:scale-95"
                        >
                            Increment Count: {count}
                        </button>

                        <button
                            onclick={HandleToggle}
                            class={
                                "px-6 py-3.5 font-semibold text-white rounded-xl shadow-md cursor-pointer transition-all duration-300 hover:-translate-y-0.5 active:scale-95 bg-emerald-600 shadow-emerald-600/20"
                                if isToggled
                                else "px-6 py-3.5 font-semibold text-white rounded-xl shadow-md cursor-pointer transition-all duration-300 hover:-translate-y-0.5 active:scale-95 bg-rose-600 shadow-rose-600/20"
                            }
                        >
                            Status: {isToggled}
                        </button>
                    </div>
                </section>

                {/* -------------------------------------------------------- 02 Tabs */}
                <section id="tabs"
                         class="min-h-[85vh] flex flex-col justify-center p-8 md:p-12 bg-white border border-slate-200 rounded-3xl shadow-sm">
                    <span class="inline-block px-3 py-1 mb-4 text-xs font-semibold tracking-wider text-blue-700 uppercase rounded-full w-fit bg-blue-50">
                        Section 02 • Spring Tab Indicator
                    </span>
                    <h2 class="text-3xl font-extrabold tracking-tight md:text-4xl text-slate-900">Instant Sliding Tabs</h2>

                    <div class="relative grid grid-cols-3 gap-1 p-1.5 mt-8 bg-slate-100 rounded-2xl">
                        <div class={tab_pill_class}></div>

                        <button onclick={SelectTab0}
                                class={tab_btn_active if activeTab == 0 else tab_btn_idle}>
                            Instant State Sync
                        </button>
                        <button onclick={SelectTab1}
                                class={tab_btn_active if activeTab == 1 else tab_btn_idle}>
                            GPU Motion
                        </button>
                        <button onclick={SelectTab2}
                                class={tab_btn_active if activeTab == 2 else tab_btn_idle}>
                            Scroll Spy
                        </button>
                    </div>

                    <div class="mt-8">
                        <div class="flex flex-wrap items-center gap-3">
                            <h3 class="text-xl font-bold text-slate-900">{tab_title}</h3>
                            <span class="px-2.5 py-1 text-xs font-semibold rounded-full text-emerald-700 bg-emerald-50">
                                {tab_stat}
                            </span>
                        </div>
                        <p class="max-w-2xl mt-2 leading-relaxed text-slate-600">{tab_desc}</p>
                    </div>
                </section>

                {/* ------------------------------------------------------- 03 Cards */}
                <section id="cards"
                         class="min-h-[85vh] flex flex-col justify-center p-8 md:p-12 bg-white border border-slate-200 rounded-3xl shadow-sm">
                    <span class="inline-block px-3 py-1 mb-4 text-xs font-semibold tracking-wider text-blue-700 uppercase rounded-full w-fit bg-blue-50">
                        Section 03 • Viewport Entrance
                    </span>
                    <h2 class="text-3xl font-extrabold tracking-tight md:text-4xl text-slate-900">
                        Scroll-Triggered Staggered Cards
                    </h2>

                    <div class="grid gap-6 mt-10 md:grid-cols-3">
                        <div class={
                            "p-6 rounded-2xl border border-slate-200 bg-slate-50 hover:bg-white hover:shadow-xl hover:-translate-y-1.5 transition-all duration-500 ease-out delay-75 opacity-100 translate-y-0 scale-100"
                            if cardsVisible
                            else f"{card_hidden} delay-75"
                        }>
                            <span class="font-mono text-xs text-blue-600">01</span>
                            <h3 class="mt-2 text-lg font-bold text-slate-900">Zero-Lag Hydration</h3>
                            <p class="mt-2 text-sm leading-relaxed text-slate-600">
                                Components attach event listeners cleanly on mount without flickering.
                            </p>
                        </div>

                        <div class={
                            "p-6 rounded-2xl border border-slate-200 bg-slate-50 hover:bg-white hover:shadow-xl hover:-translate-y-1.5 transition-all duration-500 ease-out delay-200 opacity-100 translate-y-0 scale-100"
                            if cardsVisible
                            else f"{card_hidden} delay-200"
                        }>
                            <span class="font-mono text-xs text-blue-600">02</span>
                            <h3 class="mt-2 text-lg font-bold text-slate-900">Tailwind Arbitrary JIT</h3>
                            <p class="mt-2 text-sm leading-relaxed text-slate-600">
                                Full support for arbitrary Tailwind classes like grid-rows-[1fr] and
                                translate-x-[calc(...)].
                            </p>
                        </div>

                        <div class={
                            "p-6 rounded-2xl border border-slate-200 bg-slate-50 hover:bg-white hover:shadow-xl hover:-translate-y-1.5 transition-all duration-500 ease-out delay-300 opacity-100 translate-y-0 scale-100"
                            if cardsVisible
                            else f"{card_hidden} delay-300"
                        }>
                            <span class="font-mono text-xs text-blue-600">03</span>
                            <h3 class="mt-2 text-lg font-bold text-slate-900">Declarative PSX</h3>
                            <p class="mt-2 text-sm leading-relaxed text-slate-600">
                                Change a single state value in Python and let PSX update the DOM diff.
                            </p>
                        </div>
                    </div>
                </section>

                {/* --------------------------------------------------- 04 Accordion */}
                <section id="accordion"
                         class="min-h-[85vh] flex flex-col justify-center p-8 md:p-12 bg-white border border-slate-200 rounded-3xl shadow-sm">
                    <span class="inline-block px-3 py-1 mb-4 text-xs font-semibold tracking-wider text-blue-700 uppercase rounded-full w-fit bg-blue-50">
                        Section 04 • Smooth Height Collapse
                    </span>
                    <h2 class="text-3xl font-extrabold tracking-tight md:text-4xl text-slate-900">
                        Instant Animated Accordion
                    </h2>

                    <div class="mt-10 space-y-3">
                        {/* Item 1 */}
                        <div class="overflow-hidden border border-slate-200 rounded-2xl bg-slate-50">
                            <button
                                onclick={ToggleAcc0}
                                class="flex items-center justify-between w-full px-6 py-5 text-left font-semibold text-slate-900 cursor-pointer transition-colors duration-200 hover:bg-slate-100"
                            >
                                How do sidebar links change color automatically on scroll?
                                <span class={f"{acc_icon} rotate-45" if openAccordion == 0 else f"{acc_icon} rotate-0"}>
                                    +
                                </span>
                            </button>
                            <div class={acc_panel_open if openAccordion == 0 else acc_panel_closed}>
                                <div class="overflow-hidden">
                                    <p class="px-6 pb-5 text-sm leading-relaxed text-slate-600">
                                        useEffect registers a scroll listener that checks each section's
                                        bounding box and updates activeSection via setActiveSection().
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Item 2 */}
                        <div class="overflow-hidden border border-slate-200 rounded-2xl bg-slate-50">
                            <button
                                onclick={ToggleAcc1}
                                class="flex items-center justify-between w-full px-6 py-5 text-left font-semibold text-slate-900 cursor-pointer transition-colors duration-200 hover:bg-slate-100"
                            >
                                How does the sliding tab pill animate smoothly?
                                <span class={f"{acc_icon} rotate-45" if openAccordion == 1 else f"{acc_icon} rotate-0"}>
                                    +
                                </span>
                            </button>
                            <div class={acc_panel_open if openAccordion == 1 else acc_panel_closed}>
                                <div class="overflow-hidden">
                                    <p class="px-6 pb-5 text-sm leading-relaxed text-slate-600">
                                        An absolute-positioned background pill swaps arbitrary Tailwind
                                        translate-x-[calc(...)] classes with transition-transform
                                        duration-300 ease-out.
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Item 3 */}
                        <div class="overflow-hidden border border-slate-200 rounded-2xl bg-slate-50">
                            <button
                                onclick={ToggleAcc2}
                                class="flex items-center justify-between w-full px-6 py-5 text-left font-semibold text-slate-900 cursor-pointer transition-colors duration-200 hover:bg-slate-100"
                            >
                                Does NextPy compile arbitrary Tailwind grid-rows-[1fr] classes?
                                <span class={f"{acc_icon} rotate-45" if openAccordion == 2 else f"{acc_icon} rotate-0"}>
                                    +
                                </span>
                            </button>
                            <div class={acc_panel_open if openAccordion == 2 else acc_panel_closed}>
                                <div class="overflow-hidden">
                                    <p class="px-6 pb-5 text-sm leading-relaxed text-slate-600">
                                        Yes—NextPy compiles arbitrary Tailwind classes natively, letting
                                        you use grid-rows-[0fr] to grid-rows-[1fr] for smooth height
                                        collapse.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

            </main>
        </div>
    )


def getServerSideProps(context):
    return {
        "props": {
            "title": "NextPy Interactive Motion",
            "message": "Scroll down to watch the sidebar links, progress bar, and cards react "
            "instantly with pure Tailwind classes in PSX.",
        }
    }


default = Home