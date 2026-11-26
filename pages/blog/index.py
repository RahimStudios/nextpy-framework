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
                {for post in posts:
                    <div class="mb-16">
                        <Link href="/blog/{post['slug']}" class="group block relative rounded-2xl overflow-hidden border border-zinc-800/80 bg-zinc-950/50 hover:border-zinc-700 transition-colors">
                            <div class="grid grid-cols-1 md:grid-cols-2">
                                {/* Featured Image Placeholder */}
                                <div class="relative aspect-video md:aspect-auto md:h-full bg-gradient-to-br from-zinc-900 to-zinc-950 overflow-hidden">
                                    <div class="absolute inset-0 bg-[linear-gradient(to_right,#27272a_1px,transparent_1px),linear-gradient(to_bottom,#27272a_1px,transparent_1px)] [background-size:32px_32px] opacity-20 group-hover:opacity-30 transition-opacity"></div>
                                    <div class="absolute inset-0 flex items-center justify-center">
                                        <span class="text-6xl opacity-30 group-hover:scale-110 transition-transform duration-500">&#10024;</span>
                                    </div>
                                </div>

                                {/* Featured Content */}
                                <div class="p-8 md:p-12 flex flex-col justify-center">
                                    <div class="flex items-center gap-3 mb-4">
                                        <span class="px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-semibold tracking-wide uppercase">Featured</span>
                                        <span class="text-sm text-zinc-500">{post["date"]}</span>
                                    </div>
                                    <h2 class="text-2xl sm:text-3xl font-bold text-white mb-4 group-hover:text-blue-400 transition-colors leading-tight">
                                        {post["title"]}
                                    </h2>
                                    <p class="text-zinc-400 leading-relaxed mb-6 line-clamp-3">
                                        {post["excerpt"]}
                                    </p>
                                    <div class="flex items-center gap-3 mt-auto">
                                        <div class="w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center text-sm font-bold text-zinc-400 border border-zinc-700">
                                            {post["author"][0]}
                                        </div>
                                        <span class="text-sm font-medium text-zinc-300">{post["author"]}</span>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    </div>
                }

                {if len(posts) == 0:
                    <div class="py-32 text-center">
                        <div class="mb-6 text-6xl opacity-30">&#128230;</div>
                        <h3 class="text-2xl font-bold text-white mb-2">No posts yet</h3>
                        <p class="text-zinc-400">We&apos;re cooking up something great. Check back soon!</p>
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
            "excerpt": "Learn how to leverage NextPy's file-based routing and server actions to build a production-ready dashboard quickly.",
            "date": "2026-09-15",
            "author": "John Smith",
            "category": "Tutorial"
        },
        {
            "slug": "python-frontend-revolution",
            "title": "The Python Frontend Revolution is Here",
            "excerpt": "Discover how PSX syntax allows you to write React-like components using pure Python logic and syntax.",
            "date": "2026-09-01",
            "author": "Sarah Connor",
            "category": "Engineering"
        },
        {
            "slug": "scaling-nextpy-apps",
            "title": "Scaling NextPy Applications to Millions of Users",
            "excerpt": "A deep dive into optimizing NextPy apps for high traffic, covering caching, database indexing, and async patterns.",
            "date": "2026-08-20",
            "author": "David Miller",
            "category": "Performance"
        }
    ]
    return {"props": {"posts": posts}}

default = BlogIndex
