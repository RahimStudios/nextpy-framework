from turtle import title
from nextpy.psx import component, Link

@component
def BlogIndex(props=None):
    props = props or {}
    posts = props.get("posts", [])

    return (
        <div class="min-h-screen py-4 bg-black text-white selection:bg-blue-500/30 selection:text-blue-200 font-sans">
            

            {/* Category Filter */}
            <div class="max-w-6xl px-4 mx-auto sm:px-6 lg:px-8 mt-12 mb-12">
                <div class="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-none">
                    <button class="px-4 py-1.5 rounded-full bg-white text-black text-sm font-medium transition-colors">All Posts</button>
                    <button class="px-4 py-1.5 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-300 text-sm font-medium hover:bg-zinc-800 transition-colors">Engineering</button>
                    <button class="px-4 py-1.5 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-300 text-sm font-medium hover:bg-zinc-800 transition-colors">Product</button>
                    <button class="px-4 py-1.5 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-300 text-sm font-medium hover:bg-zinc-800 transition-colors">Design</button>
                    <button class="px-4 py-1.5 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-300 text-sm font-medium hover:bg-zinc-800 transition-colors">Open Source</button>
                </div>
            </div>

            {/* Posts Content */}
            <div class="max-w-6xl px-4 mx-auto sm:px-6 lg:px-8 pb-24">
                
                {if len(posts) > 0:
                    
                    {/* Featured Post (First Item) */}
                    <div class="mb-16">
                        <Link href="/blog/{posts[0]['slug']}" class="group block relative rounded-2xl overflow-hidden border border-zinc-800/80 bg-zinc-950/50 hover:border-zinc-700 transition-colors">
                            <div class="grid grid-cols-1 md:grid-cols-2">
                                {/* Featured Image Placeholder */}
                                <div class="relative aspect-video md:aspect-auto md:h-full bg-gradient-to-br from-zinc-900 to-zinc-950 overflow-hidden">
                                    <div class="absolute inset-0 bg-[linear-gradient(to_right,#27272a_1px,transparent_1px),linear-gradient(to_bottom,#27272a_1px,transparent_1px)] [background-size:32px_32px] opacity-20 group-hover:opacity-30 transition-opacity"></div>
                                    <div class="absolute inset-0 flex items-center justify-center">
                                        <span class="text-6xl opacity-30 group-hover:scale-110 transition-transform duration-500">✨</span>
                                    </div>
                                </div>
                                
                                {/* Featured Content */}
                                <div class="p-8 md:p-12 flex flex-col justify-center">
                                    <div class="flex items-center gap-3 mb-4">
                                        <span class="px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-semibold tracking-wide uppercase">Featured</span>
                                        <span class="text-sm text-zinc-500">{posts[0]["date"]}</span>
                                    </div>
                                    <h2 class="text-2xl sm:text-3xl font-bold text-white mb-4 group-hover:text-blue-400 transition-colors leading-tight">
                                        {posts[0]["title"]}
                                    </h2>
                                    <p class="text-zinc-400 leading-relaxed mb-6 line-clamp-3">
                                        {posts[0]["excerpt"]}
                                    </p>
                                    <div class="flex items-center gap-3 mt-auto">
                                        <div class="w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center text-sm font-bold text-zinc-400 border border-zinc-700">
                                            {posts[0]["author"][0]}
                                        </div>
                                        <span class="text-sm font-medium text-zinc-300">{posts[0]["author"]}</span>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    </div>

                    {/* Standard Grid (Remaining Items) */}
                    <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
                        {for post in posts:
                            <article class="relative flex flex-col overflow-hidden transition-all duration-300 bg-zinc-950/40 border border-zinc-800/60 group rounded-2xl hover:border-zinc-700 hover:bg-zinc-900/40 hover:-translate-y-1 hover:shadow-2xl">
                                {/* Card Image Placeholder */}
                                <div class="relative h-48 overflow-hidden bg-zinc-900 border-b border-zinc-800/50">
                                    <div class="absolute inset-0 bg-[radial-gradient(#3f3f46_1px,transparent_1px)] [background-size:16px_16px] opacity-30 group-hover:opacity-50 transition-opacity"></div>
                                    <div class="absolute inset-0 flex items-center justify-center text-4xl opacity-40 group-hover:scale-110 transition-transform duration-500">
                                        📝
                                    </div>
                                </div>

                                <div class="flex flex-col flex-1 p-6">
                                    <div class="flex items-center gap-2 mb-3 text-xs font-medium text-zinc-500">
                                        <span class="text-blue-400">Engineering</span>
                                        <span>•</span>
                                        <span>{post["date"]}</span>
                                    </div>
                                    
                                    <h3 class="text-xl font-bold text-white mb-2 line-clamp-2 group-hover:text-blue-400 transition-colors">
                                        {post["title"]}
                                    </h3>
                                    
                                    <p class="text-sm leading-relaxed text-zinc-400 mb-6 line-clamp-3">
                                        {post["excerpt"]}
                                    </p>

                                    <div class="mt-auto flex items-center justify-between">
                                        <div class="flex items-center gap-2">
                                            <div class="w-6 h-6 rounded-full bg-zinc-800 flex items-center justify-center text-[10px] font-bold text-zinc-400 border border-zinc-700">
                                                {post["author"][0]}
                                            </div>
                                            <span class="text-xs font-medium text-zinc-400">{post["author"]}</span>
                                        </div>
                                        <Link href="/blog/{post['slug']}" className="text-blue-400 text-sm font-semibold flex items-center gap-1 group-hover:gap-2 transition-all">
                                            Read <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                                        </Link>
                                    </div>
                                </div>
                            </article>
                        }
                    </div>
                {else:
                    <div class="py-32 text-center">
                        <div class="mb-6 text-6xl opacity-30">📭</div>
                        <h3 class="text-2xl font-bold text-white mb-2">No posts yet</h3>
                        <p class="text-zinc-400">We're cooking up something great. Check back soon!</p>
                    </div>
                }
                
                {/* Pagination Placeholder */}
                {if len(posts) > 0:
                    <div class="mt-16 pt-8 border-t border-zinc-800/50 flex items-center justify-between">
                        <button class="px-4 py-2 text-sm font-medium text-zinc-500 bg-zinc-900/50 border border-zinc-800 rounded-md cursor-not-allowed" disabled>
                            Previous
                        </button>
                        <span class="text-sm text-zinc-500">Page 1 of 1</span>
                        <button class="px-4 py-2 text-sm font-medium text-zinc-300 bg-zinc-900 border border-zinc-800 rounded-md hover:bg-zinc-800 transition-colors">
                            Next
                        </button>
                    </div>
                }
            </div>
        </div>
    )

def getServerSideProps(context):
    posts = [
        {
            "slug": "introducing-nextpy-1-0",
            "title": "Introducing NextPy 5.0: The Future of Python Web Apps",
            "excerpt": "We are thrilled to announce the official release of NextPy 1.0. After months of development, we've built a framework that truly bridges the gap between Python's backend power and modern frontend reactivity.",
            "date": "2026-10-01",
            "author": "Team NextPy",
            "category": "Product"
        },
        {
            "slug": "why-python-web",
            "title": "Why Python is the Future of Web Development",
            "excerpt": "For years, JavaScript has dominated the frontend. But with the rise of frameworks like NextPy, Python is proving it can do much more than just backend scripts.",
            "date": "2026-09-28",
            "author": "Jane Doe",
            "category": "Engineering"
        },
        {
            "slug": "building-a-saas-dashboard",
            "title": "Building a Full-Stack SaaS Dashboard in 15 Minutes",
            "excerpt": "Learn how to scaffold a complete authentication system, database models, and a responsive UI using purely Python and NextPy.",
            "date": "2026-09-22",
            "author": "Alex Smith",
            "category": "Tutorial"
        },
        {
            "slug": "understanding-psx-internals",
            "title": "Under the Hood: How the PSX Engine Compiles Python",
            "excerpt": "Dive deep into the architecture of our custom PSX compiler, exploring how it generates highly optimized React components from Python strings.",
            "date": "2026-09-15",
            "author": "David Chen",
            "category": "Engineering"
        },
        {
            "slug": "state-management-patterns",
            "title": "Mastering State Management in NextPy",
            "excerpt": "Stop wrestling with Redux and Context APIs. Explore how NextPy's built-in `useState` and component-level state trees simplify complex UI logic.",
            "date": "2026-09-10",
            "author": "Sarah Jenkins",
            "category": "Design"
        },
        {
            "slug": "nextpy-vs-fastapi",
            "title": "NextPy vs FastAPI: Which should you choose?",
            "excerpt": "While FastAPI is incredible for building pure APIs, NextPy takes it a step further by integrating the frontend directly into your Python stack.",
            "date": "2026-09-02",
            "author": "Team NextPy",
            "category": "Open Source"
        }
    ]
    return {"props": {"posts": posts, "title": "NextPy Blog"}}

default = BlogIndex