from nextpy.psx import psx, component, register_component


@component
def SSRSSGGuide(props):
    return psx("""
        <section id="ssr-ssg" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">SSR & Static Generation</h2>
                <p class="mt-2 text-gray-400">
                    Leverage server-side rendering and static site generation for optimal performance and SEO.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-orange-400">Rendering Strategies</h3>
                <p class="mt-2 text-sm text-orange-300">
                    NextPy supports multiple rendering strategies: Server-Side Rendering (SSR), Static Site Generation (SSG), and Incremental Static Regeneration (ISR). Choose the right strategy for each page.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Server-Side Rendering</h3>
                    <p class="mt-2 text-sm text-gray-400">Render pages on each request.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># pages/dashboard.py

async def getServerSideProps(context):
    user = await get_current_user(context)
    data = await fetch_user_data(user.id)
    
    return {
        "props": {
            "user": user,
            "data": data
        }
    }

@component
def Dashboard(props):
    user = props.get("user")
    return <h1>Welcome, {user["name"]}</h1></pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Static Site Generation</h3>
                    <p class="mt-2 text-sm text-gray-400">Generate pages at build time.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># pages/blog/[slug].py

async def getStaticPaths():
    posts = await fetch_all_posts()
    return {
        "paths": [
            {"params": {"slug": post.slug}}
            for post in posts
        ],
        "fallback": "blocking"
    }

async def getStaticProps(context):
    slug = context.get("params", {}).get("slug")
    post = await fetch_post(slug)
    
    return {"props": {"post": post}}</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Incremental Static Regeneration</h3>
                    <p class="mt-2 text-sm text-gray-400">Update static content periodically.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">async def getStaticProps():
    data = await fetch_data()
    
    return {
        "props": {"data": data},
        "revalidate": 60  # Regenerate every 60 seconds
    }

// Combines static performance with fresh data</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Client-Side Rendering</h3>
                    <p class="mt-2 text-sm text-gray-400">Render content in the browser.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">@component
def ClientOnly(props):
    [mounted, setMounted] = useState(False)
    
    useEffect(lambda: setMounted(True), [])
    
    if not mounted:
        return <div>Loading...</div>
    
    return props.get("children")

// Use for non-critical content</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Choosing a Strategy</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li><strong>SSR:</strong> User-specific content, real-time data, authentication-required pages</li>
                    <li><strong>SSG:</strong> Marketing pages, documentation, blog posts, product listings</li>
                    <li><strong>ISR:</strong> Content that updates periodically (news, stats, analytics)</li>
                    <li><strong>CSR:</strong> Highly interactive content, user preferences, real-time features</li>
                </ul>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Performance Benefits</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li>Faster initial page load with pre-rendered HTML</li>
                    <li>Improved SEO with server-rendered content</li>
                    <li>Better Core Web Vitals scores</li>
                    <li>Reduced client-side JavaScript bundle</li>
                    <li>Optimal caching strategies for different content types</li>
                </ul>
            </div>
        </section>
    """)
