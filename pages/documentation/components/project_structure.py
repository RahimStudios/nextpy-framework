from nextpy.psx import psx



def ProjectStructure():
    return psx(f"""
        <section id="project-structure" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">Project Structure</h2>
                <p class="mt-2 text-gray-400">
                    NextPy uses a clean folder layout that maps directly to routes, templates, and app logic.
                </p>
            </div>

            <div class="p-6 text-gray-100 bg-gray-950 border border-gray-700 rounded-2xl">
                <pre class="overflow-x-auto text-sm text-emerald-400">my-app/
├── pages/
│   ├── index.py              # Home page (/)
│   ├── about.py              # About page (/about)
│   ├── blog/
│   │   ├── index.py          # Blog listing (/blog)
│   │   └── [slug].py         # Blog post (/blog/hello-world)
│   └── api/
│       ├── users.py          # API endpoint (/api/users)
│       └── health.py         # Health check (/api/health)
├── templates/
│   ├── _base.html            # Base template
│   └── _layout.html          # Layout template
├── public/
│   ├── images/               # Static images
│   └── favicon.ico           # Site icon
├── styles/
│   └── custom.css            # Custom CSS
├── components/
│   ├── Button.py             # Reusable components
│   └── Card.py
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project configuration
└── .env                      # Environment variables</pre>
            </div>

            <div class="grid gap-4 md:grid-cols-2">
                <div class="p-5 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Pages</h3>
                    <p class="mt-2 text-sm text-gray-400">Every Python or PSX file under pages becomes a route automatically. Use brackets for dynamic routes like [slug].py.</p>
                </div>
                <div class="p-5 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">API Routes</h3>
                    <p class="mt-2 text-sm text-gray-400">Place API endpoints in pages/api/ to create backend endpoints. Support GET, POST, PUT, DELETE methods.</p>
                </div>
                <div class="p-5 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Templates</h3>
                    <p class="mt-2 text-sm text-gray-400">Store Jinja2 templates for server-side rendering. Use _base.html for shared layouts and _layout.html for page-specific layouts.</p>
                </div>
                <div class="p-5 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Public & Styles</h3>
                    <p class="mt-2 text-sm text-gray-400">Public folder contains static assets served at root. Styles folder holds custom CSS files imported in your components.</p>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">File Naming Conventions</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li><strong>index.py:</strong> Maps to the directory path (pages/blog/index.py → /blog)</li>
                    <li><strong>[param].py:</strong> Dynamic route parameter (pages/blog/[slug].py → /blog/anything)</li>
                    <strong>layout.psx:</strong> Layout for all pages in that directory</li>
                    <li><strong>_filename:</strong> Files starting with underscore are not routes</li>
                    <li><strong>.psx files:</strong> PSX syntax files are automatically converted to Python</li>
                </ul>
            </div>
        </section>
    """)