from nextpy.psx import component

@component
def BlogIndex(props=None):
    props = props or {}
    posts = props.get("posts", [])

    return (
        <div class="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50/30">
            {/* Hero Section */}
            <div class="relative overflow-hidden bg-white shadow-sm">
                <div class="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-purple-500/10"></div>
                <div class="relative max-w-6xl px-4 py-16 mx-auto text-center sm:py-24 sm:px-6 lg:px-8">
                    <h1 class="text-5xl font-extrabold tracking-tight text-gray-900 sm:text-6xl">
                        <span class="text-transparent bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text">
                            Our Blog
                        </span>
                    </h1>
                    <p class="max-w-2xl mx-auto mt-4 text-xl text-gray-600">
                        Stories, insights, and updates from the team
                    </p>
                </div>
            </div>

            {/* Posts Grid */}
            <div class="max-w-6xl px-4 py-12 mx-auto sm:px-6 lg:px-8">
                <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
                    {if len(posts) > 0:
                        {for post in posts:
                            <article class="relative flex flex-col overflow-hidden transition-all duration-300 bg-white shadow-md group rounded-2xl hover:shadow-2xl hover:-translate-y-1">
                                {/* Card Image Placeholder */}
                                <div class="relative h-48 overflow-hidden bg-gradient-to-br from-indigo-200 to-purple-200">
                                    <div class="absolute inset-0 flex items-center justify-center text-4xl text-indigo-400/50">
                                        📖
                                    </div>
                                    <div class="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-white/80 to-transparent"></div>
                                </div>

                                <div class="flex flex-col flex-1 p-6">
                                    <h2 class="text-xl font-bold text-gray-900 line-clamp-2">
                                        <a href="/blog/{post['slug']}" class="transition-colors rounded hover:text-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                                            {post["title"]}
                                        </a>
                                    </h2>
                                    <p class="mt-2 text-sm text-gray-600 line-clamp-3">{post["excerpt"]}</p>

                                    <div class="flex items-center justify-between mt-4 text-xs text-gray-500">
                                        <div class="flex items-center space-x-2">
                                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                                                Article
                                            </span>
                                            <span>·</span>
                                            <span>{post["date"]}</span>
                                        </div>
                                        <span class="font-medium text-gray-700">{post["author"]}</span>
                                    </div>

                                    <div class="mt-4">
                                        <a href="/blog/{post['slug']}" class="inline-flex items-center text-sm font-semibold text-indigo-600 transition-colors hover:text-indigo-800 group-hover:underline">
                                            Read more
                                            <svg class="w-4 h-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                                            </svg>
                                        </a>
                                    </div>
                                </div>
                            </article>
                        }
                    {else:
                        <div class="py-20 text-center col-span-full">
                            <div class="mb-4 text-6xl">📭</div>
                            <p class="text-xl text-gray-600">No posts yet. Check back soon!</p>
                            <p class="text-sm text-gray-400">We're cooking up something great.</p>
                        </div>
                    }
                </div>
            </div>
        </div>
    )

def getServerSideProps(context):
    posts = [
        {
            "slug": "hello-world",
            "title": "Hello World",
            "excerpt": "Welcome to our blog built with NextPy! This is a modern way to build web apps with Python.",
            "date": "2025-01-15",
            "author": "Team NextPy",
        },
        {
            "slug": "why-python-web",
            "title": "Why Python for Web Apps",
            "excerpt": "Discover how Python is changing front-end development and why you should care.",
            "date": "2025-02-20",
            "author": "Jane Doe",
        },
    ]
    return {"props": {"posts": posts}}

default = BlogIndex