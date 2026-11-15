"""Layout animations (FLIP) — sections glide when siblings resize."""

from nextpy.psx import component, interactive_component, useState, Motion, Link


@interactive_component
def FlipDemo():
    [open_0, set_open_0] = useState(True)
    [open_1, set_open_1] = useState(False)
    [open_2, set_open_2] = useState(False)

    def Toggle0(e):
        set_open_0(not open_0)

    def Toggle1(e):
        set_open_1(not open_1)

    def Toggle2(e):
        set_open_2(not open_2)

    btn_cls = "flex w-full items-center justify-between px-5 py-4 text-left transition-colors hover:bg-zinc-800/50"
    panel_cls = "border-t border-zinc-800/60 px-5 py-4 pl-14 text-sm leading-relaxed text-zinc-400"

    return (
        <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
            <Motion layout={True} transition={{"duration": 0.45, "easing": "ease-in-out"}}
                    className="border-b border-zinc-800/60">
                <button type="button" onclick={Toggle0} class={btn_cls}>
                    <span class="flex items-center gap-3">
                        <span class="flex h-6 w-6 items-center justify-center rounded-md border border-zinc-800 bg-zinc-950 text-[11px] font-semibold text-zinc-500">01</span>
                        <span>
                            <span class="block text-sm font-semibold text-zinc-100">First measurement</span>
                            <span class="block text-xs text-zinc-500">Snapshot every layout element's box</span>
                        </span>
                    </span>
                    {if open_0: <span class="text-zinc-500">▾</span>}{if not open_0: <span class="text-zinc-600">▸</span>}
                </button>
                {if open_0:
                    <div class={panel_cls}>
                        The runtime records each element's bounding box before the DOM changes — the 'First' in FLIP.
                    </div>
                }
            </Motion>

            <Motion layout={True} transition={{"duration": 0.45, "easing": "ease-in-out"}}
                    className="border-b border-zinc-800/60">
                <button type="button" onclick={Toggle1} class={btn_cls}>
                    <span class="flex items-center gap-3">
                        <span class="flex h-6 w-6 items-center justify-center rounded-md border border-zinc-800 bg-zinc-950 text-[11px] font-semibold text-zinc-500">02</span>
                        <span>
                            <span class="block text-sm font-semibold text-zinc-100">DOM mutation</span>
                            <span class="block text-xs text-zinc-500">State change re-renders the conditional</span>
                        </span>
                    </span>
                    {if open_1: <span class="text-zinc-500">▾</span>}{if not open_1: <span class="text-zinc-600">▸</span>}
                </button>
                {if open_1:
                    <div class={panel_cls}>
                        The conditional swap inserts or removes content — elements below shift position instantly. This is 'Last'.
                    </div>
                }
            </Motion>

            <Motion layout={True} transition={{"duration": 0.45, "easing": "ease-in-out"}}
                    className="">
                <button type="button" onclick={Toggle2} class={btn_cls}>
                    <span class="flex items-center gap-3">
                        <span class="flex h-6 w-6 items-center justify-center rounded-md border border-zinc-800 bg-zinc-950 text-[11px] font-semibold text-zinc-500">03</span>
                        <span>
                            <span class="block text-sm font-semibold text-zinc-100">Inverted delta</span>
                            <span class="block text-xs text-zinc-500">Compute how far each element moved</span>
                        </span>
                    </span>
                    {if open_2: <span class="text-zinc-500">▾</span>}{if not open_2: <span class="text-zinc-600">▸</span>}
                </button>
                {if open_2:
                    <div class={panel_cls}>
                        For every element the runtime computes first-box minus last-box and pre-translates by that delta — 'Invert', then 'Play'.
                    </div>
                }
            </Motion>
        </div>
    )


@component
def Page():
    code = '''# layout=True → FLIP handled by the runtime

<Motion layout={True} transition={{"duration": 0.45}}>
    ...conditional or reorderable content...
</Motion>

# any state-driven box change animates automatically'''

    return (
        <div class="mx-auto max-w-5xl px-6 py-16">
            <nav class="mb-8 flex items-center gap-2 text-sm text-zinc-500">
                <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
                <span class="text-zinc-700">/</span>
                <span class="text-zinc-300">Layout (FLIP)</span>
            </nav>
            <header class="mb-10 max-w-2xl">
                <h1 class="text-2xl font-semibold tracking-tight text-white">Layout animations — FLIP</h1>
                <p class="mt-2 text-[15px] leading-relaxed text-zinc-500">
                    <code class="font-mono text-[13px] text-zinc-400">layout=True</code> snapshots each element's box before a
                    state-driven DOM update and animates it to the new position. Click the sections — the ones below glide.
                </p>
            </header>

            <div class="mb-8 flex items-center gap-2">
                <span class="rounded-md border border-zinc-800 bg-zinc-900 px-2.5 py-1 text-xs font-medium text-zinc-400">First</span>
                <span class="text-zinc-700">→</span>
                <span class="rounded-md border border-zinc-800 bg-zinc-900 px-2.5 py-1 text-xs font-medium text-zinc-400">Last</span>
                <span class="text-zinc-700">→</span>
                <span class="rounded-md border border-zinc-800 bg-zinc-900 px-2.5 py-1 text-xs font-medium text-zinc-400">Invert</span>
                <span class="text-zinc-700">→</span>
                <span class="rounded-md border border-zinc-800 bg-zinc-900 px-2.5 py-1 text-xs font-medium text-zinc-400">Play</span>
            </div>

            <div class="grid gap-5 lg:grid-cols-5">
                <div class="lg:col-span-3">
                    <FlipDemo />
                </div>
                <div class="lg:col-span-2">
                    <h2 class="mb-3 text-xs font-medium uppercase tracking-wider text-zinc-600">Usage</h2>
                    <pre class="overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-950 p-5 font-mono text-[12px] leading-5 text-zinc-300"><code>{code}</code></pre>
                    <p class="mt-4 text-sm leading-relaxed text-zinc-500">
                        Works with any box change — conditional panels, grids, lists. Combine with
                        <code class="font-mono text-[13px] text-zinc-400"> whileHover</code> for reorder-on-hover polish.
                    </p>
                </div>
            </div>
        </div>
    )
