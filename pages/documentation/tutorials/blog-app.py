from nextpy.psx import register_component, component, psx, interactive_component, useState, Link


@component
def BlogAppTutorial():
    return psx("""
        <div class="mx-auto max-w-6xl">
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full">
        <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 pb-24 pt-6">
                        <!-- Top Breadcrumb & Actions -->
            <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                <div class="flex items-center gap-2 text-sm font-medium text-zinc-300">
                    <span>Documentation</span>
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                    <span class="text-white">Build a Blog App</span>
                </div>
                <div class="relative flex items-center rounded-md border border-zinc-800 bg-zinc-950 overflow-hidden">
                    <button class="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-zinc-300 hover:bg-zinc-900 transition-colors border-r border-zinc-800"
                        onclick="navigator.clipboard.writeText(document.querySelector('article').innerText);var l=this.querySelector('.cp-label');l.textContent='Copied';setTimeout(()=>l.textContent='Copy page',1500)">
                        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                        <span class="cp-label">Copy page</span>
                    </button>
                    <button class="px-2 py-1.5 text-zinc-500 hover:bg-zinc-900 hover:text-zinc-300 transition-colors"
                        onclick="var m=this.parentElement.querySelector('.copy-menu');m.style.display=m.style.display==='none'?'block':'none'">
                        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
                    </button>
                    <div class="copy-menu absolute right-0 top-full mt-1 w-44 rounded-lg border border-zinc-800 bg-zinc-900 shadow-xl z-50 py-1" style="display:none">
                        <button class="w-full text-left px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-800" onclick="navigator.clipboard.writeText(document.querySelector('article').innerText);this.closest('.copy-menu').style.display='none'">Copy page</button>
                        <button class="w-full text-left px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-800" onclick="navigator.clipboard.writeText(window.location.href);this.closest('.copy-menu').style.display='none'">Copy link</button>
                    </div>
                </div>
            </div>

            <!-- Page Header -->
            <header class="mb-12">
                <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                    Build a Blog App
                </h1>
                <p class="leading-relaxed text-zinc-300">
                    Learn to build a full-featured blog with server-side rendering, dynamic routes, and data fetching in NextPy.
                </p>
            </header>
            
            <div class="my-6 p-4 border border-zinc-700 bg-zinc-800 rounded-lg">
                <div class="flex items-start gap-3">
                    <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-zinc-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                    </svg>
                    <div class="flex-1">
                        <h4 class="font-semibold text-zinc-200">Prerequisites</h4>
                        <ul class="mt-2 space-y-1 text-sm text-zinc-300">
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                Completed "Your First App" tutorial
                            </li>
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                Completed "Todo App" tutorial
                            </li>
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                Basic understanding of database concepts
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <section id="overview" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    What You'll Build
                </h2>
                <p class="text-zinc-300 mb-4">
                    In this tutorial, you'll build a blog application with:
                </p>
                <ul class="list-disc list-inside space-y-2 text-zinc-300 ml-4">
                    <li>Server-side rendering (SSR) for SEO</li>
                    <li>Dynamic routes for individual blog posts</li>
                    <li>Data fetching with getServerSideProps</li>
                    <li>API routes for CRUD operations</li>
                    <li>Blog post listing page</li>
                    <li>Create new blog posts</li>
                    <li>View individual posts</li>
                </ul>
            </section>
            
            <section id="setup" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 1: Project Setup
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create a new NextPy project:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            bash
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-bash">nextpy create blog-app
cd blog-app
nextpy dev</code>
                    </pre>
                </div>
            </section>
            
            <section id="post-model" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 2: Create Post Model
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create a database model for blog posts:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">models/post.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    author = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)</code>
                    </pre>
                </div>
            </section>
            
            <section id="api-routes" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 3: Create API Routes
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create API routes for CRUD operations:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">pages/api/posts.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from fastapi import APIRouter, HTTPException
from models.post import Post
from nextpy.db import get_db

router = APIRouter()

@router.get("/posts")
def get_posts():
    db = get_db()
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return {"posts": posts}

@router.get("/posts/{post_id}")
def get_post(post_id: int):
    db = get_db()
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/posts")
def create_post(title: str, content: str, author: str):
    db = get_db()
    post = Post(title=title, content=content, author=author)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post</code>
                    </pre>
                </div>
            </section>
            
            <section id="index-page" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 4: Create Index Page (Post List)
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create the main blog listing page with SSR:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">pages/index.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.psx import component
from models.post import Post
from nextpy.db import get_db


def getServerSideProps(request):
    db = get_db()
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return {"posts": posts}

@component
def BlogIndex(props):
    posts = props.get("posts", [])
    
    return (
        &lt;div class="max-w-4xl mx-auto p-8 bg-gray-900 min-h-screen"&gt;
            &lt;div class="mb-8"&gt;
                &lt;h1 class="text-4xl font-bold text-white mb-2"&gt;Blog&lt;/h1&gt;
                &lt;p class="text-gray-400"&gt;Latest posts from our blog&lt;/p&gt;
            &lt;/div&gt;
            
            &lt;div class="space-y-6"&gt;
                {for post in posts:
                    &lt;article class="p-6 border border-gray-700 rounded-lg hover:border-gray-600 transition"&gt;
                        &lt;h2 class="text-2xl font-bold text-white mb-2"&gt;
                            &lt;a href={"/post/" + str(post["id"])} class="hover:text-blue-400"&gt;
                                {post["title"]}
                            &lt;/a&gt;
                        &lt;/h2&gt;
                        &lt;p class="text-gray-400 mb-4"&gt;
                            {post["content"][:200]}...
                        &lt;/p&gt;
                        &lt;div class="flex items-center gap-4 text-sm text-gray-500"&gt;
                            &lt;span&gt;By {post["author"]}&lt;/span&gt;
                            &lt;span&gt;{post["created_at"].strftime("%B %d, %Y")}&lt;/span&gt;
                        &lt;/div&gt;
                    &lt;/article&gt;
                }
            &lt;/div&gt;
            
            {if len(posts) == 0:
                &lt;p class="text-gray-400"&gt;No posts yet. Create your first post!&lt;/p&gt;
            }
        &lt;/div&gt;
    )

default = BlogIndex</code>
                    </pre>
                </div>
                
                <div class="my-6 p-4 border-l-4 border-purple-500 bg-purple-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-purple-400">How SSR Works</h4>
                            <div class="mt-1 text-sm text-zinc-300">
                                The getServerSideProps function runs on the server before the page is rendered. This is perfect for fetching data that needs to be SEO-friendly or requires server-side processing.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="dynamic-route" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 5: Create Dynamic Route (Post Detail)
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create a dynamic route for individual blog posts:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">pages/post/[id].py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.psx import component
from models.post import Post
from nextpy.db import get_db

def getServerSideProps(request, id):
    db = get_db()
    post = db.query(Post).filter(Post.id == int(id)).first()
    if not post:
        return {"not_found": True}
    return {"post": post}

@component
def PostDetail(props):
    post = props.get("post")
    
    if props.get("not_found"):
        return (
            &lt;div class="max-w-4xl mx-auto p-8 bg-gray-900 min-h-screen"&gt;
                &lt;h1 class="text-4xl font-bold text-white"&gt;Post Not Found&lt;/h1&gt;
                &lt;a href="/" class="text-blue-400 hover:text-blue-300"&gt;Back to Blog&lt;/a&gt;
            &lt;/div&gt;
        )
    
    return (
        &lt;article class="max-w-4xl mx-auto p-8 bg-gray-900 min-h-screen"&gt;
            &lt;a href="/" class="text-blue-400 hover:text-blue-300 mb-6 block"&gt;
                ← Back to Blog
            &lt;/a&gt;
            
            &lt;h1 class="text-4xl font-bold text-white mb-4"&gt;
                {post["title"]}
            &lt;/h1&gt;
            
            &lt;div class="flex items-center gap-4 mb-8 text-sm text-gray-500"&gt;
                &lt;span&gt;By {post["author"]}&lt;/span&gt;
                &lt;span&gt;{post["created_at"].strftime("%B %d, %Y at %I:%M %p")}&lt;/span&gt;
            &lt;/div&gt;
            
            &lt;div class="prose prose-invert max-w-none"&gt;
                &lt;p class="text-gray-300 leading-relaxed whitespace-pre-wrap"&gt;
                    {post["content"]}
                &lt;/p&gt;
            &lt;/div&gt;
        &lt;/article&gt;
    )

default = PostDetail</code>
                    </pre>
                </div>
                
                <div class="my-6 p-4 border-l-4 border-yellow-500 bg-yellow-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-yellow-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-yellow-400">Dynamic Routes</h4>
                            <div class="mt-1 text-sm text-zinc-300">
                                The [id].py file creates a dynamic route. The id parameter is extracted from the URL and passed to getServerSideProps.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="create-page" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 6: Create Post Page
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create a page to add new blog posts:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">pages/create.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.psx import component, interactive_component, useState, callServerAction

@interactive_component
def CreatePost():
    [title, setTitle] = useState("")
    [content, setContent] = useState("")
    [author, setAuthor] = useState("")
    [loading, setLoading] = useState(False)
    [error, setError] = useState("")
    
    def handle_submit(e):
        e.preventDefault()
        setLoading(True)
        setError("")
        
        result = callServerAction("create_post", {
            "title": title,
            "content": content,
            "author": author
        })
        
        if result:
            window.location.href = "/"
        else:
            setError("Failed to create post")
            setLoading(False)
    
    return (
        &lt;div class="max-w-4xl mx-auto p-8 bg-gray-900 min-h-screen"&gt;
            &lt;a href="/" class="text-blue-400 hover:text-blue-300 mb-6 block"&gt;
                ← Back to Blog
            &lt;/a&gt;
            
            &lt;h1 class="text-4xl font-bold text-white mb-8"&gt;Create New Post&lt;/h1&gt;
            
            {if error:
                &lt;div class="mb-4 p-3 text-red-400 bg-red-900/20 rounded"&gt;
                    {error}
                &lt;/div&gt;
            }
            
            &lt;form onsubmit="handle_submit" class="space-y-6"&gt;
                &lt;div&gt;
                    &lt;label class="block text-sm font-medium text-gray-300 mb-2"&gt;Title&lt;/label&gt;
                    &lt;input 
                        type="text"
                        value={title}
                        oninput={lambda e: setTitle(e.target.value)}
                        required
                        class="w-full px-4 py-2 rounded-lg border border-zinc-600 bg-zinc-800 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    /&gt;
                &lt;/div&gt;
                
                &lt;div&gt;
                    &lt;label class="block text-sm font-medium text-gray-300 mb-2"&gt;Author&lt;/label&gt;
                    &lt;input 
                        type="text"
                        value={author}
                        oninput={lambda e: setAuthor(e.target.value)}
                        required
                        class="w-full px-4 py-2 rounded-lg border border-zinc-600 bg-zinc-800 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    /&gt;
                &lt;/div&gt;
                
                &lt;div&gt;
                    &lt;label class="block text-sm font-medium text-gray-300 mb-2"&gt;Content&lt;/label&gt;
                    &lt;textarea 
                        value={content}
                        oninput={lambda e: setContent(e.target.value)}
                        required
                        rows="10"
                        class="w-full px-4 py-2 rounded-lg border border-zinc-600 bg-zinc-800 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    /&gt;
                &lt;/div&gt;
                
                &lt;button 
                    type="submit"
                    disabled={loading}
                    class="px-6 py-3 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                &gt;
                    {loading ? "Creating..." : "Create Post"}
                &lt;/button&gt;
            &lt;/form&gt;
        &lt;/div&gt;
    )

default = CreatePost</code>
                    </pre>
                </div>
            </section>
            
            <section id="navigation" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 7: Add Navigation
                </h2>
                <p class="text-zinc-300 mb-4">
                    Add a navigation component to the index page:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">pages/index.py (updated)</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">@component
def BlogIndex(props):
    posts = props.get("posts", [])
    
    return (
        &lt;div class="max-w-4xl mx-auto p-8 bg-gray-900 min-h-screen"&gt;
            &lt;div class="flex items-center justify-between mb-8"&gt;
                &lt;div&gt;
                    &lt;h1 class="text-4xl font-bold text-white mb-2"&gt;Blog&lt;/h1&gt;
                    &lt;p class="text-gray-400"&gt;Latest posts from our blog&lt;/p&gt;
                &lt;/div&gt;
                &lt;a 
                    href="/create"
                    class="px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700"
                &gt;
                    + New Post
                &lt;/a&gt;
            &lt;/div&gt;
            
            &lt;div class="space-y-6"&gt;
                {for post in posts:
                    &lt;article class="p-6 border border-gray-700 rounded-lg hover:border-gray-600 transition"&gt;
                        &lt;h2 class="text-2xl font-bold text-white mb-2"&gt;
                            &lt;a href={"/post/" + str(post["id"])} class="hover:text-blue-400"&gt;
                                {post["title"]}
                            &lt;/a&gt;
                        &lt;/h2&gt;
                        &lt;p class="text-gray-400 mb-4"&gt;
                            {post["content"][:200]}...
                        &lt;/p&gt;
                        &lt;div class="flex items-center gap-4 text-sm text-gray-500"&gt;
                            &lt;span&gt;By {post["author"]}&lt;/span&gt;
                            &lt;span&gt;{post["created_at"].strftime("%B %d, %Y")}&lt;/span&gt;
                        &lt;/div&gt;
                    &lt;/article&gt;
                }
            &lt;/div&gt;
        &lt;/div&gt;
    )</code>
                    </pre>
                </div>
            </section>
            
            <section id="summary" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Summary
                </h2>
                <p class="text-zinc-300 mb-4">
                    You've built a complete blog application with:
                </p>
                <ul class="list-disc list-inside space-y-2 text-zinc-300 ml-4">
                    <li>✅ Server-side rendering (SSR) with getServerSideProps</li>
                    <li>✅ Dynamic routes for individual posts</li>
                    <li>✅ API routes for CRUD operations</li>
                    <li>✅ Database models with SQLAlchemy</li>
                    <li>✅ Form handling and state management</li>
                    <li>✅ SEO-friendly page structure</li>
                </ul>
                
                <div class="my-6 p-4 border-l-4 border-green-500 bg-green-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-green-400">Congratulations!</h4>
                            <div class="mt-1 text-sm text-zinc-300">
                                You've mastered SSR, dynamic routes, and data fetching in NextPy. Your blog is SEO-friendly and ready for production!
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="next-steps" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    What's Next?
                </h2>
                <p class="text-zinc-300 mb-4">
                    Continue your NextPy journey:
                </p>
                <ul class="space-y-2 text-zinc-300">
                    <li>Build a Full-Stack App with authentication</li>
                    <li>Learn about static site generation (SSG)</li>
                    <li>Add image upload support</li>
                    <li>Implement comment system</li>
                    <li>Add search functionality</li>
                </ul>
            </section>
            <!-- Footer Pagination -->
            <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                <div class="w-1/2">
                    <Link href="/documentation/tutorials/todo-app" class="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                        <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                        <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                            <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                            Build a Todo App
                        </span>
                    </Link>
                </div>
                <div class="w-1/2 text-right">
                    <Link href="/documentation/tutorials/ai-chat" class="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                        <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                        <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                            AI Chat App
                            <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        </span>
                    </Link>
                </div>
            </footer>
        </article>
        <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-4 pl-8 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
            <div class="text-sm">
                <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What You'll Build</a></li>
                        <li><a href="#setup" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 1: Project Setup</a></li>
                        <li><a href="#post-model" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 2: Post Model</a></li>
                        <li><a href="#api-routes" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 3: API Routes</a></li>
                        <li><a href="#index-page" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 4: Index Page</a></li>
                        <li><a href="#dynamic-route" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 5: Post Detail</a></li>
                        <li><a href="#create-page" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 6: Create Post</a></li>
                        <li><a href="#navigation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 7: Navigation</a></li>
                        <li><a href="#summary" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Summary</a></li>
                        <li><a href="#next-steps" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What's Next</a></li>
                </ul>
            </div>
        </aside>
        </div>
        </div>
        """)


default = BlogAppTutorial

