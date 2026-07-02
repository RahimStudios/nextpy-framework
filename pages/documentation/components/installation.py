from nextpy.psx import psx, component, register_component
from pages.components.codeblock import CodeBlock

register_component("CodeBlock", CodeBlock)


def Installation():
    return psx("""
        <section id="installation" class="space-y-10">

            <!-- Header -->
            <div class="pb-4 border-b border-gray-800">
                <h2 class="text-3xl font-bold text-white">
                    Installation
                </h2>

                <p class="mt-3 text-gray-400 leading-relaxed">
                    Install <span class="text-sky-400 font-medium">NextPy</span> in a fresh environment and start building
                    production-ready applications in minutes.
                </p>
            </div>

            <!-- System Requirements -->
            <div class="p-6 rounded-2xl border border-gray-800 bg-gray-900/60 backdrop-blur">

                <h3 class="text-white font-semibold flex items-center gap-2">

                    <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" stroke-width="2"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M9.75 3v2.25m4.5-2.25v2.25M4.5 9h15M6.75 21h10.5A2.25 2.25 0 0019.5 18.75V7.5A2.25 2.25 0 0017.25 5.25H6.75A2.25 2.25 0 004.5 7.5v11.25A2.25 2.25 0 006.75 21z" />
                    </svg>

                    System Requirements
                </h3>

                <ul class="mt-4 space-y-2 text-sm text-gray-300 list-disc pl-5">
                    <li><span class="text-sky-400">Python 3.9+</span></li>
                    <li>pip (Python package manager)</li>
                    <li>Node.js 16+ (for build tools)</li>
                    <li>Git (optional version control)</li>
                </ul>
            </div>

            <!-- Step Grid -->
            <div class="grid gap-6 md:grid-cols-2">

                <!-- Step 1 -->
                <div class="p-6 rounded-2xl border border-gray-800 bg-gray-900/40">

                    <h3 class="text-white font-semibold flex items-center gap-2">

                        <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" stroke-width="2"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M4 6h16M4 12h16M4 18h16" />
                        </svg>

                        Create virtual environment
                    </h3>

                    <CodeBlock
                        lang="bash"
                        code="
python -m venv venv
source venv/bin/activate
# Windows: venv\\Scripts\\activate
                        "
                    />

                    <p class="mt-3 text-sm text-gray-400">
                        Keeps dependencies isolated and avoids system conflicts.
                    </p>
                </div>

                <!-- Step 2 -->
                <div class="p-6 rounded-2xl border border-gray-800 bg-gray-900/40">

                    <h3 class="text-white font-semibold flex items-center gap-2">

                        <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" stroke-width="2"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M12 6v6l4 2" />
                        </svg>

                        Install NextPy
                    </h3>

                    <CodeBlock
                        lang="bash"
                        code="
pip install nextpy-framework
                        "
                    />

                    <p class="mt-3 text-sm text-gray-400">
                        Installs CLI, runtime, and framework dependencies.
                    </p>
                </div>

            </div>

            <!-- Step 3 -->
            <div class="p-6 rounded-2xl border border-gray-800 bg-gray-900/40">

                <h3 class="text-white font-semibold flex items-center gap-2">

                    <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" stroke-width="2"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M9 12h6m-6 4h6m-7 4h8a2 2 0 002-2V6a2 2 0 00-2-2H8a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>

                    Create your first app
                </h3>

                <CodeBlock
                    lang="bash"
                    code="
nextpy create my-app
cd my-app
nextpy dev
                    "
                />

                <p class="mt-3 text-sm text-gray-400">
                    Starts development server at <span class="text-sky-400">localhost:8000</span> with hot reload.
                </p>
            </div>

            <!-- Alternative -->
            <div class="p-6 rounded-2xl border border-gray-800 bg-gray-900/40">

                <h3 class="text-white font-semibold flex items-center gap-2">

                    <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" stroke-width="2"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                    </svg>

                    Alternative: Install from source
                </h3>

                <CodeBlock
                    lang="bash"
                    code="
git clone https://github.com/RahimStudios/nextpy-framework.git
cd nextpy-framework
pip install -e .
                    "
                />

                <p class="mt-3 text-sm text-gray-400">
                    Useful for contributors and early feature testing.
                </p>
            </div>

            <!-- Verify -->
            <div class="p-6 rounded-2xl border border-gray-800 bg-gray-900/40">

                <h3 class="text-white font-semibold flex items-center gap-2">

                    <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" stroke-width="2"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M5 13l4 4L19 7" />
                    </svg>

                    Verify installation
                </h3>

                <CodeBlock
                    lang="bash"
                    code="
nextpy --version
nextpy --help
                    "
                />

                <p class="mt-3 text-gray-400 text-sm">
                    Confirms your installation is working correctly.
                </p>
            </div>

        </section>
    """)