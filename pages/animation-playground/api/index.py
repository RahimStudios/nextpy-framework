"""API Reference — animation playground index."""

from nextpy.psx import component, Link


@component
def Page():
    return (
        <div class="mx-auto max-w-5xl px-6 py-16">
            <nav class="mb-6 flex items-center gap-2 text-sm text-zinc-500">
                <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
                <span class="text-zinc-700">/</span>
                <span class="font-medium text-zinc-200">API Reference</span>
            </nav>
            <header class="mb-10">
                <h1 class="text-2xl font-semibold tracking-tight text-white">API Reference</h1>
                <p class="mt-2 max-w-2xl text-[15px] leading-relaxed text-zinc-500">
                    2 animated examples — live previews with copy-paste PSX code.
                </p>
            </header>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        <Link href="/animation-playground/api/registry-json" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">registry.json</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">The registry index schema.</p>
                        </Link>
                        <Link href="/animation-playground/api/registry-item-json" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">registry-item.json</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">The item schema reference.</p>
                        </Link>
            </div>
        </div>
    )
