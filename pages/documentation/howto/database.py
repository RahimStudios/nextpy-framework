from nextpy.psx import register_component, component, psx, interactive_component, useState, useEffect


@component
def DatabaseGuide():
    return psx("""
        <div class="mx-auto max-w-6xl">
        <div class="grid gap-12 lg:grid-cols-[1fr_260px]">
        <article class="min-w-0">
        <DocsScrollSpy />
            <div class="mb-8 pb-6 border-b border-gray-800">
                <div class="flex items-center gap-3 mb-4">
                    <span class="px-2 py-1 text-xs font-medium border rounded bg-green-500/20 text-green-400 border-green-500">
                        How-to Guide
                    </span>
                    <span class="px-2 py-1 text-xs font-medium border rounded bg-yellow-500/20 text-yellow-400 border-yellow-500">
                        Intermediate
                    </span>
                    <span class="px-2 py-1 text-xs font-medium border rounded bg-gray-700 text-gray-300 border-gray-600">
                        NextPy 5.0.0
                    </span>
                </div>
                
                <h1 class="text-4xl font-bold text-white">
                    Database Integration
                </h1>
                
                <p class="mt-4 text-lg text-gray-400">
                    Learn how to integrate databases into your NextPy application using SQLAlchemy and perform CRUD operations.
                </p>
            </div>
            
            <div class="my-6 p-4 border border-gray-700 bg-gray-800 rounded-lg">
                <div class="flex items-start gap-3">
                    <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                    </svg>
                    <div class="flex-1">
                        <h4 class="font-semibold text-gray-200">Prerequisites</h4>
                        <ul class="mt-2 space-y-1 text-sm text-gray-400">
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
                                Basic SQL knowledge
                            </li>
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                PostgreSQL or SQLite installed
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <section id="overview" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    What You'll Learn
                </h2>
                <p class="text-gray-300 mb-4">
                    This guide covers:
                </p>
                <ul class="list-disc list-inside space-y-2 text-gray-300 ml-4">
                    <li>Setting up SQLAlchemy with NextPy</li>
                    <li>Creating database models</li>
                    <li>Database migrations</li>
                    <li>CRUD operations</li>
                    <li>Relationships between models</li>
                    <li>Query optimization</li>
                </ul>
            </section>
            
            <section id="setup" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Step 1: Database Setup
                </h2>
                <p class="text-gray-300 mb-4">
                    Install the required dependencies:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            bash
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-bash">pip install sqlalchemy psycopg2-binary python-dotenv</code>
                    </pre>
                </div>
                
                <p class="text-gray-300 mb-4 mt-6">
                    Configure database connection in main.py:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">main.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()</code>
                    </pre>
                </div>
            </section>
            
            <section id="models" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Step 2: Create Models
                </h2>
                <p class="text-gray-300 mb-4">
                    Create database models using SQLAlchemy:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">models/user.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)</code>
                    </pre>
                </div>
                
                <div class="my-6 p-4 border-l-4 border-purple-500 bg-purple-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-purple-400">Tip</h4>
                            <div class="mt-1 text-sm text-gray-300">
                                Use index=True on columns that you'll frequently query or filter by. This improves query performance.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="migrations" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Step 3: Create Tables
                </h2>
                <p class="text-gray-300 mb-4">
                    Create database tables from your models:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">models/__init__.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from models.user import Base, User
from main import engine

# Create all tables
Base.metadata.create_all(bind=engine)</code>
                    </pre>
                </div>
                
                <div class="my-6 p-4 border-l-4 border-yellow-500 bg-yellow-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-yellow-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-yellow-400">Production Note</h4>
                            <div class="mt-1 text-sm text-gray-300">
                                For production, use Alembic for database migrations instead of creating tables directly. This allows you to version and rollback schema changes.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="crud" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Step 4: CRUD Operations
                </h2>
                <p class="text-gray-300 mb-4">
                    Perform Create, Read, Update, and Delete operations:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">CRUD operations</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from main import get_db
from models.user import User

# CREATE
def create_user(email, username, full_name):
    db = next(get_db())
    user = User(email=email, username=username, full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# READ
def get_user(user_id):
    db = next(get_db())
    return db.query(User).filter(User.id == user_id).first()

def get_all_users():
    db = next(get_db())
    return db.query(User).all()

# UPDATE
def update_user(user_id, **kwargs):
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

# DELETE
def delete_user(user_id):
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user</code>
                    </pre>
                </div>
            </section>
            
            <section id="relationships" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Step 5: Model Relationships
                </h2>
                <p class="text-gray-300 mb-4">
                    Create relationships between models:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">models/post.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.user import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)
    
    # Relationship
    user = relationship("User", back_populates="posts")

# Update User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    
    # Relationship
    posts = relationship("Post", back_populates="user")</code>
                    </pre>
                </div>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">Using relationships</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python"># Get user with their posts
user = db.query(User).filter(User.id == 1).first()
for post in user.posts:
    print(post.title)

# Get post with author
post = db.query(Post).filter(Post.id == 1).first()
print(post.user.full_name)</code>
                    </pre>
                </div>
            </section>
            
            <section id="queries" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Step 6: Advanced Queries
                </h2>
                <p class="text-gray-300 mb-4">
                    Use advanced query features:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">Advanced queries</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from sqlalchemy import or_, and_, desc

# Filter with OR
users = db.query(User).filter(
    or_(User.email.like("%gmail%"), User.email.like("%yahoo%"))
).all()

# Filter with AND
users = db.query(User).filter(
    and_(User.email.like("%gmail%"), User.full_name.like("%John%"))
).all()

# Order by
users = db.query(User).order_by(desc(User.created_at)).all()

# Limit and offset
users = db.query(User).limit(10).offset(20).all()

# Count
count = db.query(User).count()

# Join
results = db.query(User, Post).join(Post).all()</code>
                    </pre>
                </div>
            </section>
            
            <section id="best-practices" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Best Practices
                </h2>
                <ul class="space-y-3 text-gray-300">
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Always use environment variables for database URLs</span>
                    </li>
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Use connection pooling in production</span>
                    </li>
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Implement proper error handling for database operations</span>
                    </li>
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Use Alembic for production migrations</span>
                    </li>
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Index frequently queried columns</span>
                    </li>
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Use eager loading (joinedload) to avoid N+1 queries</span>
                    </li>
                </ul>
            </section>
            
            <section id="summary" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Summary
                </h2>
                <p class="text-gray-300 mb-4">
                    You've learned how to:
                </p>
                <ul class="list-disc list-inside space-y-2 text-gray-300 ml-4">
                    <li>✅ Set up SQLAlchemy with NextPy</li>
                    <li>✅ Create database models</li>
                    <li>✅ Perform CRUD operations</li>
                    <li>✅ Create model relationships</li>
                    <li>✅ Write advanced queries</li>
                    <li>✅ Follow database best practices</li>
                </ul>
            </section>
        </article>
        <aside class="hidden lg:block">
            <div class="sticky top-24 text-sm">
                <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What You'll Learn</a></li>
                        <li><a href="#setup" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 1: Database Setup</a></li>
                        <li><a href="#models" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 2: Create Models</a></li>
                        <li><a href="#migrations" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 3: Create Tables</a></li>
                        <li><a href="#crud" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 4: CRUD Operations</a></li>
                        <li><a href="#relationships" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 5: Relationships</a></li>
                        <li><a href="#queries" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 6: Advanced Queries</a></li>
                        <li><a href="#best-practices" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Best Practices</a></li>
                        <li><a href="#summary" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Summary</a></li>
                </ul>
            </div>
        </aside>
        </div>
        </div>
        """)





default = DatabaseGuide

@interactive_component
def DocsScrollSpy():
    [scroll_progress, set_scroll_progress] = useState(0)

    def SetupScroll():
        def OnScroll():
            doc_height = document.documentElement.scrollHeight - window.innerHeight
            if doc_height > 0:
                set_scroll_progress((window.scrollY / doc_height) * 100)

            current = ""
            sections = document.querySelectorAll("article div[id], article header[id], section[id]")
            for sec in sections:
                rect = sec.getBoundingClientRect()
                if rect.top <= 160:
                    current = sec.id
                in_view = rect.top < window.innerHeight * 0.92 and rect.bottom > 0
                if in_view:
                    sec.setAttribute("data-docs-revealed", "")
                else:
                    sec.removeAttribute("data-docs-revealed")

            links = document.querySelectorAll("aside a[href^='#'], nav a[href^='#']")
            for a in links:
                if a.getAttribute("href") == "#" + current:
                    a.setAttribute("data-docs-toc-active", "")
                else:
                    a.removeAttribute("data-docs-toc-active")

            path = window.location.pathname
            nav_links = document.querySelectorAll("aside a[href^='/']")
            for a in nav_links:
                if a.getAttribute("href") == path:
                    a.setAttribute("data-docs-nav-active", "")
                    parent = a.closest("details")
                    if parent:
                        parent.setAttribute("open", "")
                else:
                    a.removeAttribute("data-docs-nav-active")

        sections = document.querySelectorAll("article div[id], article header[id], section[id]")
        for sec in sections:
            sec.setAttribute("data-docs-reveal", "")

        window.addEventListener("scroll", OnScroll)
        document.addEventListener("nextpy:navigate", OnScroll)
        OnScroll()
        return lambda: window.removeEventListener("scroll", OnScroll)

    useEffect(SetupScroll, [])

    progress_style = f"width: {scroll_progress}%"

    return (
        <div class="fixed top-0 left-0 right-0 z-[70] h-[3px] pointer-events-none">
            <div style={progress_style} class="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 transition-[width] duration-100"></div>
        </div>
    )

register_component("DocsScrollSpy", DocsScrollSpy)
