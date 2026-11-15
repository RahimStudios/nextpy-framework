from nextpy.psx import register_component, component, psx, Link


@component
def DeploymentGuide():
    return psx("""
        <div class="mx-auto max-w-6xl">
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full">
        <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 pb-24 pt-6">
                        <!-- Top Breadcrumb & Actions -->
            <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                <div class="flex items-center gap-2 text-sm font-medium text-zinc-300">
                    <span>Documentation</span>
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                    <span class="text-white">Deploy Your NextPy App</span>
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
                    Deploy Your NextPy App
                </h1>
                <p class="leading-relaxed text-zinc-300">
                    Learn how to deploy your NextPy application to production using various platforms like Render, Vercel, Docker, and more.
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
            
            <section id="overview" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Deployment Options
                </h2>
                <p class="text-zinc-300 mb-4">
                    NextPy applications can be deployed to various platforms:
                </p>
                <ul class="list-disc list-inside space-y-2 text-zinc-300 ml-4">
                    <li>Render - Simple, free tier available</li>
                    <li>Vercel - Fast previews, edge deployment</li>
                    <li>Docker - Container-based deployment</li>
                    <li>AWS/GCP/Azure - Cloud platforms</li>
                    <li>DigitalOcean - VPS deployment</li>
                </ul>
            </section>
            
            <section id="render" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Deploy to Render
                </h2>
                <p class="text-zinc-300 mb-4">
                    Render offers a free tier for web services and makes deployment simple:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">render.yaml</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
                            <div class="mt-1 text-sm text-zinc-300">
                                Make sure your main.py exports the FastAPI app. Render will automatically detect the render.yaml file and configure your service.
                            </div>
                        </div>
                    </div>
                </div>
                
                <h3 class="text-2xl font-semibold text-white mt-8 mb-4">Deployment Steps</h3>
                <ol class="list-decimal list-inside space-y-2 text-zinc-300 ml-4">
                    <li>Push your code to GitHub</li>
                    <li>Create a Render account at render.com</li>
                    <li>Click "New +" and select "Web Service"</li>
                    <li>Connect your GitHub repository</li>
                    <li>Render will auto-detect your render.yaml</li>
                    <li>Click "Deploy Web Service"</li>
                </ol>
            </section>
            
            <section id="docker" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Deploy with Docker
                </h2>
                <p class="text-zinc-300 mb-4">
                    Docker provides a consistent environment across development and production:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">Dockerfile</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">.dockerignore</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
            
            <section id="vercel" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Deploy to Vercel
                </h2>
                <p class="text-zinc-300 mb-4">
                    Vercel is optimized for Next.js but can also deploy Python applications:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">vercel.json</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
                            <div class="mt-1 text-sm text-zinc-300">
                                Vercel is primarily designed for JavaScript frameworks. For best performance with NextPy, consider using Render or Docker-based deployment.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="environment-variables" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Environment Variables
                </h2>
                <p class="text-zinc-300 mb-4">
                    Always use environment variables for sensitive data:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">.env.example</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
                
                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">main.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
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
                            <div class="mt-1 text-sm text-zinc-300">
                                Never commit .env files to version control. Add .env to your .gitignore file and use environment variable management in your deployment platform.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="asgi-deployment" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    ASGI Deployment
                </h2>
                <p class="text-zinc-300 mb-4">
                    A NextPy project entry point (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">main.py</code>) builds and exports a standard ASGI application:
                </p>

                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">main.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">import nextpy as nx

app = nx.create_app(
    pages_dir="pages",
    templates_dir="templates",
    public_dir="public",
    out_dir="out",
    debug=settings["debug"],
)</code>
                    </pre>
                </div>

                <p class="text-zinc-300 mb-4">
                    Because <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">app</code> is a plain ASGI callable, any ASGI server can host it. The project also ships an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">asgi.py</code> entry point that compiles Tailwind CSS, initializes the database, and exposes the same <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">app</code> object for platforms that prefer it.
                </p>

                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            bash
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-bash"># Uvicorn (single worker — dev/staging)
uvicorn main:app --host 0.0.0.0 --port $PORT

# Uvicorn with multiple workers (production)
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4

# Gunicorn with the Uvicorn worker class
gunicorn main:app -k uvicorn.workers.UvicornWorker \
    --workers 4 --bind 0.0.0.0:$PORT</code>
                    </pre>
                </div>

                <div class="my-6 p-4 border-l-4 border-blue-500 bg-blue-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-blue-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-blue-400">Note</h4>
                            <div class="mt-1 text-sm text-zinc-300">
                                When you run uvicorn/gunicorn directly, set <code class="text-zinc-200 font-mono text-xs">DEBUG=false</code> and <code class="text-zinc-200 font-mono text-xs">DEVELOPMENT=false</code> in your environment — otherwise the app boots in development mode. <code class="text-zinc-200 font-mono text-xs">nextpy start</code> sets these for you automatically.
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="build-start-export" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Build, Start &amp; Export
                </h2>
                <p class="text-zinc-300 mb-4">
                    The CLI wraps the ASGI server and static builder for common workflows:
                </p>

                <div class="my-6 overflow-x-auto rounded-lg border border-zinc-700">
                    <table class="w-full text-sm text-left">
                        <thead class="bg-zinc-800 text-zinc-300">
                            <tr>
                                <th class="px-4 py-3 font-semibold">Command</th>
                                <th class="px-4 py-3 font-semibold">What it does</th>
                                <th class="px-4 py-3 font-semibold">Output</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-zinc-800 text-zinc-300">
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">nextpy build</td>
                                <td class="px-4 py-3">Static build with optimization (minify, tree-shake report, code splitting)</td>
                                <td class="px-4 py-3 font-mono text-xs">out/ + build manifest</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">nextpy start</td>
                                <td class="px-4 py-3">Production server: uvicorn on <code class="text-zinc-200 font-mono text-xs">main:app</code> with 4 workers, debug disabled, log level warning</td>
                                <td class="px-4 py-3 font-mono text-xs">live server on :5000</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">nextpy export</td>
                                <td class="px-4 py-3">Static export for CDN/static hosting (no server)</td>
                                <td class="px-4 py-3 font-mono text-xs">out/ static files</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            bash
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-bash">nextpy build --out dist          # optimized static build
nextpy export --out public_html    # plain static export
nextpy start --port 8080           # production server (DEBUG=false forced)</code>
                    </pre>
                </div>

                <p class="text-zinc-300 mb-4">
                    <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy start</code> overrides your <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.env</code>: it sets <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">DEBUG=false</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NEXTPY_DEBUG=false</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">DEVELOPMENT=false</code> before booting uvicorn with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">workers=1</code> by default (set <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">NEXTPY_WORKERS</code> to scale out &mdash; note WebSocket channels and state sync are per-process) and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">log_level="warning"</code>. For anything more custom (different worker count, SSL, process manager), use the ASGI commands above.
                </p>
            </section>

            <section id="production-env" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Production Environment Variables
                </h2>
                <p class="text-zinc-300 mb-4">
                    Settings are read from the project <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.env</code> (loaded by <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.config</code>) or real environment variables. For production, set at minimum:
                </p>

                <div class="my-6 overflow-x-auto rounded-lg border border-zinc-700">
                    <table class="w-full text-sm text-left">
                        <thead class="bg-zinc-800 text-zinc-300">
                            <tr>
                                <th class="px-4 py-3 font-semibold">Variable</th>
                                <th class="px-4 py-3 font-semibold">Production value</th>
                                <th class="px-4 py-3 font-semibold">Why</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-zinc-800 text-zinc-300">
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">DEBUG</td>
                                <td class="px-4 py-3 font-mono text-xs">false</td>
                                <td class="px-4 py-3">Sanitizes error pages — no tracebacks or file paths leak</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">DEVELOPMENT</td>
                                <td class="px-4 py-3 font-mono text-xs">false</td>
                                <td class="px-4 py-3">Disables the HMR file watcher and <code class="text-zinc-200 font-mono text-xs">/__nextpy/hmr</code></td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">NEXTPY_DEBUG</td>
                                <td class="px-4 py-3 font-mono text-xs">false</td>
                                <td class="px-4 py-3">Removes the debug panel and <code class="text-zinc-200 font-mono text-xs">/__nextpy/debug/*</code> routes</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">NEXTPY_HOT_RELOAD</td>
                                <td class="px-4 py-3 font-mono text-xs">false</td>
                                <td class="px-4 py-3">Turns off reload signaling</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">NEXTPY_LOG_LEVEL</td>
                                <td class="px-4 py-3 font-mono text-xs">warning</td>
                                <td class="px-4 py-3">Quiets framework logs (trace|debug|info|warning|error)</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">SECRET_KEY</td>
                                <td class="px-4 py-3 font-mono text-xs">&lt;random secret&gt;</td>
                                <td class="px-4 py-3">Defaults to <code class="text-zinc-200 font-mono text-xs">change-me-in-production</code> — always override</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">JWT_SECRET / SESSION_SECRET</td>
                                <td class="px-4 py-3 font-mono text-xs">&lt;random secrets&gt;</td>
                                <td class="px-4 py-3">Auth token signing — defaults are <code class="text-zinc-200 font-mono text-xs">change-me</code></td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">DATABASE_URL</td>
                                <td class="px-4 py-3 font-mono text-xs">postgresql://…</td>
                                <td class="px-4 py-3">Production database (defaults to local SQLite)</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-mono text-zinc-200">HOST / PORT</td>
                                <td class="px-4 py-3 font-mono text-xs">0.0.0.0 / $PORT</td>
                                <td class="px-4 py-3">Bind address and port for the ASGI server</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="my-6 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-zinc-700 bg-zinc-800">
                        <span class="text-sm text-zinc-400 font-mono">.env.production</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-zinc-300 uppercase bg-zinc-700 rounded">
                            text
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-text">DEBUG=false
DEVELOPMENT=false
NEXTPY_DEBUG=false
NEXTPY_HOT_RELOAD=false
NEXTPY_LOG_LEVEL=warning
SECRET_KEY=&lt;generate-a-long-random-string&gt;
JWT_SECRET=&lt;generate-a-long-random-string&gt;
SESSION_SECRET=&lt;generate-a-long-random-string&gt;
DATABASE_URL=postgresql://user:pass@host:5432/dbname
PORT=8000</code>
                    </pre>
                </div>

                <div class="my-6 p-4 border-l-4 border-yellow-500 bg-yellow-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-yellow-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-yellow-400">Warning</h4>
                            <div class="mt-1 text-sm text-zinc-300">
                                If <code class="text-zinc-200 font-mono text-xs">SECRET_KEY</code>, <code class="text-zinc-200 font-mono text-xs">JWT_SECRET</code> or <code class="text-zinc-200 font-mono text-xs">SESSION_SECRET</code> keep their <code class="text-zinc-200 font-mono text-xs">change-me</code> defaults, sessions and tokens are forgeable. Generate real secrets and inject them via your platform's secret manager — never commit them.
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="production-checklist" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Production Checklist
                </h2>
                <p class="text-zinc-300 mb-4">
                    Before deploying to production, verify each item:
                </p>

                <div class="my-6 overflow-x-auto rounded-lg border border-zinc-700">
                    <table class="w-full text-sm text-left">
                        <thead class="bg-zinc-800 text-zinc-300">
                            <tr>
                                <th class="px-4 py-3 font-semibold">Check</th>
                                <th class="px-4 py-3 font-semibold">How to verify</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-zinc-800 text-zinc-300">
                            <tr>
                                <td class="px-4 py-3 font-medium text-white">Debug flags off</td>
                                <td class="px-4 py-3">DEBUG=false, DEVELOPMENT=false, NEXTPY_DEBUG=false in env (nextpy start sets these)</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-medium text-white">Secrets configured</td>
                                <td class="px-4 py-3">SECRET_KEY, JWT_SECRET, SESSION_SECRET set to random values, not defaults</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-medium text-white">Production database</td>
                                <td class="px-4 py-3">DATABASE_URL points at managed Postgres/MySQL with backups enabled</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-medium text-white">Static assets built</td>
                                <td class="px-4 py-3">nextpy build or nextpy export ran successfully; out/ is deployed or served</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-medium text-white">HTTPS enabled</td>
                                <td class="px-4 py-3">SSL/TLS terminates at the platform or reverse proxy</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-medium text-white">Monitoring &amp; logs</td>
                                <td class="px-4 py-3">Error tracking and log aggregation configured; NEXTPY_LOG_LEVEL=warning</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-medium text-white">Rate limiting</td>
                                <td class="px-4 py-3">RateLimitMiddleware active on API/auth routes (enabled by default)</td>
                            </tr>
                            <tr>
                                <td class="px-4 py-3 font-medium text-white">Smoke test</td>
                                <td class="px-4 py-3">nextpy routes reviewed; key pages and /api routes return 200 in production mode</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <div class="space-y-3">
                    <div class="flex items-start gap-3 p-4 border border-zinc-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Set DEBUG=False</span>
                            <p class="text-sm text-zinc-300">Disable debug mode in production</p>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-3 p-4 border border-zinc-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Use HTTPS</span>
                            <p class="text-sm text-zinc-300">Enable SSL/TLS for secure connections</p>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-3 p-4 border border-zinc-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Secure environment variables</span>
                            <p class="text-sm text-zinc-300">Use platform's secret management</p>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-3 p-4 border border-zinc-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Database backups</span>
                            <p class="text-sm text-zinc-300">Set up automated backups</p>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-3 p-4 border border-zinc-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Monitoring and logging</span>
                            <p class="text-sm text-zinc-300">Set up error tracking and logging</p>
                        </div>
                    </div>
                    
                    <div class="flex items-start gap-3 p-4 border border-zinc-700 rounded-lg">
                        <input type="checkbox" class="mt-1 w-5 h-5 rounded" />
                        <div>
                            <span class="font-medium text-white">Rate limiting</span>
                            <p class="text-sm text-zinc-300">Implement rate limiting to prevent abuse</p>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="summary" class="my-12 pt-8 border-t border-zinc-800/50 scroll-mt-20">
                <h2 class="text-2xl font-semibold text-white tracking-tight mb-6">
                    Summary
                </h2>
                <p class="text-zinc-300 mb-4">
                    You've learned how to:
                </p>
                <ul class="list-disc list-inside space-y-2 text-zinc-300 ml-4">
                    <li>✅ Deploy to Render with render.yaml</li>
                    <li>✅ Containerize your app with Docker</li>
                    <li>✅ Configure Vercel deployment</li>
                    <li>✅ Manage environment variables securely</li>
                    <li>✅ Serve the app via ASGI (uvicorn/gunicorn) or nextpy start</li>
                    <li>✅ Use nextpy build/export for static output</li>
                    <li>✅ Follow production best practices</li>
                </ul>
                
                <div class="my-6 p-4 border-l-4 border-green-500 bg-green-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-green-400">Ready to Deploy!</h4>
                            <div class="mt-1 text-sm text-zinc-300">
                                Your NextPy application is now ready for production. Choose the deployment platform that best fits your needs and budget.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <!-- Footer Pagination -->
            <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                <div class="w-1/2">
                    <Link href="/documentation/howto/building" class="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                        <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                        <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                            <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                            Production Building
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
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Deployment Options</a></li>
                        <li><a href="#render" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Deploy to Render</a></li>
                        <li><a href="#docker" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Deploy with Docker</a></li>
                        <li><a href="#vercel" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Deploy to Vercel</a></li>
                        <li><a href="#environment-variables" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Environment Variables</a></li>
                        <li><a href="#asgi-deployment" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">ASGI Deployment</a></li>
                        <li><a href="#build-start-export" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Build, Start &amp; Export</a></li>
                        <li><a href="#production-env" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Production Environment Variables</a></li>
                        <li><a href="#production-checklist" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Production Checklist</a></li>
                        <li><a href="#summary" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Summary</a></li>
                </ul>
            </div>
        </aside>
        </div>
        </div>
        """)


default = DeploymentGuide

