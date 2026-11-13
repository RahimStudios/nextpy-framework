from nextpy.psx import interactive_component, Link

@interactive_component
def BlogPost(props=None):
    props = props or {}
    post = props.get("post", {})

    if not post:
        return (
            <div class="flex items-center justify-center min-h-screen bg-black text-white">
                <div class="text-center">
                    <h1 class="mb-4 text-4xl font-bold tracking-tight text-white">Post Not Found</h1>
                    <p class="text-zinc-400 mb-8">The article you are looking for doesn't exist or has been moved.</p>
                    <Link href="/blog" class="px-6 py-2.5 text-sm font-semibold text-black bg-white rounded-full hover:bg-zinc-200 transition-colors">
                        Back to Blog
                    </Link>
                </div>
            </div>
        )

    return (
        <div class="min-h-screen bg-black text-zinc-300 font-sans selection:bg-blue-500/30 selection:text-blue-200">
            
            {/* ========================================== */}
            {/* Main Layout Grid */}
            {/* ========================================== */}
            <div class="flex flex-col xl:flex-row items-start justify-center gap-12 max-w-6xl mx-auto px-4 py-12">
                
                {/* 1. Main Article Column */}
                <article class="flex-1 min-w-0 max-w-3xl">
                    
                    {/* Breadcrumb / Back Link */}
                    <nav class="mb-8 flex items-center gap-2 text-sm font-medium text-zinc-500">
                        <Link href="/blog" class="hover:text-zinc-300 transition-colors">Blog</Link>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-zinc-300 truncate max-w-[200px] sm:max-w-none">{post["title"]}</span>
                    </nav>

                    {/* Article Header */}
                    <header class="mb-12 border-b border-zinc-800/50 pb-8">
                        <div class="flex items-center gap-3 mb-6">
                            <span class="px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-semibold tracking-wide uppercase">
                                Engineering
                            </span>
                            <span class="text-sm text-zinc-500">{post.get("readingTime", "5 min read")}</span>
                        </div>
                        
                        <h1 class="text-4xl sm:text-5xl font-bold leading-tight text-white tracking-tight mb-6">
                            {post["title"]}
                        </h1>
                        
                        <div class="flex items-center justify-between mt-8">
                            {/* Author Info */}
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 rounded-full bg-zinc-800 border border-zinc-700 flex items-center justify-center text-sm font-bold text-zinc-300">
                                    {post["author"][0]}
                                </div>
                                <div>
                                    <div class="text-sm font-semibold text-white">{post["author"]}</div>
                                    <div class="text-xs text-zinc-500">Published on {post["date"]}</div>
                                </div>
                            </div>

                            {/* Social Share (Top) */}
                            <div class="flex items-center gap-2">
                                <button class="p-2 rounded-md bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-800 transition-all" title="Share on X">
                                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                                </button>
                                <button class="p-2 rounded-md bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-800 transition-all" title="Share on LinkedIn">
                                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                                </button>
                            </div>
                        </div>
                    </header>

                    {/* Article Content (Prose) */}
                    {/* We use prose-invert for the dark theme */}
                    <div class="prose prose-invert prose-zinc prose-lg max-w-none 
                                prose-headings:text-white prose-headings:font-semibold prose-headings:tracking-tight
                                prose-p:leading-7 prose-p:text-zinc-400
                                prose-a:text-blue-400 prose-a:no-underline hover:prose-a:underline
                                prose-strong:text-zinc-200
                                prose-code:text-blue-300 prose-code:bg-zinc-900 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:border prose-code:border-zinc-800 prose-code:font-normal prose-code:before:content-none prose-code:after:content-none
                                prose-pre:bg-zinc-950 prose-pre:border prose-pre:border-zinc-800/80 prose-pre:rounded-xl
                                prose-blockquote:border-l-blue-500 prose-blockquote:text-zinc-400 prose-blockquote:bg-zinc-900/50 prose-blockquote:py-1 prose-blockquote:px-4 prose-blockquote:rounded-r-lg
                                prose-img:rounded-xl prose-img:border prose-img:border-zinc-800">
                        
                        {/* Render content. Assuming post["content"] is HTML or Markdown converted to HTML */}
                        {post["content"]}
                        
                    </div>

                    {/* Author Bio Card (Bottom) */}
                    <div class="mt-16 p-6 sm:p-8 rounded-2xl bg-zinc-950/50 border border-zinc-800/80 flex flex-col sm:flex-row items-center gap-6">
                        <div class="w-16 h-16 rounded-full bg-zinc-800 border-2 border-zinc-700 flex items-center justify-center text-2xl font-bold text-zinc-300 shrink-0">
                            {post["author"][0]}
                        </div>
                        <div class="text-center sm:text-left">
                            <h3 class="text-lg font-bold text-white">{post["author"]}</h3>
                            <p class="text-sm text-zinc-400 mt-1 leading-relaxed">
                                Core contributor at NextPy. Passionate about building developer tools, exploring the intersection of Python and web tech, and sharing knowledge with the community.
                            </p>
                            <div class="flex items-center justify-center sm:justify-start gap-4 mt-3">
                                <a href="#" class="text-xs font-semibold text-zinc-400 hover:text-white transition-colors">Twitter</a>
                                <a href="#" class="text-xs font-semibold text-zinc-400 hover:text-white transition-colors">GitHub</a>
                            </div>
                        </div>
                    </div>

                    {/* Post Footer Navigation */}
                    <div class="mt-12 pt-8 border-t border-zinc-800/50 flex flex-col sm:flex-row items-center justify-between gap-4">
                        <Link href="/blog" class="flex items-center gap-2 text-sm font-medium text-zinc-400 hover:text-white transition-colors">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                            Back to all posts
                        </Link>
                        
                        <div class="flex items-center gap-3">
                            <span class="text-sm text-zinc-500">Share this article:</span>
                            <button class="p-1.5 rounded-md bg-zinc-900 text-zinc-400 hover:text-white transition-colors"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></button>
                            <button class="p-1.5 rounded-md bg-zinc-900 text-zinc-400 hover:text-white transition-colors"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></button>
                        </div>
                    </div>
                </article>

                {/* 2. Right Sidebar (Sticky TOC) */}
                <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-6 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
                    <div class="text-sm">
                        <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                        <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                            <li>
                                <a href="#introduction" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Introduction</a>
                            </li>
                            <li>
                                <a href="#why-python" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Why Python?</a>
                            </li>
                            <li>
                                <a href="#the-architecture" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">The Architecture</a>
                            </li>
                            <li>
                                <a href="#getting-started" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Getting Started</a>
                            </li>
                        </ul>
                    </div>

                    {/* Back to top */}
                    <div class="pt-8 mt-8 border-t border-zinc-800/50 text-sm font-medium space-y-4">
                        <Link href="/blog" className="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors">
                            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 10l7-7m0 0l7 7m-7-7v18"/></svg>
                            Back to top
                        </Link>
                    </div>
                </aside>

            </div>
        </div>
    )

def getServerSideProps(context):
    slug = context.get("params", {}).get("slug", "")
    
    # Expanded mock data to demonstrate the prose styling (Headings, lists, blockquotes)
    posts = {
        "introducing-nextpy-1-0": {
            "slug": "introducing-nextpy-1-0",
            "title": "Introducing NextPy 1.0: The Future of Python Web Apps",
            "date": "October 1, 2026",
            "author": "Team NextPy",
            "readingTime": "6 min read",
            "content": """
                <h2 id="introduction">Introduction</h2>
                <p>We are absolutely thrilled to announce the official release of <strong>NextPy 1.0</strong>. After months of rigorous development, testing, and community feedback, we have built a framework that truly bridges the gap between Python's backend power and modern frontend reactivity.</p>
                
                <p>Historically, building a full-stack web application meant wrestling with multiple languages, complex build tools, and a fragmented developer experience. You'd write Python for the backend (FastAPI, Django) and JavaScript/TypeScript for the frontend (React, Vue). NextPy eliminates this context switching entirely.</p>

                <h2 id="why-python">Why Python?</h2>
                <p>Python is the world's most popular programming language for a reason. It's readable, expressive, and has an incredible ecosystem of libraries for data science, AI, and backend logic. However, the frontend has always been the domain of JavaScript.</p>
                
                <blockquote>
                    <p>"NextPy doesn't just compile Python to JavaScript; it compiles Python into highly optimized React components, giving you the best of both worlds."</p>
                </blockquote>

                <p>With NextPy, you can define your entire application—from database models to complex UI states—in pure Python. Our custom PSX engine handles the heavy lifting of translating your Python functions into reactive frontend components.</p>

                <h2 id="the-architecture">The Architecture</h2>
                <p>Under the hood, NextPy is a marvel of modern compilation techniques. Here is how it works:</p>
                <ul>
                    <li><strong>PSX Parser:</strong> A custom AST parser that reads your Python syntax and translates it into a standard React tree.</li>
                    <li><strong>State Synchronization:</strong> The <code>useState</code> hooks are serialized and synchronized across the network using WebSockets, ensuring your UI is always in sync with the backend.</li>
                    <li><strong>File-Based Routing:</strong> Just drop a file in the <code>pages/</code> directory, and NextPy handles the rest.</li>
                </ul>

                <h2 id="getting-started">Getting Started</h2>
                <p>Ready to dive in? You can install NextPy right now using pip:</p>
                <pre><code>pip install nextpy-framework</code></pre>
                <p>We can't wait to see what you build. Welcome to the future of Python web development.</p>
            """
        },
        "why-python-web": {
            "slug": "why-python-web",
            "title": "Why Python is the Future of Web Development",
            "date": "September 28, 2026",
            "author": "Jane Doe",
            "readingTime": "4 min read",
            "content": """
                <h2>Python's Evolution</h2>
                <p>Python has evolved far beyond just scripting and data science. With frameworks like NextPy, it's becoming a first-class citizen for building modern, reactive web applications.</p>
                <p>The simplicity and readability of Python, combined with its massive ecosystem, make it the perfect language for full-stack development.</p>
            """
        },
    }

    post = posts.get(slug, {})
    if not post:
        return {"not_found": True}
    return {"props": {"post": post, "title": post['title']}}

default = BlogPost