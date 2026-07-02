from nextpy.psx import psx, component, register_component


@component
def TableOfContents(props):
    return psx("""
        <div class="sticky top-20 space-y-8">
            <div>
                <h3 class="mb-4 text-sm font-semibold text-gray-400">On this page</h3>
                <nav class="space-y-3 text-sm">
                    <a href="#installation" class="block text-gray-400 hover:text-gray-100">Installation</a>
                    <a href="#quickstart" class="block text-gray-400 hover:text-gray-100">Quick Start</a>
                    <a href="#project-structure" class="block text-gray-400 hover:text-gray-100">Project Structure</a>
                    <a href="#cli-commands" class="block text-gray-400 hover:text-gray-100">CLI Commands</a>
                    <a href="#psx-guide" class="block text-gray-400 hover:text-gray-100">PSX Syntax</a>
                    <a href="#file-routing" class="block text-gray-400 hover:text-gray-100">File-based Routing</a>
                    <a href="#state-and-hooks" class="block text-gray-400 hover:text-gray-100">State and Hooks</a>
                    <a href="#hooks-guide" class="block text-gray-400 hover:text-gray-100">Hooks Guide</a>
                    <a href="#data-fetching" class="block text-gray-400 hover:text-gray-100">Data Fetching</a>
                    <a href="#api-and-deployment" class="block text-gray-400 hover:text-gray-100">API Routes</a>
                    <a href="#database" class="block text-gray-400 hover:text-gray-100">Database Integration</a>
                    <a href="#authentication" class="block text-gray-400 hover:text-gray-100">Authentication</a>
                    <a href="#styling" class="block text-gray-400 hover:text-gray-100">Styling & Tailwind</a>
                    <a href="#components" class="block text-gray-400 hover:text-gray-100">Reusable Components</a>
                    <a href="#ssr-ssg" class="block text-gray-400 hover:text-gray-100">SSR & Static Generation</a>
                    <a href="#error-handling" class="block text-gray-400 hover:text-gray-100">Error Handling</a>
                    <a href="#ai" class="block text-gray-400 hover:text-gray-100">AI Assistant</a>
                </nav>
            </div>
        </div>
    """)
