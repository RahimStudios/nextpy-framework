"""Basics — entrance animations (fade, slide, scale, rotate, stagger)."""

from nextpy.psx import component, interactive_component, useState, Motion, Link, psx


DEMOS = [
    ("Fade", '''<Motion className="rounded-lg border border-zinc-700 bg-zinc-800 px-8 py-4 text-sm text-zinc-200"
    initial={{"opacity": 0}} animate={{"opacity": 1}} transition={{"duration": 0.7, "easing": "ease-out"}}>
    opacity 0 → 1
</Motion>'''),
    ("Slide", '''<Motion className="rounded-lg border border-zinc-700 bg-zinc-800 px-8 py-4 text-sm text-zinc-200"
    initial={{"opacity": 0, "y": 24}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.6, "easing": "ease-out"}}>
    translateY 24px → 0
</Motion>'''),
    ("Scale", '''<Motion className="rounded-lg border border-zinc-700 bg-zinc-800 px-8 py-4 text-sm text-zinc-200"
    initial={{"opacity": 0, "scale": 0.8}} animate={{"opacity": 1, "scale": 1}}
    transition={{"duration": 0.5, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}>
    spring pop
</Motion>'''),
    ("Rotate", '''<Motion className="rounded-lg border border-zinc-700 bg-zinc-800 px-8 py-4 text-sm text-zinc-200"
    initial={{"opacity": 0, "rotate": -6}} animate={{"opacity": 1, "rotate": 0}} transition={{"duration": 0.6}}>
    rotate -6° → 0
</Motion>'''),
    ("Slide + fade", '''<Motion className="rounded-lg bg-blue-600 px-8 py-4 text-sm font-semibold text-white shadow-lg shadow-blue-600/30"
    initial={{"opacity": 0, "x": -32}} animate={{"opacity": 1, "x": 0}} transition={{"duration": 0.55, "easing": "ease-out"}}>
    combined entrance
</Motion>'''),
    ("Stagger", '''<div className="flex gap-2">
    <Motion className="h-10 w-10 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 12}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0}} />
    <Motion className="h-10 w-10 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 12}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0.08}} />
    <Motion className="h-10 w-10 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 12}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0.16}} />
    <Motion className="h-10 w-10 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 12}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0.24}} />
    <Motion className="h-10 w-10 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 12}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0.32}} />
</div>'''),
]

CODE_SNIPPET = '''<Motion
    className="..."
    initial={{"opacity": 0, "y": 24}}      # from
    animate={{"opacity": 1, "y": 0}}       # to — scalar or [keyframes]
    transition={{"duration": 0.5, "easing": "ease-out", "delay": 0.1}}
>
    ...
</Motion>'''


def _cards():
    """Card markup: Replay toggles show_i → {if}/{else} swaps the demo
    instance → remount → entrance replays. Pure PSX, no custom JS."""
    out = []
    for i, (label, markup) in enumerate(DEMOS):
        out.append(
            '<div><p class="mb-2 text-xs font-medium text-zinc-500">' + label + '</p>'
            '<div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">'
            '<div class="flex items-center justify-between border-b border-zinc-800/60 px-4 py-2.5">'
            '<span class="text-xs font-medium uppercase tracking-wider text-zinc-500">' + label + '</span>'
            '<button type="button" onclick={Replay' + str(i) + '} '
            'class="rounded-md border border-zinc-700 bg-zinc-800/80 px-2.5 py-1 text-xs font-medium text-zinc-400 transition-colors hover:border-zinc-600 hover:text-zinc-200">Replay</button>'
            '</div>'
            '<div class="flex h-44 items-center justify-center p-6">'
            '{if show_' + str(i) + ':\n' + markup + '\n{else:\n' + markup + '\n}'
            '</div></div></div>')
    return "".join(out)


@interactive_component
def Page(props=None):
    props = props or {}
    [show_0, set_show_0] = useState(True)
    [show_1, set_show_1] = useState(True)
    [show_2, set_show_2] = useState(True)
    [show_3, set_show_3] = useState(True)
    [show_4, set_show_4] = useState(True)
    [show_5, set_show_5] = useState(True)

    def Replay0(e):
        set_show_0(not show_0)

    def Replay1(e):
        set_show_1(not show_1)

    def Replay2(e):
        set_show_2(not show_2)

    def Replay3(e):
        set_show_3(not show_3)

    def Replay4(e):
        set_show_4(not show_4)

    def Replay5(e):
        set_show_5(not show_5)

    code_v = CODE_SNIPPET
    page_jsx = '''<div class="mx-auto max-w-5xl px-6 py-16">
        <nav class="mb-8 flex items-center gap-2 text-sm text-zinc-500">
            <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
            <span class="text-zinc-700">/</span>
            <span class="text-zinc-300">Basics</span>
        </nav>
        <header class="mb-10 max-w-2xl">
            <h1 class="text-2xl font-semibold tracking-tight text-white">Entrance animations</h1>
            <p class="mt-2 text-[15px] leading-relaxed text-zinc-500">
                <code class="font-mono text-[13px] text-zinc-400">initial</code> is the from-state applied before mount,
                <code class="font-mono text-[13px] text-zinc-400"> animate</code> the target. Hit Replay to re-run any demo.
            </p>
        </header>
        <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            CARDS_HERE
        </div>
        <div class="mt-12">
            <h2 class="mb-3 text-xs font-medium uppercase tracking-wider text-zinc-600">The pattern</h2>
            <pre class="overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-950 p-5 font-mono text-[13px] leading-6 text-zinc-300"><code>{code_v}</code></pre>
        </div>
    </div>'''.replace("CARDS_HERE", _cards())

    return psx(page_jsx)
