"""Integrations — animation playground index."""

from nextpy.psx import component, Link


@component
def Page():
    return (
        <div class="mx-auto max-w-5xl px-6 py-16">
            <nav class="mb-6 flex items-center gap-2 text-sm text-zinc-500">
                <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
                <span class="text-zinc-700">/</span>
                <span class="font-medium text-zinc-200">Integrations</span>
            </nav>
            <header class="mb-10">
                <h1 class="text-2xl font-semibold tracking-tight text-white">Integrations</h1>
                <p class="mt-2 max-w-2xl text-[15px] leading-relaxed text-zinc-500">
                    7 animated examples — live previews with copy-paste PSX code.
                </p>
            </header>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        <Link href="/animation-playground/integrations/shadcn-react" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">@shadcn/react</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">React interop layer notes.</p>
                        </Link>
                        <Link href="/animation-playground/integrations/shadcn-helpers" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">@shadcn/helpers</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Helper utilities overview.</p>
                        </Link>
                        <Link href="/animation-playground/integrations/ai-sdk" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">AI SDK</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Model streaming into chat elements.</p>
                        </Link>
                        <Link href="/animation-playground/integrations/tanstack-ai" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">TanStack AI</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">TanStack adapter overview.</p>
                        </Link>
                        <Link href="/animation-playground/integrations/react-hook-form" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">React Hook Form</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Form state with animated validation.</p>
                        </Link>
                        <Link href="/animation-playground/integrations/tanstack-form" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">TanStack Form</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Schema-driven form animations.</p>
                        </Link>
                        <Link href="/animation-playground/integrations/formisch" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Formisch</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Lightweight form validation motion.</p>
                        </Link>
            </div>
        </div>
    )
