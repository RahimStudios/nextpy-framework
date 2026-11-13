from nextpy.psx import psx, component, register_component


@component
def ErrorHandlingGuide(props):
    return psx("""
        <section id="error-handling" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">Error Handling</h2>
                <p class="mt-2 text-gray-400">
                    Handle errors gracefully in your NextPy applications with custom error pages and error boundaries.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-red-400">Error Handling Overview</h3>
                <p class="mt-2 text-sm text-red-300">
                    NextPy provides multiple layers of error handling: custom error pages, error boundaries for components, try-catch blocks for async operations, and global error middleware.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Custom Error Pages</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># pages/404.py

@component
def NotFound():
    return (
        <div class="flex items-center justify-center min-h-screen">
            <div class="text-center">
                <h1 class="text-6xl font-bold">404</h1>
                <p class="mt-4 text-gray-600">Page not found</p>
                <a href="/" class="mt-4 text-blue-600">Go home</a>
            </div>
        </div>
    )

# pages/500.py
@component
def ServerError():
    return (
        <div class="flex items-center justify-center min-h-screen">
            <h1 class="text-6xl font-bold">500</h1>
            <p>Server error</p>
        </div>
    )</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Error Boundaries</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import component, ErrorBoundary

@component
def SafeComponent(props):
    return (
        <ErrorBoundary fallback={<ErrorFallback />}>
            {props.get("children")}
        </ErrorBoundary>
    )

@component
def ErrorFallback():
    return (
        <div class="p-4 bg-red-100 rounded-lg">
            <p>Something went wrong</p>
            <button onclick={location.reload}>Retry</button>
        </div>
    )</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">API Error Handling</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># pages/api/data.py

async def get(request, params):
    try:
        data = await fetch_data()
        return {"data": data}
    except ValueError as e:
        return {
            "error": str(e),
            "status": 400
        }
    except Exception as e:
        return {
            "error": "Internal server error",
            "status": 500
        }</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Async Error Handling</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import useState, useEffect

[data, setData] = useState(None)
[error, setError] = useState(None)

async def fetch_data():
    try:
        response = await fetch("/api/data")
        result = await response.json()
        setData(result)
    except Exception as e:
        setError(str(e))

useEffect(lambda: fetch_data(), [])</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Error Handling Best Practices</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li>Always handle errors in async operations</li>
                    <li>Provide user-friendly error messages</li>
                    <li>Log errors for debugging in production</li>
                    <li>Use error boundaries to isolate component failures</li>
                    <li>Implement retry logic for transient failures</li>
                    <li>Create custom error pages for different HTTP status codes</li>
                    <li>Use validation to prevent errors before they occur</li>
                </ul>
            </div>
        </section>
    """)
