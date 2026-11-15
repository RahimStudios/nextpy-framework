"""Dynamic values — animation targets and styles driven by state."""

from nextpy.psx import component, interactive_component, useState, Motion, Link


@interactive_component
def DynamicDemos():
    [pos, set_pos] = useState(0)
    [size, set_size] = useState("md")

    def MoveLeft(e):
        set_pos(0)

    def MoveCenter(e):
        set_pos(1)

    def MoveRight(e):
        set_pos(2)

    def BindLeft(e):
        set_size("sm")

    def BindCenter(e):
        set_size("md")

    def BindRight(e):
        set_size("lg")

    btn = "rounded-lg border px-3.5 py-1.5 text-xs font-medium transition-colors"
    btn_on = btn + " border-blue-500/60 bg-blue-500/15 text-blue-200"
    btn_off = btn + " border-zinc-700 bg-zinc-800 text-zinc-400 hover:text-zinc-200"

    return (
        <div class="grid gap-5 lg:grid-cols-2">
            <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
                <div class="border-b border-zinc-800/60 px-4 py-2.5">
                    <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">Animated target</span>
                </div>
                <div class="p-6">
                    <div class="mb-5 flex items-center justify-center gap-2">
                        <button type="button" onclick={MoveLeft} class={btn_on if pos == 0 else btn_off}>Left</button>
                        <button type="button" onclick={MoveCenter} class={btn_on if pos == 1 else btn_off}>Center</button>
                        <button type="button" onclick={MoveRight} class={btn_on if pos == 2 else btn_off}>Right</button>
                    </div>
                    <div class="relative flex h-36 items-center justify-center overflow-hidden rounded-lg border border-zinc-800/60 bg-zinc-950/50">
                        <div class="absolute inset-x-8 top-1/2 border-t border-dashed border-zinc-800"></div>
                        {if pos == 0:
                            <Motion initial={{"opacity": 0, "x": -90}} animate={{"x": -60, "opacity": 1}}
                                    transition={{"duration": 0.5, "easing": "ease-out"}}
                                    className="relative rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-600/30">
                                -60
                            </Motion>
                        }
                        {if pos == 1:
                            <Motion initial={{"opacity": 0, "x": 90}} animate={{"x": 0, "opacity": 1}}
                                    transition={{"duration": 0.5, "easing": "ease-out"}}
                                    className="relative rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-600/30">
                                0
                            </Motion>
                        }
                        {if pos == 2:
                            <Motion initial={{"opacity": 0, "x": -90}} animate={{"x": 60, "opacity": 1}}
                                    transition={{"duration": 0.5, "easing": "ease-out"}}
                                    className="relative rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-600/30">
                                +60
                            </Motion>
                        }
                    </div>
                    <p class="mt-4 text-center text-xs text-zinc-500">Each branch remounts with a new animate target — the runtime tweens to it.</p>
                </div>
            </div>

            <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/40">
                <div class="border-b border-zinc-800/60 px-4 py-2.5">
                    <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">State-driven style</span>
                </div>
                <div class="p-6">
                    <div class="mb-5 flex items-center justify-center gap-2">
                        <button type="button" onclick={BindLeft} class={btn_on if size == "sm" else btn_off}>Small</button>
                        <button type="button" onclick={BindCenter} class={btn_on if size == "md" else btn_off}>Medium</button>
                        <button type="button" onclick={BindRight} class={btn_on if size == "lg" else btn_off}>Large</button>
                    </div>
                    <div class="relative flex h-36 items-center justify-center overflow-hidden rounded-lg border border-zinc-800/60 bg-zinc-950/50">
                        {if size == "sm":
                            <div class="h-10 w-16 rounded-lg bg-violet-500/30 border border-violet-500/40"></div>
                        }
                        {if size == "md":
                            <div class="h-14 w-24 rounded-lg bg-violet-500/40 border border-violet-500/50"></div>
                        }
                        {if size == "lg":
                            <div class="h-20 w-32 rounded-xl bg-violet-500/50 border border-violet-400/60 shadow-lg shadow-violet-500/20"></div>
                        }
                    </div>
                    <p class="mt-4 text-center text-xs text-zinc-500">Conditional branches swap the element — state drives which style renders.</p>
                </div>
            </div>
        </div>
    )


@component
def Page():
    code = '''# 1. Animated: swap the animate target via state
{if pos == 0:
    <Motion animate={{"x": -60}}>left</Motion>
}
{if pos == 1:
    <Motion animate={{"x": 0}}>center</Motion>
}

# 2. Style swap: {if} branches render different classes
{if size == "sm": <div class="h-10 w-16 bg-violet-500/30" />}
{if size == "lg": <div class="h-20 w-32 bg-violet-500/50" />}'''

    return (
        <div class="mx-auto max-w-5xl px-6 py-16">
            <nav class="mb-8 flex items-center gap-2 text-sm text-zinc-500">
                <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
                <span class="text-zinc-700">/</span>
                <span class="text-zinc-300">Dynamic values</span>
            </nav>
            <header class="mb-10 max-w-2xl">
                <h1 class="text-2xl font-semibold tracking-tight text-white">State-driven values</h1>
                <p class="mt-2 text-[15px] leading-relaxed text-zinc-500">
                    Animation props and style attributes both accept Python expressions — drive them with
                    <code class="font-mono text-[13px] text-zinc-400"> useState</code> and the UI updates on every change.
                    Left animates, right binds instantly.
                </p>
            </header>

            <div class="mb-10">
                <DynamicDemos />
            </div>

            <div>
                <h2 class="mb-3 text-xs font-medium uppercase tracking-wider text-zinc-600">Usage</h2>
                <pre class="overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-950 p-5 font-mono text-[12px] leading-5 text-zinc-300"><code>{code}</code></pre>
            </div>
        </div>
    )
