from nextpy.psx import psx, interactive_component



@interactive_component
def AIAssistantGuide(props):
    return psx("""
        <section id="ai" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">AI Assistant</h2>
                <p class="mt-2 text-gray-400">
                    Speed up development with the built-in AI assistant for scaffolding, explanations, and app generation.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-indigo-400">Useful commands</h3>
                <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">nextpy ai
nextpy ai chatbot
nextpy ai agent
nextpy ai create ecommerce app</pre>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                <h3 class="font-semibold text-gray-100">Best uses</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li>Generate starter pages and layouts</li>
                    <li>Explain unfamiliar code paths and patterns</li>
                    <li>Prototype features before turning them into production code</li>
                </ul>
            </div>
        </section>
    """)
