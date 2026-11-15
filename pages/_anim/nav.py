"""Shared sidebar layout for animation playground category sections."""

from nextpy.psx import component, Link, clsx
from .registry import GROUPS, ITEMS


@component
def GroupLayout(children, group="components", **props):
    """Left-sidebar docs layout for one animation category."""
    props = props or {}
    props.pop("children", None)
    base = f"/animation-playground/{group}"
    group_label = dict(GROUPS).get(group, group)
    items = [(f"{base}/{slug}", label)
             for slug, meta in ITEMS.items() if meta[1] == group
             for label in [meta[0]]]

    return (
        <div class="mx-auto flex max-w-7xl gap-8 px-4 py-10">
            <aside class="hidden w-56 shrink-0 lg:block">
                <div class="sticky top-20 max-h-[calc(100vh-6rem)] overflow-y-auto pb-8 pr-2 scrollbar-none">
                    <Link href="/animation-playground" class="mb-4 block text-sm font-bold text-white hover:text-blue-400">
                        ← Playground
                    </Link>
                    <p class="mb-2 px-2 text-[10px] font-bold uppercase tracking-widest text-zinc-600">{group_label}</p>
                    <nav class="flex flex-col gap-0.5">
                        {for pair in items:
                            <a href="{pair[0]}"
                               class="rounded-md px-2 py-1 text-[13px] text-zinc-400 transition-colors hover:bg-zinc-800/60 hover:text-white">
                                {pair[1]}
                            </a>
                        }
                    </nav>
                </div>
            </aside>
            <main class="min-w-0 flex-1">
                {children}
            </main>
        </div>
    )
