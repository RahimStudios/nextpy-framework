from nextpy.psx import register_component, component, psx, interactive_component, useState, Link


@component
def AuthenticationGuide():
    return psx("""
        <div class="mx-auto max-w-6xl">
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full">
        <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 pb-24 pt-6">
                        <!-- Top Breadcrumb & Actions -->
            <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                <div class="flex items-center gap-2 text-sm font-medium text-zinc-300">
                    <span>Documentation</span>
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                    <span class="text-white">Implement Authentication</span>
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
                    Implement Authentication
                </h1>
                <p class="leading-relaxed text-zinc-300">
                    Learn how to add user authentication to your NextPy application with login, registration, and session management.
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
                                Completed Todo App tutorial
                            </li>
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                Basic understanding of server actions
                            </li>
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                Database set up (SQLAlchemy)
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
                    <li>Setting up user models with SQLAlchemy</li>
                    <li>Creating server actions for authentication</li>
                    <li>Implementing login and registration forms</li>
                    <li>Managing sessions and cookies</li>
                    <li>Protecting routes with authentication</li>
                </ul>
            </section>
            
            <section id="user-model" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 1: Create User Model
                </h2>
                <p class="text-zinc-300 mb-4">
                    First, create a user model to store user credentials:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">models/user.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    
    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)</code>
                    </pre>
                </div>
                
                <div class="my-6 p-4 border-l-4 border-yellow-500 bg-yellow-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-yellow-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-yellow-400">Security Note</h4>
                            <div class="mt-1 text-sm text-zinc-300">
                                Never store passwords in plain text. Always use bcrypt or another secure hashing algorithm.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="auth-actions" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 2: Create Authentication Actions
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create server actions for registration and login:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">pages/auth/actions.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.server_actions import server_action
from models.user import User
from nextpy.db import get_db

@server_action()
def register(email, username, full_name, password):
    db = get_db()
    
    # Check if user exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return {"success": False, "error": "Email already registered"}
    
    # Create new user
    user = User(
        email=email.lower().strip(),
        username=username,
        full_name=full_name
    )
    user.set_password(password)
    
    db.add(user)
    db.commit()
    
    return {"success": True, "user": {"id": user.id, "email": user.email}}

@server_action()
def login(email, password):
    db = get_db()
    
    # Find user
    user = db.query(User).filter(User.email == email.lower().strip()).first()
    if not user or not user.verify_password(password):
        return {"success": False, "error": "Invalid credentials"}
    
    # Create session
    return {
        "success": True,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name
        }
    }</code>
                    </pre>
                </div>
            </section>
            
            <section id="login-page" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 3: Create Login Page
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create a login page with form validation:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">pages/auth/login.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.psx import component, interactive_component, useState, callServerAction

@interactive_component
def LoginPage():
    [email, setEmail] = useState("")
    [password, setPassword] = useState("")
    [error, setError] = useState("")
    [loading, setLoading] = useState(False)
    
    def handle_login(e):
        e.preventDefault()
        setLoading(True)
        setError("")
        
        result = callServerAction("login", {"email": email, "password": password})
        
        if result.get("success"):
            window.location.href = "/dashboard"
        else:
            setError(result.get("error", "Login failed"))
            setLoading(False)
    
    return (
        &lt;div class="min-h-screen flex items-center justify-center bg-gray-900"&gt;
            &lt;div class="max-w-md w-full p-8 bg-gray-800 rounded-lg"&gt;
                &lt;h1 class="text-2xl font-semibold text-white tracking-tight mb-6"&gt;Login&lt;/h1&gt;
                
                {if error:
                    &lt;div class="mb-4 p-3 text-red-400 bg-red-900/20 rounded"&gt;
                        {error}
                    &lt;/div&gt;
                }
                
                &lt;form onsubmit="handle_login" class="space-y-4"&gt;
                    &lt;div&gt;
                        &lt;label class="block text-sm font-medium text-gray-300 mb-2"&gt;Email&lt;/label&gt;
                        &lt;input 
                            type="email"
                            value={email}
                            oninput={lambda e: setEmail(e.target.value)}
                            required
                            class="w-full px-4 py-2 rounded-lg border border-zinc-600 bg-zinc-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        /&gt;
                    &lt;/div&gt;
                    
                    &lt;div&gt;
                        &lt;label class="block text-sm font-medium text-gray-300 mb-2"&gt;Password&lt;/label&gt;
                        &lt;input 
                            type="password"
                            value={password}
                            oninput={lambda e: setPassword(e.target.value)}
                            required
                            class="w-full px-4 py-2 rounded-lg border border-zinc-600 bg-zinc-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        /&gt;
                    &lt;/div&gt;
                    
                    &lt;button 
                        type="submit"
                        disabled={loading}
                        class="w-full px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                    &gt;
                        {loading ? "Logging in..." : "Login"}
                    &lt;/button&gt;
                &lt;/form&gt;
                
                &lt;p class="mt-4 text-center text-gray-400"&gt;
                    Don't have an account? &lt;a href="/auth/register" class="text-blue-400 hover:text-blue-300"&gt;Register&lt;/a&gt;
                &lt;/p&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    )


default = LoginPage</code>
                    </pre>
                </div>
            </section>
            
            <section id="register-page" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 4: Create Registration Page
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create a registration page similar to login:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">pages/auth/register.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.psx import component, interactive_component, useState, callServerAction

@interactive_component
def RegisterPage():
    [email, setEmail] = useState("")
    [username, setUsername] = useState("")
    [full_name, setFullName] = useState("")
    [password, setPassword] = useState("")
    [error, setError] = useState("")
    [loading, setLoading] = useState(False)
    
    def handle_register(e):
        e.preventDefault()
        setLoading(True)
        setError("")
        
        result = callServerAction("register", {
            "email": email,
            "username": username,
            "full_name": full_name,
            "password": password
        })
        
        if result.get("success"):
            window.location.href = "/auth/login"
        else:
            setError(result.get("error", "Registration failed"))
            setLoading(False)
    
    return (
        &lt;div class="min-h-screen flex items-center justify-center bg-gray-900"&gt;
            &lt;div class="max-w-md w-full p-8 bg-gray-800 rounded-lg"&gt;
                &lt;h1 class="text-2xl font-semibold text-white tracking-tight mb-6"&gt;Register&lt;/h1&gt;
                
                {if error:
                    &lt;div class="mb-4 p-3 text-red-400 bg-red-900/20 rounded"&gt;
                        {error}
                    &lt;/div&gt;
                }
                
                &lt;form onsubmit="handle_register" class="space-y-4"&gt;
                    &lt;div&gt;
                        &lt;label class="block text-sm font-medium text-gray-300 mb-2"&gt;Full Name&lt;/label&gt;
                        &lt;input 
                            type="text"
                            value={full_name}
                            oninput={lambda e: setFullName(e.target.value)}
                            required
                            class="w-full px-4 py-2 rounded-lg border border-zinc-600 bg-zinc-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        /&gt;
                    &lt;/div&gt;
                    
                    &lt;div&gt;
                        &lt;label class="block text-sm font-medium text-gray-300 mb-2"&gt;Username&lt;/label&gt;
                        &lt;input 
                            type="text"
                            value={username}
                            oninput={lambda e: setUsername(e.target.value)}
                            required
                            class="w-full px-4 py-2 rounded-lg border border-zinc-600 bg-zinc-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        /&gt;
                    &lt;/div&gt;
                    
                    &lt;div&gt;
                        &lt;label class="block text-sm font-medium text-gray-300 mb-2"&gt;Email&lt;/label&gt;
                        &lt;input 
                            type="email"
                            value={email}
                            oninput={lambda e: setEmail(e.target.value)}
                            required
                            class="w-full px-4 py-2 rounded-lg border border-zinc-600 bg-zinc-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        /&gt;
                    &lt;/div&gt;
                    
                    &lt;div&gt;
                        &lt;label class="block text-sm font-medium text-gray-300 mb-2"&gt;Password&lt;/label&gt;
                        &lt;input 
                            type="password"
                            value={password}
                            oninput={lambda e: setPassword(e.target.value)}
                            required
                            class="w-full px-4 py-2 rounded-lg border border-zinc-600 bg-zinc-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        /&gt;
                    &lt;/div&gt;
                    
                    &lt;button 
                        type="submit"
                        disabled={loading}
                        class="w-full px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                    &gt;
                        {loading ? "Registering..." : "Register"}
                    &lt;/button&gt;
                &lt;/form&gt;
                
                &lt;p class="mt-4 text-center text-gray-400"&gt;
                    Already have an account? &lt;a href="/auth/login" class="text-blue-400 hover:text-blue-300"&gt;Login&lt;/a&gt;
                &lt;/p&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    )

default = RegisterPage</code>
                    </pre>
                </div>
            </section>
            
            <section id="middleware" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Step 5: Protect Routes
                </h2>
                <p class="text-zinc-300 mb-4">
                    Create middleware to protect authenticated routes:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">middleware/auth.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from fastapi import Request, HTTPException
from functools import wraps

def require_auth(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        # Check session cookie
        session = request.cookies.get("session")
        if not session:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        # Validate session
        # Add your session validation logic here
        
        return await func(request, *args, **kwargs)
    return wrapper</code>
                    </pre>
                </div>
            </section>
            
            <section id="best-practices" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Security Best Practices
                </h2>
                <ul class="space-y-3 text-zinc-300">
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Always use HTTPS in production</span>
                    </li>
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Use secure, httpOnly cookies for sessions</span>
                    </li>
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Implement rate limiting to prevent brute force attacks</span>
                    </li>
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Validate and sanitize all user input</span>
                    </li>
                    <li class="flex items-start gap-3">
                        <svg class="mt-1 w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Use environment variables for secrets</span>
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
                    <li>✅ Create user models with password hashing</li>
                    <li>✅ Implement server actions for auth</li>
                    <li>✅ Build login and registration forms</li>
                    <li>✅ Manage sessions and cookies</li>
                    <li>✅ Protect routes with middleware</li>
                </ul>
            </section>
            <!-- Footer Pagination -->
            <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                <div class="w-1/2">
                    <Link href="/documentation/tutorials/dashboard" class="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                        <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                        <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                            <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                            Dashboard App
                        </span>
                    </Link>
                </div>
                <div class="w-1/2 text-right">
                    <Link href="/documentation/howto/database" class="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                        <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                        <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                            Database Integration
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
                        <li><a href="#user-model" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 1: User Model</a></li>
                        <li><a href="#auth-actions" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 2: Auth Actions</a></li>
                        <li><a href="#login-page" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 3: Login Page</a></li>
                        <li><a href="#register-page" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 4: Register Page</a></li>
                        <li><a href="#middleware" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 5: Protect Routes</a></li>
                        <li><a href="#best-practices" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Security Best Practices</a></li>
                        <li><a href="#summary" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Summary</a></li>
                </ul>
            </div>
        </aside>
        </div>
        </div>
        """)


default = AuthenticationGuide

