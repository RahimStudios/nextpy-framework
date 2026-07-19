from nextpy.psx import psx, component, register_component, useState, useEffect, interactive_component


@interactive_component
def DataFetchingDemo(props):
    [data, setData] = useState("Loading...")
    [loading, setLoading] = useState(True)

    def load_data():
        nonlocal data, loading
        data = "Data loaded successfully!"
        loading = False

    handle_load = lambda e: load_data()

    return psx(f"""
        <div class="p-5 border border-cyan-200 rounded-2xl bg-cyan-50">
            <div class="flex items-center justify-between gap-4">
                <div>
                    <h3 class="font-semibold text-cyan-900">Data Fetching Demo</h3>
                    <p class="mt-1 text-sm text-cyan-700">Simulate async data loading.</p>
                </div>
                <button onclick={handle_load} class="px-4 py-2 text-sm font-semibold text-white rounded-lg bg-cyan-600">
                    Load Data
                </button>
            </div>
            <p class="mt-4 text-sm text-cyan-800">
                {data if not loading else "Loading..."}
            </p>
        </div>
    """)

register_component("DataFetchingDemo", DataFetchingDemo)


@component
def DataFetchingGuide(props):
    return psx("""
        <section id="data-fetching" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">Data Fetching</h2>
                <p class="mt-2 text-gray-400">
                    Fetch and manage data in your NextPy applications with server-side rendering and client-side state.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-teal-400">Data Fetching Strategies</h3>
                <p class="mt-2 text-sm text-teal-300">
                    NextPy supports multiple data fetching patterns: server-side rendering with getServerSideProps, static generation with getStaticProps, and client-side fetching with hooks.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Server-Side Rendering</h3>
                    <p class="mt-2 text-sm text-gray-400">Fetch data on each request.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># pages/blog/[slug].py

async def getServerSideProps(context):
    slug = context.get("params", {}).get("slug")
    post = await fetch_post(slug)
    
    return {
        "props": {
            "post": post
        }
    }</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Static Generation</h3>
                    <p class="mt-2 text-sm text-gray-400">Generate pages at build time.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># pages/index.py

async def getStaticProps():
    posts = await fetch_all_posts()
    
    return {
        "props": {
            "posts": posts
        },
        "revalidate": 60  # ISR
    }</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Client-Side Fetching</h3>
                    <p class="mt-2 text-sm text-gray-400">Fetch data in the browser.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import useState, useEffect

[data, setData] = useState(None)
[loading, setLoading] = useState(True)

useEffect(lambda: fetch_data(), [])

async def fetch_data():
    response = await fetch("/api/data")
    result = await response.json()
    setData(result)
    setLoading(False)</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">API Routes</h3>
                    <p class="mt-2 text-sm text-gray-400">Create backend endpoints.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># pages/api/users.py

async def get(request, params):
    users = await db.fetch_users()
    return {"users": users}

async def post(request, params):
    data = await request.json()
    user = await db.create_user(data)
    return {"user": user}</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Choosing the Right Strategy</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li><strong>getServerSideProps:</strong> Use for personalized content, real-time data</li>
                    <li><strong>getStaticProps:</strong> Use for static content, marketing pages</li>
                    <li><strong>Client-side:</strong> Use for user interactions, real-time updates</li>
                    <li><strong>ISR:</strong> Use for content that updates periodically</li>
                </ul>
            </div>

            <DataFetchingDemo />
        </section>
    """)
