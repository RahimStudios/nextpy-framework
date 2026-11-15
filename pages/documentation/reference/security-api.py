"""Security API (security_manager) - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def SecurityApiReference():
    overview_example = """from nextpy.security import security_manager, sanitize_input, safe_html

# HTML-escape a user-supplied string
clean = security_manager.sanitize_html(user_input)

# Sanitize nested request data before storing it
payload = sanitize_input({"name": user_name, "bio": user_bio})

# Safe markup for templates
html = safe_html(rich_content)"""

    props_example = """from nextpy.security import security_manager

props = {
    "className": "card",
    "href": "https://example.com",
    "onclick": "alert('xss')",   # stripped
    "title": '<img onerror="xss">',  # escaped
}

safe = security_manager.sanitize_jsx_props(props)
# {'className': 'card', 'href': '...', 'title': '&lt;img...&gt;'}"""

    csp_example = """from nextpy.security import security_manager

# The same header the server adds to every response automatically
csp = security_manager.create_csp_header()
print(csp)
# default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; ..."""

    upload_example = """from nextpy.security import security_manager

filename = "avatar.png"
content_type = "image/png"

if security_manager.validate_file_upload(filename, content_type):
    store_upload(filename, content_type)
else:
    raise ValueError("Unsupported file type")"""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>API Reference</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Security API</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Security API (security_manager)</h1>
                    <p class="leading-relaxed text-zinc-300">
                        XSS protection, input sanitization, URL and upload validation, and Content Security Policy helpers shipped in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.security</code>. Much of this runs automatically inside the JSX renderer and the server middleware; the functions below are for cases where you need to sanitize or validate data yourself.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The module exposes a single shared instance, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">security_manager = SecurityManager()</code>, plus three module-level convenience functions. All <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">SecurityManager</code> methods are <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@staticmethod</code>s, so they can also be called on the class itself.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={overview_example} />
                </div>

                <div id="sanitization" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">HTML &amp; JSX sanitization</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">sanitize_html(content: str) -&gt; str</code> &mdash; HTML-escapes the input and strips event-handler attributes (<code class="font-mono text-xs">on*</code>) and dangerous URL schemes (<code class="font-mono text-xs">javascript:</code>, <code class="font-mono text-xs">data:</code>, <code class="font-mono text-xs">vbscript:</code>). Returns <code class="font-mono text-xs">""</code> for falsy input. Use this for plain user text.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">sanitize_rich_html(content: str) -&gt; str</code> &mdash; conservative sanitizer that keeps harmless markup (blog bodies, CMS fields) while removing script-capable tags (<code class="font-mono text-xs">script</code>, <code class="font-mono text-xs">iframe</code>, <code class="font-mono text-xs">object</code>, <code class="font-mono text-xs">embed</code>, <code class="font-mono text-xs">svg</code>, <code class="font-mono text-xs">math</code>, form elements, etc.), <code class="font-mono text-xs">on*</code> handlers, and dangerous URL schemes in <code class="font-mono text-xs">href</code>/<code class="font-mono text-xs">src</code>/<code class="font-mono text-xs">action</code> attributes.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">sanitize_jsx_props(props: Dict[str, Any]) -&gt; Dict[str, Any]</code> &mdash; returns a new props dict with every string value run through <code class="font-mono text-xs">sanitize_html</code>, nested dicts sanitized recursively, strings inside lists escaped, and any key starting with <code class="font-mono text-xs">on</code> (case-insensitive) dropped entirely.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">sanitize_css(css: str) -&gt; str</code> &mdash; removes CSS-injection constructs: <code class="font-mono text-xs">javascript:</code>, <code class="font-mono text-xs">expression(</code>, <code class="font-mono text-xs">@import</code>, and <code class="font-mono text-xs">binding:</code>.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/components/card.py" snippet={props_example} />
                </div>

                <div id="validation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">URL, upload &amp; origin validation</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">validate_url(url: str) -&gt; bool</code> &mdash; rejects empty values and dangerous protocols (<code class="font-mono text-xs">javascript:</code>, <code class="font-mono text-xs">vbscript:</code>, <code class="font-mono text-xs">data:</code>, <code class="font-mono text-xs">file:</code>, <code class="font-mono text-xs">ftp:</code>); only allows <code class="font-mono text-xs">http://</code>, <code class="font-mono text-xs">https://</code>, and relative URLs (<code class="font-mono text-xs">/</code>, <code class="font-mono text-xs">./</code>, <code class="font-mono text-xs">../</code>). This is applied automatically to <code class="font-mono text-xs">href</code>/<code class="font-mono text-xs">src</code>/<code class="font-mono text-xs">action</code> props when JSX is rendered to HTML.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">validate_file_upload(filename: str, content_type: str) -&gt; bool</code> &mdash; rejects dangerous extensions (<code class="font-mono text-xs">.exe</code>, <code class="font-mono text-xs">.bat</code>, <code class="font-mono text-xs">.js</code>, <code class="font-mono text-xs">.php</code>, <code class="font-mono text-xs">.msi</code>, etc.) and requires a content type starting with <code class="font-mono text-xs">image/</code>, <code class="font-mono text-xs">text/</code>, or one of the allowed application types (<code class="font-mono text-xs">application/json</code>, <code class="font-mono text-xs">application/xml</code>, <code class="font-mono text-xs">application/pdf</code>, <code class="font-mono text-xs">application/msword</code>, <code class="font-mono text-xs">application/vnd*</code>).</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">is_trusted_origin(origin: Optional[str], request_host: str, allowed_origins: Optional[List[str]] = None) -&gt; bool</code> &mdash; returns <code class="font-mono text-xs">False</code> for missing or malformed origins; <code class="font-mono text-xs">True</code> when the origin netloc matches <code class="font-mono text-xs">request_host</code> or equals an entry in <code class="font-mono text-xs">allowed_origins</code> (trailing slash ignored). Used by the CSRF middleware and the <code class="font-mono text-xs">/ws</code> WebSocket handshake.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/api/upload.py" snippet={upload_example} />
                </div>

                <div id="csp" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">CSP &amp; automatic security headers</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">create_csp_header() -&gt; str</code> builds the Content Security Policy directive string: <code class="font-mono text-xs">default-src 'self'</code>, <code class="font-mono text-xs">script-src 'self' 'unsafe-inline' 'unsafe-eval'</code>, <code class="font-mono text-xs">img-src 'self' data: https:</code>, websocket <code class="font-mono text-xs">connect-src</code> for localhost dev, <code class="font-mono text-xs">object-src 'none'</code>, <code class="font-mono text-xs">frame-ancestors 'none'</code>, and <code class="font-mono text-xs">upgrade-insecure-requests</code>.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        You rarely need to call this yourself: the <code class="font-mono text-xs">add_security_headers</code> HTTP middleware in <code class="font-mono text-xs">nextpy.server.app</code> attaches the CSP header plus <code class="font-mono text-xs">X-Content-Type-Options: nosniff</code>, <code class="font-mono text-xs">X-Frame-Options: DENY</code>, <code class="font-mono text-xs">Referrer-Policy</code>, <code class="font-mono text-xs">Permissions-Policy</code>, <code class="font-mono text-xs">Cross-Origin-Opener-Policy</code>, <code class="font-mono text-xs">Cross-Origin-Resource-Policy</code>, <code class="font-mono text-xs">X-Permitted-Cross-Domain-Policies</code>, and (on HTTPS) <code class="font-mono text-xs">Strict-Transport-Security</code> to every response. The CSRF middleware separately uses <code class="font-mono text-xs">is_trusted_origin</code> to reject state-changing requests whose <code class="font-mono text-xs">Origin</code>/<code class="font-mono text-xs">Referer</code> does not match the request host or the <code class="font-mono text-xs">CSRF_TRUSTED_ORIGINS</code> env var; bearer-token requests are exempt.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/index.py" snippet={csp_example} />
                </div>

                <div id="helpers" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Module-level helpers</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">sanitize_input(data: Any) -&gt; Any</code> &mdash; recursively sanitizes strings inside dicts and lists via <code class="font-mono text-xs">security_manager.sanitize_html</code>; non-string scalars pass through unchanged.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">safe_html(content: str) -&gt; Markup</code> &mdash; sanitizes then wraps the result in <code class="font-mono text-xs">markupsafe.Markup</code> so template engines render it as safe HTML.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">validate_and_sanitize_props(props: Dict[str, Any]) -&gt; Dict[str, Any]</code> &mdash; thin wrapper around <code class="font-mono text-xs">security_manager.sanitize_jsx_props</code>.</li>
                    </ul>
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
                        <Link href="/documentation/reference/api-router" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                API Router
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
                        <li><a href="#sanitization" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">HTML &amp; JSX sanitization</a></li>
                        <li><a href="#validation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">URL, upload &amp; origin validation</a></li>
                        <li><a href="#csp" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">CSP &amp; headers</a></li>
                        <li><a href="#helpers" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Module-level helpers</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Security API - NextPy Docs"}}


default = SecurityApiReference
