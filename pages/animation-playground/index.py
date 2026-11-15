"""Animation Playground — Overview"""

from nextpy.psx import component, Link


@component
def Page():
    sections = [
        ("/animation-playground/basics", "Basics", "Fade, slide, scale, and rotate entrances."),
        ("/animation-playground/gestures", "Gestures", "whileHover and whileTap pointer feedback."),
        ("/animation-playground/keyframes", "Keyframes & easings", "Multi-step keyframes, easing curves, stagger."),
        ("/animation-playground/flip", "Layout (FLIP)", "Elements animate to new positions on reorder."),
        ("/animation-playground/presence", "AnimatePresence", "Exit animations before removal."),
        ("/animation-playground/dynamic", "Dynamic values", "Animate props driven by state."),
    ]

    groups = [
        ("/animation-playground/components", "Components", "65 components"),
        ("/animation-playground/ai", "AI elements", "22 elements"),
        ("/animation-playground/utilities", "Utilities", "scroll-fade, shimmer"),
        ("/animation-playground/get-started", "Get started", "installation, theming, CLI"),
        ("/animation-playground/integrations", "Integrations", "AI SDK, TanStack, forms"),
        ("/animation-playground/registry", "Registry", "registries & schemas"),
        ("/animation-playground/api", "API reference", "registry.json schemas"),
    ]

    return (
        <div class="mx-auto max-w-3xl px-6 py-16">
            <header class="mb-14">
                <h1 class="text-2xl font-semibold tracking-tight text-white">Animation Playground</h1>
                <p class="mt-2 text-[15px] leading-relaxed text-zinc-500">
                    Every animation NextPy supports, with live previews and copy-paste code.
                    <code class="font-mono text-[13px] text-zinc-400">Motion</code> compiles to a JSON config on the element
                    and plays through the Web Animations API — no JS bundle.
                </p>
            </header>

            <section class="mb-14">
                <h2 class="mb-1 text-xs font-medium uppercase tracking-wider text-zinc-600">Core</h2>
                <div class="divide-y divide-zinc-800/60 border-y border-zinc-800/60">
                    {for item in sections:
                        <a href="{item[0]}" class="group flex items-baseline justify-between gap-4 py-3.5 transition-colors">
                            <div class="min-w-0">
                                <span class="text-[15px] font-medium text-zinc-200 transition-colors group-hover:text-white">{item[1]}</span>
                                <span class="ml-3 text-sm text-zinc-500">{item[2]}</span>
                            </div>
                            <span class="shrink-0 text-zinc-600 transition-colors group-hover:text-zinc-400">→</span>
                        </a>
                    }
                </div>
            </section>

            <section>
                <h2 class="mb-1 text-xs font-medium uppercase tracking-wider text-zinc-600">Browse</h2>
                <div class="divide-y divide-zinc-800/60 border-y border-zinc-800/60">
                    {for item in groups:
                        <a href="{item[0]}" class="group flex items-baseline justify-between gap-4 py-3.5 transition-colors">
                            <div class="min-w-0">
                                <span class="text-[15px] font-medium text-zinc-200 transition-colors group-hover:text-white">{item[1]}</span>
                                <span class="ml-3 text-sm text-zinc-500">{item[2]}</span>
                            </div>
                            <span class="shrink-0 text-zinc-600 transition-colors group-hover:text-zinc-400">→</span>
                        </a>
                    }
                </div>
            </section>
        </div>
    )
