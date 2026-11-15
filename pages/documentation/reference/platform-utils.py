"""Platform Utilities - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def PlatformUtilsReference():
    overview_example = '''from nextpy.utils.email import send_email
from nextpy.utils.search import simple_search
from nextpy.utils.validators import validate_slug

# The nextpy.utils subpackage is NOT re-exported at the top level —
# always import from the concrete module.
await send_email(["team@example.com"], "Hello", "<p>Hi</p>")
results = simple_search("next", posts, ["title", "body"])
validate_slug("my-first-post")  # True'''

    email_example = '''from nextpy.utils.email import (
    send_email, send_welcome_email, send_reset_password_email,
)

# Generic send — returns True on success, False on failure
ok = await send_email(
    to=["user@example.com", "admin@example.com"],
    subject="Your invoice",
    html_content="<h1>Invoice</h1><p>Total: $42</p>",
    text_content="Invoice - Total: $42",
)

# Ready-made templates
await send_welcome_email("new@example.com", "Ada")
await send_reset_password_email("user@example.com", "https://app.example.com/reset?token=abc")'''

    file_upload_example = '''from fastapi import UploadFile
from nextpy.utils.file_upload import upload_file, delete_file, get_upload_url

async def save_avatar(file: UploadFile):
    path = await upload_file(file, directory="avatars")
    url = get_upload_url(path)          # /uploads/avatars/avatar.png
    return {"path": path, "url": url}

async def remove_avatar(path: str):
    return await delete_file(path)'''

    logging_example = '''from nextpy.utils.logging import get_logger

log = get_logger("myapp.orders")

log.info("order created", order_id=42, total=19.99)
log.warning("low stock", sku="A-100", remaining=2)
log.error("payment failed", order_id=42, reason="card_declined")
log.debug("cache hit", key="profile:42")'''

    search_example = '''from nextpy.utils.search import simple_search, fuzzy_search, search_highlight

posts = [
    {"title": "Getting Started", "body": "Install nextpy and run rx run"},
    {"title": "Advanced State", "body": "Learn about useState"},
]

# Case-insensitive substring match across multiple fields
hits = simple_search("nextpy", posts, ["title", "body"])

# Subsequence scoring on a single field, best matches first
close = fuzzy_search("gtting started", posts, "title")

# Wrap matches in <mark> tags for display
html = search_highlight("state", "Advanced State Guide")'''

    seo_example = '''from datetime import datetime
from nextpy.utils.seo import (
    create_article_schema, create_organization_schema,
    generate_sitemap, generate_robots_txt,
)
import json

article = create_article_schema(
    title="Hello NextPy",
    description="A quick tour",
    image="https://example.com/cover.png",
    author="Ada",
    date_published=datetime(2024, 5, 1),
    url="https://example.com/blog/hello",
)

org = create_organization_schema(
    name="Acme", url="https://example.com",
    logo="https://example.com/logo.png",
    contact_url="https://example.com/contact",
)

sitemap = generate_sitemap([
    {"url": "https://example.com/", "priority": "1.0"},
    {"url": "https://example.com/blog", "lastmod": "2024-05-01"},
])
robots = generate_robots_txt("https://example.com/sitemap.xml")
json.dumps(article)'''

    validators_example = '''from nextpy.utils.validators import (
    ContactForm, BlogPost, User, LoginForm, SignupForm, validate_slug,
)
from pydantic import ValidationError

post = BlogPost(
    title="My Post",
    slug="my-post",
    content="...",
    author="Ada",
    tags=["news"],
    published=True,
)

try:
    form = LoginForm(email="not-an-email", password="x")
except ValidationError as e:
    print(e)

validate_slug("hello-world")   # True
validate_slug("Hello_World")   # False'''

    cache_example = '''from nextpy.utils.cache import get_cache, cache_result

cache = get_cache()
cache.set("config:site", {"name": "Acme"}, ttl=300)
value = cache.get("config:site")

@cache_result(ttl=60)
async def expensive_report():
    return await compute_report()

# NOTE: this is a DIFFERENT cache from nextpy.cache.MemoryCache!
from nextpy.cache import get_cache as get_memory_cache
memory = get_memory_cache()   # shared, thread-safe, maxsize=2048'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>API Reference</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Platform Utilities</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Platform Utilities</h1>
                    <p class="leading-relaxed text-zinc-300">
                        A collection of small, dependency-light helpers shipped in the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.utils</code> subpackage: SMTP email, file uploads, structured logging, in-memory search, SEO helpers, Pydantic validators, and a simple TTL cache. These modules are <strong class="text-white">not re-exported at the top level</strong> of <code class="font-mono text-xs">nextpy</code> &mdash; import from the concrete module, e.g. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">from nextpy.utils.email import send_email</code>.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The subpackage is organized one module per concern. Everything here is server-side Python &mdash; none of it renders to the client. For request authentication see the <Link href="/documentation/reference/auth-api" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">Authentication API</Link>; for the production-grade cache see <Link href="/documentation/reference/caching" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">In-Memory Cache (MemoryCache)</Link>.
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Module</th>
                                    <th class="text-left px-4 py-3 font-semibold">Contents</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy.utils.email</td><td class="px-4 py-3">SMTP send helpers: <code class="font-mono text-xs">send_email</code>, <code class="font-mono text-xs">send_welcome_email</code>, <code class="font-mono text-xs">send_reset_password_email</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy.utils.file_upload</td><td class="px-4 py-3">Upload validation and disk storage: <code class="font-mono text-xs">upload_file</code>, <code class="font-mono text-xs">delete_file</code>, <code class="font-mono text-xs">get_upload_url</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy.utils.logging</td><td class="px-4 py-3">Thin wrapper over stdlib <code class="font-mono text-xs">logging</code>: <code class="font-mono text-xs">Logger</code>, <code class="font-mono text-xs">get_logger</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy.utils.search</td><td class="px-4 py-3">In-memory text search: <code class="font-mono text-xs">simple_search</code>, <code class="font-mono text-xs">fuzzy_search</code>, <code class="font-mono text-xs">search_highlight</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy.utils.seo</td><td class="px-4 py-3">JSON-LD schema and sitemap/robots generators.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy.utils.validators</td><td class="px-4 py-3">Pydantic models for common forms plus <code class="font-mono text-xs">validate_slug</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">nextpy.utils.cache</td><td class="px-4 py-3">Minimal TTL cache: <code class="font-mono text-xs">Cache</code>, <code class="font-mono text-xs">get_cache</code>, <code class="font-mono text-xs">cache_result</code>.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={overview_example} />
                </div>

                <div id="email" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Email (nextpy.utils.email)</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        All three functions are <code class="font-mono text-xs">async</code> and send through <code class="font-mono text-xs">smtplib.SMTP</code> with STARTTLS. Configuration comes from <code class="font-mono text-xs">nextpy.config.settings</code>, populated by environment variables:
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Env var</th>
                                    <th class="text-left px-4 py-3 font-semibold">Setting key</th>
                                    <th class="text-left px-4 py-3 font-semibold">Default</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">MAIL_SERVER</td><td class="px-4 py-3 font-mono text-xs">mail_server</td><td class="px-4 py-3">smtp.gmail.com</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">MAIL_PORT</td><td class="px-4 py-3 font-mono text-xs">mail_port</td><td class="px-4 py-3">587</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">MAIL_USERNAME</td><td class="px-4 py-3 font-mono text-xs">mail_username</td><td class="px-4 py-3">(empty)</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">MAIL_PASSWORD</td><td class="px-4 py-3 font-mono text-xs">mail_password</td><td class="px-4 py-3">(empty)</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">async send_email(to: List[str], subject: str, html_content: str, text_content: Optional[str] = None) -&gt; bool</code> &mdash; builds a <code class="font-mono text-xs">multipart/alternative</code> message (plain-text part only when <code class="font-mono text-xs">text_content</code> is given) and sends it. Returns <code class="font-mono text-xs">True</code> on success; on any exception it prints the error and returns <code class="font-mono text-xs">False</code>, so always check the return value.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">async send_welcome_email(email: str, name: str) -&gt; bool</code> &mdash; convenience wrapper sending a fixed welcome template (&quot;Welcome to NextPy&quot;).</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">async send_reset_password_email(email: str, reset_link: str) -&gt; bool</code> &mdash; sends a password-reset template containing the supplied link.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/auth/signup.py" snippet={email_example} />
                </div>

                <div id="file-upload" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">File uploads (nextpy.utils.file_upload)</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Files are written under an <code class="font-mono text-xs">uploads/</code> directory relative to the working directory, optionally nested by a <code class="font-mono text-xs">directory</code> argument. Allowed extensions are <code class="font-mono text-xs">.jpg .jpeg .png .gif .pdf .txt .doc .docx</code> and the default size cap is 10&nbsp;MB.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">async upload_file(file: UploadFile, directory: str = &quot;general&quot;, max_size: int = MAX_FILE_SIZE) -&gt; Optional[str]</code> &mdash; validates the extension (raising <code class="font-mono text-xs">ValueError</code> for disallowed types), creates the directory, and streams the upload to disk. Returns the saved path as a string, or raises <code class="font-mono text-xs">ValueError</code> if the file exceeds <code class="font-mono text-xs">max_size</code> bytes. On failure a partially written file is deleted.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">async delete_file(file_path: str) -&gt; bool</code> &mdash; removes a previously uploaded file; returns <code class="font-mono text-xs">True</code> when it existed, <code class="font-mono text-xs">False</code> otherwise or on error.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_upload_url(file_path: str) -&gt; str</code> &mdash; synchronous helper returning the public path <code class="font-mono text-xs">/uploads/&#123;file_path&#125;</code>.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/api/upload.py" snippet={file_upload_example} />
                </div>

                <div id="logging" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Logging (nextpy.utils.logging)</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_logger(name: str) -&gt; Logger</code> &mdash; returns a <code class="font-mono text-xs">Logger</code> wrapping <code class="font-mono text-xs">logging.getLogger(name)</code>. On first use it attaches a <code class="font-mono text-xs">StreamHandler</code> with the format <code class="font-mono text-xs">%(asctime)s - %(name)s - %(levelname)s - %(message)s</code> and level <code class="font-mono text-xs">INFO</code>.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Logger.info / .error / .debug / .warning(message: str, **kwargs)</code> &mdash; log at the matching level; extra keyword arguments are appended as <code class="font-mono text-xs">key=value</code> pairs separated by <code class="font-mono text-xs">|</code>.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={logging_example} />
                </div>

                <div id="search" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Search (nextpy.utils.search)</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Pure-Python helpers for searching lists of dicts in memory. Suitable for small datasets; for larger corpora use a real search backend.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">simple_search(query: str, items: List[Dict], fields: List[str]) -&gt; List[Dict]</code> &mdash; case-insensitive substring match; an item is returned once if the query appears in any of the named fields. Missing fields are skipped.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">fuzzy_search(query: str, items: List[Dict], field: str) -&gt; List[Dict]</code> &mdash; subsequence match on a single field scored by character proximity; returns only items with score &gt; 0, sorted best-first. Not a true edit-distance fuzzy match.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">search_highlight(query: str, text: str) -&gt; str</code> &mdash; returns <code class="font-mono text-xs">text</code> with every case-insensitive occurrence of <code class="font-mono text-xs">query</code> wrapped in <code class="font-mono text-xs">&lt;mark&gt;</code> tags (HTML-escaped query via <code class="font-mono text-xs">re.escape</code>).</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/blog/index.py" snippet={search_example} />
                </div>

                <div id="seo" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">SEO (nextpy.utils.seo)</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">create_article_schema(title, description, image, author, date_published, date_modified=None, url=&quot;&quot;) -&gt; Dict</code> &mdash; returns a schema.org <code class="font-mono text-xs">Article</code> JSON-LD dict; <code class="font-mono text-xs">dateModified</code> falls back to <code class="font-mono text-xs">date_published</code>. Serialize with <code class="font-mono text-xs">json.dumps</code> and inject via <code class="font-mono text-xs">Head</code>.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">create_organization_schema(name, url, logo, contact_url=None) -&gt; Dict</code> &mdash; schema.org <code class="font-mono text-xs">Organization</code> dict; <code class="font-mono text-xs">contactPoint</code> is <code class="font-mono text-xs">None</code> when <code class="font-mono text-xs">contact_url</code> is omitted.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">generate_sitemap(routes: List[Dict]) -&gt; str</code> &mdash; builds a <code class="font-mono text-xs">urlset</code> XML document from route dicts; each route may include <code class="font-mono text-xs">url</code>, <code class="font-mono text-xs">lastmod</code>, and <code class="font-mono text-xs">priority</code> keys.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">generate_robots_txt(sitemap_url: str) -&gt; str</code> &mdash; returns a robots.txt body that allows all agents, disallows <code class="font-mono text-xs">/admin/</code>, <code class="font-mono text-xs">/api/</code>, and <code class="font-mono text-xs">/_nextpy/</code>, and points at the given sitemap URL.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={seo_example} />
                </div>

                <div id="validators" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Validators (nextpy.utils.validators)</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Ready-made <code class="font-mono text-xs">pydantic.BaseModel</code> classes for common forms. Requires the <code class="font-mono text-xs">email-validator</code> extra for <code class="font-mono text-xs">EmailStr</code> and <code class="font-mono text-xs">HttpUrl</code> fields. Raise <code class="font-mono text-xs">pydantic.ValidationError</code> on bad input.
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Model</th>
                                    <th class="text-left px-4 py-3 font-semibold">Fields</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">ContactForm</td><td class="px-4 py-3"><code class="font-mono text-xs">name</code>, <code class="font-mono text-xs">email: EmailStr</code>, <code class="font-mono text-xs">message</code>, optional <code class="font-mono text-xs">subject</code></td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">BlogPost</td><td class="px-4 py-3"><code class="font-mono text-xs">title</code>, <code class="font-mono text-xs">slug</code>, <code class="font-mono text-xs">content</code>, <code class="font-mono text-xs">author</code>, optional <code class="font-mono text-xs">excerpt</code>, <code class="font-mono text-xs">featured_image: HttpUrl</code>, <code class="font-mono text-xs">tags: List[str]</code>, <code class="font-mono text-xs">published: bool</code></td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">User</td><td class="px-4 py-3"><code class="font-mono text-xs">email: EmailStr</code>, <code class="font-mono text-xs">username</code>, <code class="font-mono text-xs">full_name</code>, optional <code class="font-mono text-xs">bio</code>, <code class="font-mono text-xs">avatar_url: HttpUrl</code></td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">LoginForm</td><td class="px-4 py-3"><code class="font-mono text-xs">email: EmailStr</code>, <code class="font-mono text-xs">password</code>, <code class="font-mono text-xs">remember_me: bool = False</code></td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">SignupForm</td><td class="px-4 py-3"><code class="font-mono text-xs">email</code>, <code class="font-mono text-xs">username</code>, <code class="font-mono text-xs">password</code>, <code class="font-mono text-xs">confirm_password</code>, <code class="font-mono text-xs">agree_to_terms: bool = False</code> (note: no cross-field password match check)</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">validate_slug(slug: str) -&gt; bool</code> &mdash; returns <code class="font-mono text-xs">True</code> only for lowercase alphanumeric segments joined by single hyphens (regex <code class="font-mono text-xs">^[a-z0-9]+(?:-[a-z0-9]+)*$</code>).</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/api/posts.py" snippet={validators_example} />
                </div>

                <div id="cache" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Cache (nextpy.utils.cache)</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        A minimal dict-backed TTL cache &mdash; deliberately simpler than <code class="font-mono text-xs">nextpy.cache.MemoryCache</code>. It is <strong class="text-white">not thread-safe</strong>, has no size limit, and its global instance is a plain module-level singleton.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Cache.set(key: str, value: Any, ttl: int = 3600)</code> &mdash; stores <code class="font-mono text-xs">(value, expiry)</code> where expiry is <code class="font-mono text-xs">time.time() + ttl</code> seconds.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Cache.get(key: str) -&gt; Optional[Any]</code> &mdash; returns the value, or <code class="font-mono text-xs">None</code> when missing/expired; expired entries are deleted lazily on read.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Cache.delete(key)</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Cache.clear()</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Cache.cleanup_expired()</code> &mdash; deletion and eager expiry sweep.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_cache() -&gt; Cache</code> &mdash; returns the module-global <code class="font-mono text-xs">Cache()</code> instance. <strong>Different from</strong> <code class="font-mono text-xs">nextpy.cache.get_cache()</code>, which returns the shared thread-safe <code class="font-mono text-xs">MemoryCache</code>.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">cache_result(ttl: int = 3600)</code> &mdash; decorator caching a function&rsquo;s return value keyed on <code class="font-mono text-xs">func.__name__ + args + kwargs</code>. Handles both sync and async functions; caveat: the key uses <code class="font-mono text-xs">str(args)</code>, so unhashable/unstable reprs can collide or miss.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={cache_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/utils" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Utility Modules
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/auth-api" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Authentication API
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
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Overview</a></li>
                        <li><a href="#email" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Email</a></li>
                        <li><a href="#file-upload" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">File uploads</a></li>
                        <li><a href="#logging" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Logging</a></li>
                        <li><a href="#search" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Search</a></li>
                        <li><a href="#seo" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">SEO</a></li>
                        <li><a href="#validators" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Validators</a></li>
                        <li><a href="#cache" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Cache</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Platform Utilities - NextPy Docs"}}


default = PlatformUtilsReference
