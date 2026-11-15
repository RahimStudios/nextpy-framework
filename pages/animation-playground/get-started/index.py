"""Get Started — animation playground index."""

from nextpy.psx import component, Link


@component
def Page():
    return (
        <div class="mx-auto max-w-5xl px-6 py-16">
            <nav class="mb-6 flex items-center gap-2 text-sm text-zinc-500">
                <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
                <span class="text-zinc-700">/</span>
                <span class="font-medium text-zinc-200">Get Started</span>
            </nav>
            <header class="mb-10">
                <h1 class="text-2xl font-semibold tracking-tight text-white">Get Started</h1>
                <p class="mt-2 max-w-2xl text-[15px] leading-relaxed text-zinc-500">
                    13 animated examples — live previews with copy-paste PSX code.
                </p>
            </header>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        <Link href="/animation-playground/get-started/installation" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Installation</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Setup steps animated as a guided tour.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/components-json" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">components.json</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Config file tour with field highlights.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/package-imports" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Package Imports</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Import paths revealed with typing.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/theming" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Theming</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Theme tokens transitioning live.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/typeset" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Typeset</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Prose styling with staggered reveals.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/dark-mode" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Dark Mode</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Theme toggle with crossfade.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/cli" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">CLI</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Command animations and spinner states.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/monorepo" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Monorepo</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Workspace graph with animated edges.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/skills" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Skills</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Skill cards that deal in on hover.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/javascript" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">JavaScript</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">JS interop snippets with highlight sweep.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/figma" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Figma</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Design-to-code flow animations.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/llms-txt" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">llms.txt</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Doc indexing visualization.</p>
                        </Link>
                        <Link href="/animation-playground/get-started/legacy-docs" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Legacy Docs</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Migration path animations.</p>
                        </Link>
            </div>
        </div>
    )
