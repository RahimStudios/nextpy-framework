from nextpy.psx import psx


def DocsSidebar():
    return psx(f"""
        <aside class="sticky space-y-8 text-sm top-20">
            

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Getting Started</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#installation" class="transition-colors hover:text-gray-100">Installation</a></li>
                    <li><a href="#quickstart" class="transition-colors hover:text-gray-100">Quick Start</a></li>
                    <li><a href="#project-structure" class="transition-colors hover:text-gray-100">Project Structure</a></li>
                    <li><a href="#cli-commands" class="transition-colors hover:text-gray-100">CLI Commands</a></li>
                </ul>
            </div>

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Core Concepts</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#psx-guide" class="transition-colors hover:text-gray-100">PSX Syntax</a></li>
                    <li><a href="#file-routing" class="transition-colors hover:text-gray-100">File-based Routing</a></li>
                    <li><a href="#state-and-hooks" class="transition-colors hover:text-gray-100">State and Hooks</a></li>
                    <li><a href="#hooks-guide" class="transition-colors hover:text-gray-100">Hooks Guide</a></li>
                </ul>
            </div>

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Data & Backend</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#data-fetching" class="transition-colors hover:text-gray-100">Data Fetching</a></li>
                    <li><a href="#api-and-deployment" class="transition-colors hover:text-gray-100">API Routes</a></li>
                    <li><a href="#database" class="transition-colors hover:text-gray-100">Database Integration</a></li>
                    <li><a href="#authentication" class="transition-colors hover:text-gray-100">Authentication</a></li>
                </ul>
            </div>

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Styling & UI</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#styling" class="transition-colors hover:text-gray-100">Styling & Tailwind</a></li>
                    <li><a href="#components" class="transition-colors hover:text-gray-100">Reusable Components</a></li>
                </ul>
            </div>

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Performance</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#ssr-ssg" class="transition-colors hover:text-gray-100">SSR & Static Generation</a></li>
                </ul>
            </div>

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Advanced</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#error-handling" class="transition-colors hover:text-gray-100">Error Handling</a></li>
                    <li><a href="#ai" class="transition-colors hover:text-gray-100">AI Assistant</a></li>
                </ul>
            </div>
        </aside>
    """)