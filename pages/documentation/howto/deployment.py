from nextpy.psx import register_component, component, psx, interactive_component, useState, useEffect


@component
def DeploymentGuide():
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
                    <span class="px-2 py-1 text-xs font-medium border rounded bg-red-500/20 text-red-400 border-red-500">
                        Advanced
                    </span>
                    <span class="px-2 py-1 text-xs font-medium border rounded bg-gray-700 text-gray-300 border-gray-600">
                        NextPy 5.0.0
                    </span>
                </div>
                
                <h1 class="text-4xl font-bold text-white">
                    Deploy Your NextPy App
                </h1>
                
                <p class="mt-4 text-lg text-gray-400">
                    Learn how to deploy your NextPy application to production using various platforms like Render, Vercel, Docker, and more.
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
                                A working NextPy application
                            </li>
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                Git repository (GitHub, GitLab, etc.)
                            </li>
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                Basic knowledge of deployment concepts
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <section id="overview" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Deployment Options
                </h2>
                <p class="text-gray-300 mb-4">
                    NextPy applications can be deployed to various platforms:
                </p>
                <ul class="list-disc list-inside space-y-2 text-gray-300 ml-4">
                    <li>Render - Simple, free tier available</li>
                    <li>Vercel - Fast previews, edge deployment</li>
                    <li>Docker - Container-based deployment</li>
                    <li>AWS/GCP/Azure - Cloud platforms</li>
                    <li>DigitalOcean - VPS deployment</li>
                </ul>
            </section>
            
            <section id="render" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Deploy to Render
                </h2>
                <p class="text-gray-300 mb-4">
                    Render offers a free tier for web services and makes deployment simple:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">render.yaml</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            yaml
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-yaml">services:
  - type: web
    name: nextpy-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11</code>
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
                                Make sure your main.py exports the FastAPI app. Render will automatically detect the render.yaml file and configure your service.
                            </div>
                        </div>
                    </div>
                </div>
                
                <h3 class="text-2xl font-semibold text-white mt-8 mb-4">Deployment Steps</h3>
                <ol class="list-decimal list-inside space-y-2 text-gray-300 ml-4">
                    <li>Push your code to GitHub</li>
                    <li>Create a Render account at render.com</li>
                    <li>Click "New +" and select "Web Service"</li>
                    <li>Connect your GitHub repository</li>
                    <li>Render will auto-detect your render.yaml</li>
                    <li>Click "Deploy Web Service"</li>
                </ol>
            </section>
            
            <section id="docker" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Deploy with Docker
                </h2>
                <p class="text-gray-300 mb-4">
                    Docker provides a consistent environment across development and production:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">Dockerfile</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            dockerfile
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-dockerfile">FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]</code>
                    </pre>
                </div>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">.dockerignore</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            text
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-text">__pycache__
*.pyc
.nextpy_framework
.nextpy
.venv
venv
.git
.gitignore
.DS_Store</code>
                    </pre>
                </div>
                
                <h3 class="text-2xl font-semibold text-white mt-8 mb-4">Build and Run</h3>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            bash
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-bash"># Build the image
docker build -t nextpy-app .

# Run the container
docker run -p 8000:8000 nextpy-app</code>
                    </pre>
                </div>
            </section>
            
            <section id="vercel" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Deploy to Vercel
                </h2>
                <p class="text-gray-300 mb-4">
                    Vercel is optimized for Next.js but can also deploy Python applications:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">vercel.json</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            json
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-json">{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}</code>
                    </pre>
                </div>
                
                <div class="my-6 p-4 border-l-4 border-yellow-500 bg-yellow-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-yellow-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-yellow-400">Note</h4>
                            <div class="mt-1 text-sm text-gray-300">
                                Vercel is primarily designed for JavaScript frameworks. For best performance with NextPy, consider using Render or Docker-based deployment.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="environment-variables" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Environment Variables
                </h2>
                <p class="text-gray-300 mb-4">
                    Always use environment variables for sensitive data:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">.env.example</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            text
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-text">DATABASE_URL=postgresql://user:password@localhost/db
SECRET_KEY=your-secret-key-here
DEBUG=False
PORT=8000</code>
                    </pre>
                </div>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">main.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"
PORT = int(os.getenv("PORT", 8000))</code>
                    </pre>
                </div>
                
                <div class="my-6 p-4 border-l-4 border-red-500 bg-red-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-red-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-red-400">Security Warning</h4>
                            <div class="mt-1 text-sm text-gray-300">
                                Never commit .env files to version control. Add .env to your .gitignore file and use environment variable management in your deployment platform.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="production-checklist" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Production Checklist
                </h2>
                <p class="text-gray-300 mb-4">
                    Before deploying to production, ensure you've completed these steps:
                </p>
                
                <div class="space-y-3">
                    <div class="flex items-start gap-3 p-4 border border-gray-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Set DEBUG=False</span>
                            <p class="text-sm text-gray-400">Disable debug mode in production</p>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-3 p-4 border border-gray-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Use HTTPS</span>
                            <p class="text-sm text-gray-400">Enable SSL/TLS for secure connections</p>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-3 p-4 border border-gray-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Secure environment variables</span>
                            <p class="text-sm text-gray-400">Use platform's secret management</p>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-3 p-4 border border-gray-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Database backups</span>
                            <p class="text-sm text-gray-400">Set up automated backups</p>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-3 p-4 border border-gray-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Monitoring and logging</span>
                            <p class="text-sm text-gray-400">Set up error tracking and logging</p>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-3 p-4 border border-gray-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Rate limiting</span>
                            <p class="text-sm text-gray-400">Implement rate limiting to prevent abuse</p>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="summary" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Summary
                </h2>
                <p class="text-gray-300 mb-4">
                    You've learned how to:
                </p>
                <ul class="list-disc list-inside space-y-2 text-gray-300 ml-4">
                    <li>✅ Deploy to Render with render.yaml</li>
                    <li>✅ Containerize your app with Docker</li>
                    <li>✅ Configure Vercel deployment</li>
                    <li>✅ Manage environment variables securely</li>
                    <li>✅ Follow production best practices</li>
                </ul>
                
                <div class="my-6 p-4 border-l-4 border-green-500 bg-green-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-green-400">Ready to Deploy!</h4>
                            <div class="mt-1 text-sm text-gray-300">
                                Your NextPy application is now ready for production. Choose the deployment platform that best fits your needs and budget.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </article>
        <aside class="hidden lg:block">
            <div class="sticky top-24 text-sm">
                <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Deployment Options</a></li>
                        <li><a href="#render" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Deploy to Render</a></li>
                        <li><a href="#docker" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Deploy with Docker</a></li>
                        <li><a href="#vercel" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Deploy to Vercel</a></li>
                        <li><a href="#environment-variables" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Environment Variables</a></li>
                        <li><a href="#production-checklist" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Production Checklist</a></li>
                        <li><a href="#summary" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Summary</a></li>
                </ul>
            </div>
        </aside>
        </div>
        </div>
        """)





default = DeploymentGuide

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
