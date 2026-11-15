"""Gestures — whileHover / whileTap pointer animations."""

from nextpy.psx import component, interactive_component, Motion, Link


@interactive_component
def Page(props=None):
    props = props or {}

    hover_code = '''<Motion as="button"
    whileHover={{"scale": 1.05, "y": -3}}
    transition={{"duration": 0.2}}
>
    Hover me
</Motion>'''

    tap_code = '''<Motion as="button"
    whileTap={{"scale": 0.92}}
    transition={{"duration": 0.12}}
>
    Press me
</Motion>'''

    card_code = '''<Motion
    whileHover={{"y": -6, "boxShadow": "0 16px 40px rgba(0,0,0,0.5)"}}
    transition={{"duration": 0.25}}
>
    <div class="p-5">…card content…</div>
</Motion>'''

    combo_code = '''<Motion as="button"
    whileHover={{"scale": 1.06, "y": -3}}
    whileTap={{"scale": 0.94}}
    transition={{"duration": 0.18}}
>
    Hover & tap
</Motion>'''

    icon_code = '''<Motion as="button"
    whileHover={{"rotate": 20}}
    whileTap={{"scale": 0.85}}
    transition={{"duration": 0.2}}
>
    ⚡
</Motion>'''

    return (
        <div class="mx-auto max-w-5xl px-6 py-16">
            <nav class="mb-8 flex items-center gap-2 text-sm text-zinc-500">
                <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
                <span class="text-zinc-700">/</span>
                <span class="text-zinc-300">Gestures</span>
            </nav>
            <header class="mb-10 max-w-2xl">
                <h1 class="text-2xl font-semibold tracking-tight text-white">Pointer gestures</h1>
                <p class="mt-2 text-[15px] leading-relaxed text-zinc-500">
                    <code class="font-mono text-[13px] text-zinc-400">whileHover</code> and
                    <code class="font-mono text-[13px] text-zinc-400"> whileTap</code> animate on pointer enter/leave and
                    press/release — they revert automatically when the gesture ends. Hover and press the demos.
                </p>
            </header>

            <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
                    <div class="border-b border-zinc-800/60 px-4 py-2.5">
                        <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">whileHover</span>
                    </div>
                    <div class="flex h-44 items-center justify-center p-6">
                        <Motion as="button" whileHover={{"scale": 1.08, "y": -4}} transition={{"duration": 0.2}}
                                className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-600/30">
                            Hover me
                        </Motion>
                    </div>
                    <pre class="overflow-x-auto border-t border-zinc-800/60 bg-zinc-950 p-4 font-mono text-[12px] leading-5 text-zinc-400"><code>{hover_code}</code></pre>
                </div>

                <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
                    <div class="border-b border-zinc-800/60 px-4 py-2.5">
                        <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">whileTap</span>
                    </div>
                    <div class="flex h-44 items-center justify-center p-6">
                        <Motion as="button" whileTap={{"scale": 0.88}} transition={{"duration": 0.12}}
                                className="rounded-xl border border-zinc-700 bg-zinc-800 px-6 py-3 text-sm font-semibold text-zinc-200">
                            Press me
                        </Motion>
                    </div>
                    <pre class="overflow-x-auto border-t border-zinc-800/60 bg-zinc-950 p-4 font-mono text-[12px] leading-5 text-zinc-400"><code>{tap_code}</code></pre>
                </div>

                <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
                    <div class="border-b border-zinc-800/60 px-4 py-2.5">
                        <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">Both</span>
                    </div>
                    <div class="flex h-44 items-center justify-center p-6">
                        <Motion as="button" whileHover={{"scale": 1.06, "y": -3}} whileTap={{"scale": 0.94}}
                                transition={{"duration": 0.18}}
                                className="rounded-xl bg-gradient-to-r from-blue-600 to-violet-600 px-6 py-3 text-sm font-semibold text-white shadow-lg">
                            Hover &amp; tap
                        </Motion>
                    </div>
                    <pre class="overflow-x-auto border-t border-zinc-800/60 bg-zinc-950 p-4 font-mono text-[12px] leading-5 text-zinc-400"><code>{combo_code}</code></pre>
                </div>

                <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
                    <div class="border-b border-zinc-800/60 px-4 py-2.5">
                        <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">Card lift</span>
                    </div>
                    <div class="flex h-44 items-center justify-center p-6">
                        <Motion whileHover={{"y": -8, "boxShadow": "0 16px 40px rgba(0,0,0,0.5)"}} transition={{"duration": 0.25}}
                                className="w-44 cursor-pointer rounded-xl border border-zinc-700 bg-zinc-800 p-4">
                            <p class="text-sm font-medium text-zinc-200">Hover the card</p>
                            <p class="mt-1 text-xs text-zinc-500">lifts with a soft shadow</p>
                        </Motion>
                    </div>
                    <pre class="overflow-x-auto border-t border-zinc-800/60 bg-zinc-950 p-4 font-mono text-[12px] leading-5 text-zinc-400"><code>{card_code}</code></pre>
                </div>

                <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
                    <div class="border-b border-zinc-800/60 px-4 py-2.5">
                        <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">Icon</span>
                    </div>
                    <div class="flex h-44 items-center justify-center p-6">
                        <Motion as="button" whileHover={{"rotate": 20, "scale": 1.15}} whileTap={{"scale": 0.8}}
                                transition={{"duration": 0.2}}
                                className="text-3xl">
                            ⚡
                        </Motion>
                    </div>
                    <pre class="overflow-x-auto border-t border-zinc-800/60 bg-zinc-950 p-4 font-mono text-[12px] leading-5 text-zinc-400"><code>{icon_code}</code></pre>
                </div>

                <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40 sm:col-span-2 lg:col-span-1">
                    <div class="border-b border-zinc-800/60 px-4 py-2.5">
                        <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">Spring back</span>
                    </div>
                    <div class="flex h-44 items-center justify-center p-6">
                        <Motion as="button"
                                whileHover={{"y": -6, "scale": 1.05}}
                                whileTap={{"scale": 0.9, "y": 0}}
                                transition={{"duration": 0.3, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
                                className="rounded-xl bg-emerald-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-600/30">
                            Press &amp; hold
                        </Motion>
                    </div>
                    <pre class="overflow-x-auto border-t border-zinc-800/60 bg-zinc-950 p-4 font-mono text-[12px] leading-5 text-zinc-400"><code>{combo_code}</code></pre>
                </div>
            </div>

            <p class="mt-8 text-sm leading-relaxed text-zinc-500">
                Gestures bind automatically — no event handlers needed. <code class="font-mono text-[13px] text-zinc-400">whileHover</code> and
                <code class="font-mono text-[13px] text-zinc-400"> whileTap</code> accept the same style maps as <code class="font-mono text-[13px] text-zinc-400">animate</code>,
                including keyframe arrays and any transition easing.
            </p>
        </div>
    )
