"""Keyframes & easings — multi-step sequences, easing curves, stagger."""

from nextpy.psx import component, interactive_component, useState, Motion, Link, psx


CARDS = [
    ("Bounce keyframes", '''<Motion className="h-14 w-14 rounded-full bg-blue-500 shadow-lg shadow-blue-500/40"
    animate={{"y": [0, -34, 0]}} transition={{"duration": 1.1, "easing": "ease-in-out", "repeat": 3}} />''',
     '''<Motion
    animate={{"y": [0, -34, 0]}}
    transition={{"duration": 1.1, "easing": "ease-in-out", "repeat": 3}}
/>'''),
    ("Multi-property path", '''<Motion className="h-12 w-12 rounded-lg bg-violet-500 shadow-lg shadow-violet-500/40"
    animate={{"x": [0, 90, 0], "rotate": [0, 180, 360]}} transition={{"duration": 2.4, "easing": "linear"}} />''',
     '''<Motion
    animate={{"x": [0, 90, 0], "rotate": [0, 180, 360]}}
    transition={{"duration": 2.4, "easing": "linear"}}
/>'''),
    ("Easing curves", '''<div className="w-full space-y-3">
    <Motion className="rounded-lg bg-zinc-800 px-4 py-2.5 text-sm text-zinc-300"
        initial={{"opacity": 0, "x": -40}} animate={{"opacity": 1, "x": 0}}
        transition={{"duration": 0.9, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}>spring — cubic-bezier(0.34,1.56,0.64,1)</Motion>
    <Motion className="rounded-lg bg-zinc-800 px-4 py-2.5 text-sm text-zinc-300"
        initial={{"opacity": 0, "x": -40}} animate={{"opacity": 1, "x": 0}}
        transition={{"duration": 0.9, "easing": "ease-in-out", "delay": 0.15}}>smooth — ease-in-out</Motion>
    <Motion className="rounded-lg bg-zinc-800 px-4 py-2.5 text-sm text-zinc-300"
        initial={{"opacity": 0, "x": -40}} animate={{"opacity": 1, "x": 0}}
        transition={{"duration": 0.9, "easing": "linear", "delay": 0.3}}>constant — linear</Motion>
</div>''',
     '''transition={{"duration": 0.9, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
transition={{"duration": 0.9, "easing": "ease-in-out", "delay": 0.15}}
transition={{"duration": 0.9, "easing": "linear", "delay": 0.3}}'''),
    ("Stagger", '''<div className="flex gap-2.5">
    <Motion className="h-11 w-11 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 14}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0.0}} />
    <Motion className="h-11 w-11 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 14}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0.08}} />
    <Motion className="h-11 w-11 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 14}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0.16}} />
    <Motion className="h-11 w-11 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 14}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0.24}} />
    <Motion className="h-11 w-11 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 14}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0.32}} />
    <Motion className="h-11 w-11 rounded-lg bg-blue-500/80" initial={{"opacity": 0, "y": 14}} animate={{"opacity": 1, "y": 0}} transition={{"duration": 0.4, "delay": 0.4}} />
</div>''',
     '''# stagger: delay = index * step
{for i, item in enumerate(items):
    <Motion
        initial={{"opacity": 0, "y": 14}}
        animate={{"opacity": 1, "y": 0}}
        transition={{"duration": 0.4, "delay": i * 0.08}}
    />
}'''),
]


def _cards():
    out = []
    for i, (label, demo, code) in enumerate(CARDS):
        out.append(
            '<div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">'
            '<div class="flex items-center justify-between border-b border-zinc-800/60 px-4 py-2.5">'
            '<span class="text-xs font-medium uppercase tracking-wider text-zinc-500">' + label + '</span>'
            '<button type="button" onclick={Replay' + str(i) + '} '
            'class="rounded-md border border-zinc-700 bg-zinc-800/80 px-2.5 py-1 text-xs font-medium text-zinc-400 transition-colors hover:border-zinc-600 hover:text-zinc-200">Replay</button>'
            '</div>'
            '<div class="flex h-48 items-center justify-center p-6">'
            '{if show_' + str(i) + ':\n' + demo + '\n{else:\n' + demo + '\n}'
            '</div>'
            '<pre class="overflow-x-auto border-t border-zinc-800/60 bg-zinc-950 p-4 font-mono text-[12px] leading-5 text-zinc-400"><code>{c' + str(i) + '_code}</code></pre>'
            '</div>')
    return "".join(out)


@interactive_component
def Page(props=None):
    props = props or {}
    [show_0, set_show_0] = useState(True)
    [show_1, set_show_1] = useState(True)
    [show_2, set_show_2] = useState(True)
    [show_3, set_show_3] = useState(True)

    def Replay0(e):
        set_show_0(not show_0)

    def Replay1(e):
        set_show_1(not show_1)

    def Replay2(e):
        set_show_2(not show_2)

    def Replay3(e):
        set_show_3(not show_3)

    page_jsx = '''<div class="mx-auto max-w-5xl px-6 py-16">
        <nav class="mb-8 flex items-center gap-2 text-sm text-zinc-500">
            <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
            <span class="text-zinc-700">/</span>
            <span class="text-zinc-300">Keyframes &amp; easings</span>
        </nav>
        <header class="mb-10 max-w-2xl">
            <h1 class="text-2xl font-semibold tracking-tight text-white">Keyframes, easings &amp; stagger</h1>
            <p class="mt-2 text-[15px] leading-relaxed text-zinc-500">
                Any animate value can be a keyframe array <code class="font-mono text-[13px] text-zinc-400">[from, mid, to]</code>.
                Transitions take <code class="font-mono text-[13px] text-zinc-400">duration</code>, <code class="font-mono text-[13px] text-zinc-400">delay</code> and
                <code class="font-mono text-[13px] text-zinc-400"> easing</code> — stagger by multiplying delay by index. Hit Replay on any card.
            </p>
        </header>
        <div class="grid gap-5 sm:grid-cols-2">
            CARDS_HERE
        </div>
    </div>'''.replace("CARDS_HERE", _cards())

    c0_code = CARDS[0][2]
    c1_code = CARDS[1][2]
    c2_code = CARDS[2][2]
    c3_code = CARDS[3][2]
    return psx(page_jsx)
