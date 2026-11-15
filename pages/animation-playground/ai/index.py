"""AI Elements — animation playground index."""

from nextpy.psx import component, Link


@component
def Page():
    return (
        <div class="mx-auto max-w-5xl px-6 py-16">
            <nav class="mb-6 flex items-center gap-2 text-sm text-zinc-500">
                <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
                <span class="text-zinc-700">/</span>
                <span class="font-medium text-zinc-200">AI Elements</span>
            </nav>
            <header class="mb-10">
                <h1 class="text-2xl font-semibold tracking-tight text-white">AI Elements</h1>
                <p class="mt-2 max-w-2xl text-[15px] leading-relaxed text-zinc-500">
                    22 animated examples — live previews with copy-paste PSX code.
                </p>
            </header>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        <Link href="/animation-playground/ai/ai-introduction" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Introduction</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">What AI elements are and how they animate.</p>
                        </Link>
                        <Link href="/animation-playground/ai/chain-of-thought" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Chain of Thought</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Reasoning traces that expand step by step.</p>
                        </Link>
                        <Link href="/animation-playground/ai/ai-chat" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Chat</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Message streams that append with pop and typing dots.</p>
                        </Link>
                        <Link href="/animation-playground/ai/checkpoint" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Checkpoint</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Saved-state markers that pulse when reached.</p>
                        </Link>
                        <Link href="/animation-playground/ai/confirmation" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Confirmation</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Approval cards that slide in awaiting a decision.</p>
                        </Link>
                        <Link href="/animation-playground/ai/context" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Context</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Memory chips that fade in as context grows.</p>
                        </Link>
                        <Link href="/animation-playground/ai/file-tree" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">File Tree</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Nested file trees with expand/collapse rotation.</p>
                        </Link>
                        <Link href="/animation-playground/ai/inline-citation" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Inline Citation</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Citation chips that pop on hover.</p>
                        </Link>
                        <Link href="/animation-playground/ai/ai-message" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Message</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Single bubbles for user/assistant roles.</p>
                        </Link>
                        <Link href="/animation-playground/ai/model-selector" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Model Selector</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Model pickers with dropdown scale-in.</p>
                        </Link>
                        <Link href="/animation-playground/ai/plan" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Plan</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Agent plans whose steps check off with motion.</p>
                        </Link>
                        <Link href="/animation-playground/ai/prompt-input" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Prompt Input</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Composer boxes that focus-glow and send.</p>
                        </Link>
                        <Link href="/animation-playground/ai/queue" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Queue</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Queued-message indicators with pulse.</p>
                        </Link>
                        <Link href="/animation-playground/ai/reasoning" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Reasoning</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Thinking blocks with shimmer and collapse.</p>
                        </Link>
                        <Link href="/animation-playground/ai/sources" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Sources</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Citation lists that stagger in.</p>
                        </Link>
                        <Link href="/animation-playground/ai/stack-trace" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Stack Trace</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Error traces that slide down into view.</p>
                        </Link>
                        <Link href="/animation-playground/ai/subagent" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Subagent</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Agent cards with status pulse and progress.</p>
                        </Link>
                        <Link href="/animation-playground/ai/suggestion" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Suggestion</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Suggestion chips that wiggle for attention.</p>
                        </Link>
                        <Link href="/animation-playground/ai/task" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Task</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Task items with status icon transitions.</p>
                        </Link>
                        <Link href="/animation-playground/ai/terminal" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Terminal</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Terminal output that types line by line.</p>
                        </Link>
                        <Link href="/animation-playground/ai/test-results" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Test Results</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Result summaries whose bars fill on load.</p>
                        </Link>
                        <Link href="/animation-playground/ai/tool" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Tool</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Tool-call cards that expand args on hover.</p>
                        </Link>
            </div>
        </div>
    )
