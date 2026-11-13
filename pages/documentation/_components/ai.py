from nextpy.psx import psx, interactive_component



@interactive_component
def AIAssistantGuide(props):
    return psx("""
        <section id="ai" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">AI Assistant</h2>
                <p class="mt-2 text-gray-400">
                    Speed up development with the built-in AI assistant for scaffolding, explanations, and app generation. NextPy's AI features make it one of the most developer-friendly Python frameworks.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-indigo-400">Getting Started with AI</h3>
                <p class="mt-2 text-sm text-indigo-300">
                    The NextPy AI assistant is integrated directly into the CLI and can help you generate code, explain patterns, and build complete applications.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Basic AI Commands</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># Start AI assistant
nextpy ai

# Generate a chatbot
nextpy ai chatbot

# Create an AI agent
nextpy ai agent

# Generate a complete app
nextpy ai create ecommerce app</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">AI Code Generation</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># Generate components
nextpy ai generate component UserProfile

# Generate pages
nextpy ai generate page dashboard

# Generate API routes
nextpy ai generate api users</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">AI Code Explanation</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># Explain any code
nextpy ai explain app.py

# Get debugging help
nextpy ai debug routes.py

# Understand patterns
nextpy ai explain useState hook</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">AI Refactoring</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># Refactor code
nextpy ai refactor component.py

# Optimize performance
nextpy ai optimize page.py

# Add error handling
nextpy ai add-error-handling api.py</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">AI Capabilities</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li><strong class="text-white">Code Generation:</strong> Generate components, pages, API routes, and complete applications</li>
                    <li><strong class="text-white">Code Explanation:</strong> Understand unfamiliar code patterns and best practices</li>
                    <li><strong class="text-white">Debugging Assistance:</strong> Get help with errors and performance issues</li>
                    <li><strong class="text-white">Refactoring:</strong> Improve code quality and maintainability</li>
                    <li><strong class="text-white">Documentation:</strong> Auto-generate docs and comments</li>
                    <li><strong class="text-white">Testing:</strong> Generate unit tests and integration tests</li>
                </ul>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Best Practices</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li>Use AI for scaffolding and prototyping, then customize the generated code</li>
                    <li>Always review AI-generated code before committing to production</li>
                    <li>Use AI explanations to learn NextPy patterns and best practices</li>
                    <li>Leverage AI for repetitive tasks like boilerplate code generation</li>
                    <li>Combine AI assistance with manual coding for optimal results</li>
                </ul>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">AI Configuration</h3>
                <p class="mt-2 text-sm text-gray-400">
                    Configure AI providers and settings in your NextPy project configuration.
                </p>
                <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># nextpy.config.json
{
  "ai": {
    "provider": "openai",
    "model": "gpt-4",
    "apiKey": "your-api-key",
    "temperature": 0.7,
    "maxTokens": 2000
  }
}</pre>
            </div>
        </section>
    """)
