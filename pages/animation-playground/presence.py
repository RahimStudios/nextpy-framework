"""AnimatePresence — exit animations when elements leave the DOM."""

from nextpy.psx import component, interactive_component, useState, Motion, AnimatePresence, Link


@interactive_component
def ExitDemos():
    [card, set_card] = useState(True)
    [toast, set_toast] = useState(True)
    [badge, set_badge] = useState(True)

    def ToggleCard(e):
        set_card(not card)

    def ToggleToast(e):
        set_toast(not toast)

    def ToggleBadge(e):
        set_badge(not badge)

    btn = "rounded-lg border border-zinc-700 bg-zinc-800 px-3.5 py-1.5 text-xs font-medium text-zinc-300 transition-colors hover:bg-zinc-700"

    return (
        <div class="grid gap-5 sm:grid-cols-3">
            <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
                <div class="flex items-center justify-between border-b border-zinc-800/60 px-4 py-2.5">
                    <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">Fade + scale</span>
                    <button type="button" onclick={ToggleCard} class={btn}>Toggle</button>
                </div>
                <div class="flex h-44 items-center justify-center p-6">
                    <AnimatePresence>
                        {if card:
                            <Motion
                                initial={{"opacity": 0, "scale": 0.85, "y": 12}}
                                animate={{"opacity": 1, "scale": 1, "y": 0}}
                                exit={{"opacity": 0, "scale": 0.9, "y": -12}}
                                transition={{"duration": 0.35, "easing": "ease-in-out"}}
                                className="w-full rounded-lg border border-blue-500/40 bg-blue-500/10 p-4 text-center">
                                <p class="text-sm font-semibold text-blue-200">Card</p>
                                <p class="mt-1 text-xs text-zinc-400">fades + shrinks out</p>
                            </Motion>
                        }
                        {if not card:
                            <Motion initial={{"opacity": 0}} animate={{"opacity": 1}} className="text-xs text-zinc-600">removed</Motion>
                        }
                    </AnimatePresence>
                </div>
            </div>

            <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
                <div class="flex items-center justify-between border-b border-zinc-800/60 px-4 py-2.5">
                    <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">Slide out</span>
                    <button type="button" onclick={ToggleToast} class={btn}>Toggle</button>
                </div>
                <div class="flex h-44 items-center justify-center p-6">
                    <AnimatePresence>
                        {if toast:
                            <Motion
                                initial={{"opacity": 0, "x": -30}}
                                animate={{"opacity": 1, "x": 0}}
                                exit={{"opacity": 0, "x": 40}}
                                transition={{"duration": 0.3, "easing": "ease-in-out"}}
                                className="w-full rounded-lg border border-emerald-500/40 bg-emerald-500/10 p-4 text-center">
                                <p class="text-sm font-semibold text-emerald-200">Toast</p>
                                <p class="mt-1 text-xs text-zinc-400">slides off to the right</p>
                            </Motion>
                        }
                        {if not toast:
                            <Motion initial={{"opacity": 0}} animate={{"opacity": 1}} className="text-xs text-zinc-600">removed</Motion>
                        }
                    </AnimatePresence>
                </div>
            </div>

            <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
                <div class="flex items-center justify-between border-b border-zinc-800/60 px-4 py-2.5">
                    <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">Collapse</span>
                    <button type="button" onclick={ToggleBadge} class={btn}>Toggle</button>
                </div>
                <div class="flex h-44 items-center justify-center p-6">
                    <AnimatePresence>
                        {if badge:
                            <Motion
                                initial={{"opacity": 0, "scale": 0.6}}
                                animate={{"opacity": 1, "scale": 1}}
                                exit={{"opacity": 0, "scale": 0.4}}
                                transition={{"duration": 0.3, "easing": "ease-in-out"}}
                                className="flex h-16 w-16 items-center justify-center rounded-full border border-violet-500/40 bg-violet-500/15 text-xl">
                                64
                            </Motion>
                        }
                        {if not badge:
                            <Motion initial={{"opacity": 0}} animate={{"opacity": 1}} className="text-xs text-zinc-600">removed</Motion>
                        }
                    </AnimatePresence>
                </div>
            </div>
        </div>
    )


@component
def Page():
    code = '''from nextpy.psx import AnimatePresence, Motion

<AnimatePresence>
    {if open:
        <Motion
            initial={{"opacity": 0, "scale": 0.85}}
            animate={{"opacity": 1, "scale": 1}}
            exit={{"opacity": 0, "scale": 0.9}}
            transition={{"duration": 0.35}}
        >
            ...content...
        </Motion>
    }
</AnimatePresence>'''

    return (
        <div class="mx-auto max-w-5xl px-6 py-16">
            <nav class="mb-8 flex items-center gap-2 text-sm text-zinc-500">
                <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
                <span class="text-zinc-700">/</span>
                <span class="text-zinc-300">AnimatePresence</span>
            </nav>
            <header class="mb-10 max-w-2xl">
                <h1 class="text-2xl font-semibold tracking-tight text-white">Exit animations</h1>
                <p class="mt-2 text-[15px] leading-relaxed text-zinc-500">
                    <code class="font-mono text-[13px] text-zinc-400">exit</code> plays when a Motion element leaves the DOM —
                    the runtime waits for it before swapping the conditional. Wrap the block in
                    <code class="font-mono text-[13px] text-zinc-400"> AnimatePresence</code> and try the buttons.
                </p>
            </header>

            <div class="mb-10">
                <ExitDemos />
            </div>

            <div class="grid gap-5 lg:grid-cols-5">
                <div class="lg:col-span-3">
                    <h2 class="mb-3 text-xs font-medium uppercase tracking-wider text-zinc-600">Usage</h2>
                    <pre class="overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-950 p-5 font-mono text-[12px] leading-5 text-zinc-300"><code>{code}</code></pre>
                </div>
                <div class="lg:col-span-2">
                    <h2 class="mb-3 text-xs font-medium uppercase tracking-wider text-zinc-600">How it works</h2>
                    <div class="space-y-3 rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 text-sm leading-relaxed text-zinc-400">
                        <p><span class="font-medium text-zinc-200">1.</span> State flips → the conditional re-evaluates.</p>
                        <p><span class="font-medium text-zinc-200">2.</span> The runtime finds exiting <code class="font-mono text-[13px] text-zinc-300">[data-psx-motion]</code> elements with an <code class="font-mono text-[13px] text-zinc-300">exit</code> config.</p>
                        <p><span class="font-medium text-zinc-200">3.</span> It plays the exit animation, <em>then</em> swaps the DOM — no pop-out.</p>
                    </div>
                </div>
            </div>
        </div>
    )
