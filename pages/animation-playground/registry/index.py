"""Registry — animation playground index."""

from nextpy.psx import component, Link


@component
def Page():
    return (
        <div class="mx-auto max-w-5xl px-6 py-16">
            <nav class="mb-6 flex items-center gap-2 text-sm text-zinc-500">
                <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
                <span class="text-zinc-700">/</span>
                <span class="font-medium text-zinc-200">Registry</span>
            </nav>
            <header class="mb-10">
                <h1 class="text-2xl font-semibold tracking-tight text-white">Registry</h1>
                <p class="mt-2 max-w-2xl text-[15px] leading-relaxed text-zinc-500">
                    12 animated examples — live previews with copy-paste PSX code.
                </p>
            </header>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        <Link href="/animation-playground/registry/registry-introduction" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Introduction</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">How the component registry works.</p>
                        </Link>
                        <Link href="/animation-playground/registry/registry-getting-started" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Getting Started</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Registry setup walkthrough.</p>
                        </Link>
                        <Link href="/animation-playground/registry/github-registries" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">GitHub Registries</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Registry hosting on GitHub.</p>
                        </Link>
                        <Link href="/animation-playground/registry/registry-directory" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Registry Directory</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Browsing the component index.</p>
                        </Link>
                        <Link href="/animation-playground/registry/registry-health" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Registry Health</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Registry status indicators.</p>
                        </Link>
                        <Link href="/animation-playground/registry/registry-examples" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Examples</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Registry usage patterns.</p>
                        </Link>
                        <Link href="/animation-playground/registry/namespaces" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Namespaces</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Namespaced registry items.</p>
                        </Link>
                        <Link href="/animation-playground/registry/registry-authentication" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Authentication</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Private registry auth flows.</p>
                        </Link>
                        <Link href="/animation-playground/registry/dynamic-search" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Dynamic Search</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Live-filtered registry search.</p>
                        </Link>
                        <Link href="/animation-playground/registry/mcp-server" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">MCP Server</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Registry MCP endpoint.</p>
                        </Link>
                        <Link href="/animation-playground/registry/open-in-v0" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Open in v0</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">One-click v0 handoff.</p>
                        </Link>
                        <Link href="/animation-playground/registry/registry-faq" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">FAQ</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Registry questions answered.</p>
                        </Link>
            </div>
        </div>
    )
