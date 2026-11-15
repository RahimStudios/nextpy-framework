from nextpy.psx import register_component, component, psx, Link


@component
def DatabaseGuide():
    return psx("""
        <div class="mx-auto max-w-6xl">
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full">
        <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 pb-24 pt-6">
                        <!-- Top Breadcrumb & Actions -->
            <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                <div class="flex items-center gap-2 text-sm font-medium text-zinc-300">
                    <span>Documentation</span>
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                    <span class="text-white">Database Integration</span>
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
                    Database Integration
                </h1>
                <p class="leading-relaxed text-zinc-300">
                    Learn how to integrate databases into your NextPy application using SQLAlchemy and perform CRUD operations.
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
            
            <section id="overview" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    What You'll Learn
                </h2>
                <p class="text-zinc-300 mb-4">
                    This guide covers:
                </p>
                <ul class="list-disc list-inside space-y-2 text-zinc-300 ml-4">
                    <li>Setting up SQLAlchemy with NextPy</li>
                    <li>Creating database models</li>
                    <li>Database migrations</li>
                    <li>CRUD operations</li>
                    <li>Relationships between models</li>
                    <li>Query optimization</li>
                </ul>
            </section>
            
            <section id="setup" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 1: Database Setup
                </h2>
                <p class="text-zinc-300 mb-4">
                    Install the required dependencies:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            bash
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-bash">pip install sqlalchemy psycopg2-binary python-dotenv</code>
                    </pre>
                </div>
                
                <p class="text-zinc-300 mb-4 mt-6">
                    Configure database connection in main.py:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">main.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
            
            <section id="models" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 2: Create Models
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create database models using SQLAlchemy:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">models/user.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
                            <div class="mt-1 text-sm text-zinc-300">
                                Use index=True on columns that you'll frequently query or filter by. This improves query performance.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="migrations" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 3: Create Tables
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create database tables from your models:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">models/__init__.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
                            <div class="mt-1 text-sm text-zinc-300">
                                For production, use Alembic for database migrations instead of creating tables directly. This allows you to version and rollback schema changes.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="crud" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 4: CRUD Operations
                </h2>
                <p class="text-zinc-300 mb-4">
                    Perform Create, Read, Update, and Delete operations:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">CRUD operations</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
            
            <section id="relationships" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 5: Model Relationships
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create relationships between models:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">models/post.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">Using relationships</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
            
            <section id="queries" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 6: Advanced Queries
                </h2>
                <p class="text-zinc-300 mb-4">
                    Use advanced query features:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">Advanced queries</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
            
            <section id="nextpy-db" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 7: nextpy.db Helpers
                </h2>
                <p class="text-zinc-300 mb-4">
                    NextPy ships a managed SQLAlchemy layer in <code class="font-mono text-sm">nextpy.db</code>. Instead of wiring up your own engine, call <code class="font-mono text-sm">init_db()</code> once and use the helpers below — they work with both the built-in models and your own <code class="font-mono text-sm">Base</code> models.
                </p>

                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">nextpy.db helpers</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.db import (
    init_db, get_session, session, transaction,
    paginate, apply_filters, get_or_none, get_or_404,
    batch_get, eager_load, serialize_model, count_by,
)

# Initialize once at startup — creates all tables, returns the Database
db_manager = init_db()   # or init_db("postgresql+psycopg2://user:pass@host/db")

db = get_session()       # session() is an alias

# Atomic writes: commits on success, rolls back on error
with transaction() as db:
    user = User(email="a@b.com", username="ann")
    db.add(user)

# Fetch helpers
user = get_or_none(db, User, 1)              # -> User or None
post = get_or_404(db, Post, 7, "Post")       # -> raises LookupError

# Batch fetch: one query, dict keyed by column
rows = batch_get(db, Job, [1, 2, 3], key="id")

# Eager-load relationships (selectinload — avoids N+1 queries)
jobs = eager_load(db.query(Job), Job.employer, Job.applications).all()

# Safe dynamic filtering from query params
q = db.query(Post)
q = apply_filters(q, Post, filters=params.get("filters"),
                  allowed=["published", "author_id"],
                  search=params.get("q"),
                  search_fields=["title", "excerpt"])
page = paginate(q, page=params.get("page", 1), per_page=20)
# page.items, page.total, page.pages, page.has_next, page.has_prev

# Serialize a model to a JSON-safe dict (datetimes -> ISO strings)
data = serialize_model(user, exclude=["hashed_password"])

# Grouped counts in one GROUP BY query
counts = count_by(db, Application, "status", filters={"job_id": 5})</code>
                    </pre>
                </div>

                <div class="my-6 p-4 border-l-4 border-blue-500 bg-blue-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-blue-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-blue-400">Configuration</h4>
                            <div class="mt-1 text-sm text-zinc-300">
                                The database URL comes from the <code class="font-mono text-xs">DATABASE_URL</code> environment variable (default <code class="font-mono text-xs">sqlite:///./nextpy.db</code>, resolved to an absolute path). Pooling and echo are tuned with <code class="font-mono text-xs">DB_POOL_SIZE</code>, <code class="font-mono text-xs">DB_MAX_OVERFLOW</code>, and <code class="font-mono text-xs">DB_ECHO</code>. For PostgreSQL, install <code class="font-mono text-xs">psycopg2-binary</code>.
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="built-in-models" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 8: Built-in Models
                </h2>
                <p class="text-zinc-300 mb-4">
                    <code class="font-mono text-sm">nextpy.db</code> ships ready-made models on the shared <code class="font-mono text-sm">Base</code> declarative base, so <code class="font-mono text-sm">init_db()</code> creates their tables automatically:
                </p>
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">Built-in models</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.db import User, UserSession, Post, Todo, Job, Application

# User        - id, email, username, full_name, hashed_password,
#               role (job_seeker | employer), bio, company_name,
#               is_active, created_at
# UserSession - id, user_id, created_at, expires_at
#               (database-backed login sessions that survive restarts)
# Post        - id, title, slug, content, excerpt, author_id,
#               published, created_at, updated_at
# Todo        - id, title, completed, created_at, updated_at
# Job         - id, title, company, location, description,
#               salary_min, salary_max, job_type, experience_level,
#               employer_id -&gt; users.id, is_active
#               relationships: applications, employer
# Application - id, job_id -&gt; jobs.id, applicant_id -&gt; users.id,
#               cover_letter, resume_url, status (pending|accepted|rejected)
#               relationships: job, applicant (lazy="joined")</code>
                    </pre>
                </div>
                <p class="text-zinc-300 mb-4">
                    Define your own models by subclassing <code class="font-mono text-sm">Base</code> (also exported as <code class="font-mono text-sm">Model</code>) exactly as shown in Step 2 — they are created by the same <code class="font-mono text-sm">create_all</code> call inside <code class="font-mono text-sm">init_db()</code>.
                </p>
            </section>

            <section id="live-crud" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 9: Live CRUD Lists
                </h2>
                <p class="text-zinc-300 mb-4">
                    Add a <code class="font-mono text-sm">data-nextpy-crud</code> attribute containing a JSON config and the built-in CRUD runtime wires your list to server actions — create forms, toggle checkboxes, and delete buttons all work without custom JavaScript, and rows update live over a WebSocket channel.
                </p>

                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">pages/todos.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.psx import component, useCrudEvent

@component
def Todos():
    event = useCrudEvent(resource="todos")
    return (
        &lt;div data-nextpy-crud={'{"resource": "todos",'
                                '"createAction": "create_todo",'
                                '"updateAction": "update_todo",'
                                '"deleteAction": "delete_todo"}'}&gt;
            &lt;form data-nextpy-action="create"&gt;
                &lt;input data-nextpy-field="title" placeholder="New todo" /&gt;
                &lt;button type="submit"&gt;Add&lt;/button&gt;
            &lt;/form&gt;
            &lt;ul data-nextpy-list&gt;
                &lt;li data-nextpy-item="1"&gt;
                    &lt;input type="checkbox" data-nextpy-toggle="1" /&gt;
                    &lt;span data-nextpy-field="title"&gt;Buy milk&lt;/span&gt;
                    &lt;button data-nextpy-delete="1"&gt;Delete&lt;/button&gt;
                &lt;/li&gt;
            &lt;/ul&gt;
            &lt;p data-nextpy-error class="hidden"&gt;&lt;/p&gt;
            &lt;span data-nextpy-status&gt;&lt;/span&gt;
        &lt;/div&gt;
    )</code>
                    </pre>
                </div>

                <p class="text-zinc-300 mb-4">
                    Config keys: <code class="font-mono text-sm">resource</code>, <code class="font-mono text-sm">createAction</code>/<code class="font-mono text-sm">updateAction</code>/<code class="font-mono text-sm">deleteAction</code> (defaults <code class="font-mono text-sm">"create"</code>/<code class="font-mono text-sm">"update"</code>/<code class="font-mono text-sm">"delete"</code>), <code class="font-mono text-sm">idParam</code> (default <code class="font-mono text-sm">"id"</code>), <code class="font-mono text-sm">updateFields</code>, <code class="font-mono text-sm">deleteConfirm</code> (<code class="font-mono text-sm">false</code>, a message string, or <code class="font-mono text-sm">"psx"</code> for a PSX-rendered modal), <code class="font-mono text-sm">createReset</code>, and <code class="font-mono text-sm">wsChannel</code>/<code class="font-mono text-sm">messageType</code>.
                </p>
                <p class="text-zinc-300 mb-4">
                    Inside an <code class="font-mono text-sm">interactive_component</code>, <code class="font-mono text-sm">useCrudEvent(resource="todos")</code> subscribes to <code class="font-mono text-sm">nextpy:crud:changed</code> events and returns <code class="font-mono text-sm">&#123;"data": ..., "_eventKey": ...&#125;</code> so your UI can react to <code class="font-mono text-sm">created</code>/<code class="font-mono text-sm">updated</code>/<code class="font-mono text-sm">deleted</code> changes. See the <Link href="/documentation/reference/components" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">Components API</Link> for the full attribute reference.
                </p>
            </section>

            <section id="best-practices" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Best Practices
                </h2>
                <ul class="space-y-3 text-zinc-300">
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
            
            <section id="summary" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Summary
                </h2>
                <p class="text-zinc-300 mb-4">
                    You've learned how to:
                </p>
                <ul class="list-disc list-inside space-y-2 text-zinc-300 ml-4">
                    <li>✅ Set up SQLAlchemy with NextPy</li>
                    <li>✅ Create database models</li>
                    <li>✅ Perform CRUD operations</li>
                    <li>✅ Create model relationships</li>
                    <li>✅ Write advanced queries</li>
                    <li>✅ Follow database best practices</li>
                </ul>
            </section>
            <!-- Footer Pagination -->
            <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                <div class="w-1/2">
                    <Link href="/documentation/howto/auth" class="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                        <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                        <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                            <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                            Implement Authentication
                        </span>
                    </Link>
                </div>
                <div class="w-1/2 text-right">
                    <Link href="/documentation/howto/api" class="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                        <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                        <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                            API Development
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
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What You'll Learn</a></li>
                        <li><a href="#setup" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 1: Database Setup</a></li>
                        <li><a href="#models" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 2: Create Models</a></li>
                        <li><a href="#migrations" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 3: Create Tables</a></li>
                        <li><a href="#crud" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 4: CRUD Operations</a></li>
                        <li><a href="#relationships" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 5: Relationships</a></li>
                        <li><a href="#queries" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 6: Advanced Queries</a></li>
                        <li><a href="#nextpy-db" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 7: nextpy.db Helpers</a></li>
                        <li><a href="#built-in-models" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 8: Built-in Models</a></li>
                        <li><a href="#live-crud" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 9: Live CRUD Lists</a></li>
                        <li><a href="#best-practices" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Best Practices</a></li>
                        <li><a href="#summary" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Summary</a></li>
                </ul>
            </div>
        </aside>
        </div>
        </div>
        """)


default = DatabaseGuide

