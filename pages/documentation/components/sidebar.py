from nextpy.psx import psx


def DocsSidebar():
    return psx(f"""
        <aside class="sticky top-20 space-y-8 text-sm">
            

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Getting Started</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#installation" class="hover:text-gray-100 transition-colors">Installation</a></li>
                    <li><a href="#quickstart" class="hover:text-gray-100 transition-colors">Quick Start</a></li>
                    <li><a href="#project-structure" class="hover:text-gray-100 transition-colors">Project Structure</a></li>
                    <li><a href="#cli-commands" class="hover:text-gray-100 transition-colors">CLI Commands</a></li>
                </ul>
            </div>

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Core Concepts</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#psx-guide" class="hover:text-gray-100 transition-colors">PSX Syntax</a></li>
                    <li><a href="#file-routing" class="hover:text-gray-100 transition-colors">File-based Routing</a></li>
                    <li><a href="#state-and-hooks" class="hover:text-gray-100 transition-colors">State and Hooks</a></li>
                    <li><a href="#hooks-guide" class="hover:text-gray-100 transition-colors">Hooks Guide</a></li>
                </ul>
            </div>

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Data & Backend</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#data-fetching" class="hover:text-gray-100 transition-colors">Data Fetching</a></li>
                    <li><a href="#api-and-deployment" class="hover:text-gray-100 transition-colors">API Routes</a></li>
                    <li><a href="#database" class="hover:text-gray-100 transition-colors">Database Integration</a></li>
                    <li><a href="#authentication" class="hover:text-gray-100 transition-colors">Authentication</a></li>
                </ul>
            </div>

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Styling & UI</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#styling" class="hover:text-gray-100 transition-colors">Styling & Tailwind</a></li>
                    <li><a href="#components" class="hover:text-gray-100 transition-colors">Reusable Components</a></li>
                </ul>
            </div>

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Performance</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#ssr-ssg" class="hover:text-gray-100 transition-colors">SSR & Static Generation</a></li>
                </ul>
            </div>

            <div>
                <h3 class="mb-3 font-semibold text-gray-100">Advanced</h3>
                <ul class="space-y-2 text-gray-400">
                    <li><a href="#error-handling" class="hover:text-gray-100 transition-colors">Error Handling</a></li>
                    <li><a href="#ai" class="hover:text-gray-100 transition-colors">AI Assistant</a></li>
                </ul>
            </div>
        </aside>
    """)