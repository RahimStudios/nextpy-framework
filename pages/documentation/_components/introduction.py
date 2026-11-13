from nextpy.psx import component, psx, Link

@component
def Introduction(props):
    return psx("""
<article class="mx-auto max-w-4xl px-2 py-2 font-sans antialiased text-zinc-400 selection:bg-blue-500/30 selection:text-white">

    <!-- Document Header -->
    <header class="mb-12">
        <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">
            Welcome to NextPy!
        </h1>
        <p class="text-lg leading-relaxed text-zinc-400">
            NextPy is a flexible, highly optimized Python framework for building full-stack web applications. By utilizing pre-compiled structures, it unifies user interfaces, routing patterns, and data persistence models under a single clean execution layer.
        </p>
    </header>

    <!-- Section: What is NextPy -->
    <section id="what-is" class="mb-12">
        <h2 class="text-2xl font-semibold text-white mb-4">
            What is NextPy?
        </h2>
        <div class="space-y-6 text-base leading-relaxed text-zinc-400">
            <p>
                <strong class="text-zinc-200 font-semibold">NextPy bridges the division between Python computation speed and JavaScript-style reactive interfaces.</strong> It abstracts complex configurations away entirely, allowing you to focus on logic orchestration rather than asset scaffolding.
            </p>
            <p>
                Whether you are structuring isolated microservice routers, building distributed application networks, or crafting real-time AI dashboards, NextPy handles asset optimization, server-side generation workflows, and code delivery pipelines out of the box.
            </p>
        </div>
    </section>

    <!-- Section: How to use -->
    <section id="how-to-use" class="mb-12">
        <h2 class="text-2xl font-semibold text-white mb-4">
            How to use the documentation
        </h2>
        <p class="text-base leading-relaxed text-zinc-400 mb-4">
            The documentation is structured systematically into distinct segments tailored to your immediate project milestones:
        </p>
        
        <!-- Converted Grid to List to match image -->
        <ul class="list-disc pl-6 space-y-3 text-base text-zinc-400 marker:text-zinc-600">
            <li>
                <a href="#" class="font-medium text-white underline underline-offset-4 decoration-zinc-700 hover:decoration-white transition-colors">Getting Started</a>: Step-by-step guides covering rapid component setup, package distribution installations, and sandbox environment assembly.
            </li>
            <li>
                <a href="#" class="font-medium text-white underline underline-offset-4 decoration-zinc-700 hover:decoration-white transition-colors">Guides</a>: Deep dives on token-based secure authorization systems, real-time context streaming, state persistence, and performance scaling.
            </li>
            <li>
                <a href="#" class="font-medium text-white underline underline-offset-4 decoration-zinc-700 hover:decoration-white transition-colors">API Reference</a>: Rigorous technical signatures, return parameters, configuration flags, and complete shell mapping variables for all core modules.
            </li>
        </ul>
    </section>

    <!-- Section: Prerequisites -->
    <section id="prerequisites" class="mb-12">
        <h2 class="text-2xl font-semibold text-white mb-4">
            Prerequisite knowledge
        </h2>
        <p class="text-base leading-relaxed text-zinc-400 mb-4">
            While NextPy provides a clean developer abstraction pattern, you will find it beneficial to maintain basic engineering familiarity with these core paradigms:
        </p>
        <ul class="list-disc pl-6 space-y-2 text-base text-zinc-400 marker:text-zinc-600">
            <li><strong class="text-zinc-200 font-medium">Python 3.9+ Programming:</strong> Standard structural objects, async context execution loops, and package manager environments.</li>
            <li><strong class="text-zinc-200 font-medium">Component State Trees:</strong> Understanding data distribution flow across nested visualization layouts.</li>
            <li><strong class="text-zinc-200 font-medium">Web Basics:</strong> High-level knowledge of request-response operations, network routes, and style grids.</li>
        </ul>
    </section>

    <!-- Section: Community -->
    <section id="community" class="mb-12">
        <h2 class="text-2xl font-semibold text-white mb-4">
            Join our Community
        </h2>
        <p class="text-base leading-relaxed text-zinc-400 mb-4">
            Stuck on an architectural layout configuration or searching for design performance patterns? Reach out to the global development circle on our active tracking boards:
        </p>
        <div class="flex flex-wrap gap-4 text-sm font-medium">
            <a href="#" class="text-zinc-300 underline underline-offset-4 decoration-zinc-700 hover:text-white hover:decoration-white transition-colors">GitHub Discussions</a>
            <a href="#" class="text-zinc-300 underline underline-offset-4 decoration-zinc-700 hover:text-white hover:decoration-white transition-colors">Discord Server</a>
            <a href="#" class="text-zinc-300 underline underline-offset-4 decoration-zinc-700 hover:text-white hover:decoration-white transition-colors">X / Twitter Community</a>
        </div>
    </section>

    <!-- Section: Accessibility -->
    <section id="accessibility" class="mb-12">
        <h2 class="text-2xl font-semibold text-white mb-4">
            Accessibility
        </h2>
        <p class="text-base leading-relaxed text-zinc-400">
            Our reference structures are formatted to conform tightly to clean semantic markup matrices. For optimal audio readout feedback cycles, we suggest relying on modern screen reader applications such as VoiceOver or NVDA.
        </p>
    </section>

    <!-- Enhanced Pagination Footer -->
    <footer class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-16 pt-8 border-t border-zinc-800/60">
        
        <!-- Previous Page -->
        <div class="flex flex-col items-start p-4 rounded-lg border border-zinc-800 bg-zinc-950/50 opacity-50 cursor-not-allowed">
            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-2">Previous</span>
            <span class="text-base font-semibold text-zinc-600 select-none">—</span>
        </div>

        <!-- Next Page -->
        <Link href="/documentation/getting-started/installation" className="group flex flex-col items-end p-4 rounded-lg border border-zinc-800 bg-zinc-950/50 hover:bg-zinc-900/50 hover:border-zinc-700 transition-all">
            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-2">Next</span>
            <span class="text-base font-semibold text-white group-hover:text-blue-400 flex items-center gap-2 transition-colors">
                Installation
                <svg class="h-4 w-4 text-zinc-500 group-hover:text-blue-400 group-hover:translate-x-0.5 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
            </span>
        </Link>
        
    </footer>
</article>
""")