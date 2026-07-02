from nextpy.psx import psx, interactive_component


@interactive_component
def CLICommands(props):
    return psx(f"""
        <section id="cli-commands" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">CLI Commands</h2>
                <p class="mt-2 text-gray-400">Use the built-in CLI to scaffold projects, launch the development server, and ship production builds.</p>
            </div>

            <div class="grid gap-4 md:grid-cols-2">
                <div class="p-4 border border-gray-700 rounded-2xl bg-gray-900">
                    <p class="font-semibold text-gray-100">$ nextpy create my-app</p>
                    <p class="mt-2 text-sm text-gray-400">Create a fresh project with the recommended folder structure.</p>
                </div>
                <div class="p-4 border border-gray-700 rounded-2xl bg-gray-900">
                    <p class="font-semibold text-gray-100">$ nextpy dev</p>
                    <p class="mt-2 text-sm text-gray-400">Start the local dev server and open the app in your browser.</p>
                </div>
                <div class="p-4 border border-gray-700 rounded-2xl bg-gray-900">
                    <p class="font-semibold text-gray-100">$ nextpy build</p>
                    <p class="mt-2 text-sm text-gray-400">Compile the app for production and prepare static assets.</p>
                </div>
                <div class="p-4 border border-gray-700 rounded-2xl bg-gray-900">
                    <p class="font-semibold text-gray-100">$ nextpy start</p>
                    <p class="mt-2 text-sm text-gray-400">Start the production server (requires build first).</p>
                </div>
                <div class="p-4 border border-gray-700 rounded-2xl bg-gray-900">
                    <p class="font-semibold text-gray-100">$ nextpy ai</p>
                    <p class="mt-2 text-sm text-gray-400">Launch the built-in AI assistant to scaffold, explain, and extend your app.</p>
                </div>
                <div class="p-4 border border-gray-700 rounded-2xl bg-gray-900">
                    <p class="font-semibold text-gray-100">$ nextpy export</p>
                    <p class="mt-2 text-sm text-gray-400">Export your app as static HTML for deployment to any static host.</p>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Development Options</h3>
                <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">nextpy dev --port 3000      # Custom port
nextpy dev --host 0.0.0.0   # Listen on all interfaces
nextpy dev --no-reload      # Disable auto-reload</pre>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">AI Assistant Commands</h3>
                <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">nextpy ai chatbot           # Start AI chat interface
nextpy ai agent              # Start AI agent mode
nextpy ai create ecommerce  # Generate complete app
nextpy ai explain            # Explain code
nextpy ai optimize           # Optimize code</pre>
            </div>
        </section>
    """)
    