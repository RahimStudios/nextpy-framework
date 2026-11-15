"""Authentication API - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def AuthApiReference():
    overview_example = '''from nextpy import (
    AuthManager, require_auth, require_user, require_role,
    create_session, get_auth_session, delete_session,
    hash_password, verify_password,
    set_session_cookie, get_user_id_from_request, clear_session_cookie,
    get_user_from_request, current_user_id,
)
from nextpy.server_actions import get_current_user

# All of the above live in nextpy.auth; get_auth_session is the
# top-level alias of auth.get_session (avoids clashing with
# nextpy.db.get_session).'''

    passwords_example = '''from nextpy import hash_password, verify_password

# PBKDF2-HMAC-SHA256, 260k iterations, format "salt$hash"
stored = hash_password("s3cret!")

verify_password("s3cret!", stored)   # True
verify_password("wrong", stored)     # False
verify_password("x", "garbage")      # False (never raises)'''

    jwt_example = '''from nextpy import AuthManager

# Create a JWT (default expiry: settings.jwt_expiration_hours, 24h)
token = AuthManager.create_token(user_id=42)
token = AuthManager.create_token(42, expires_in=3600)          # seconds
token = AuthManager.create_token(42, expires_delta=timedelta(hours=2))

# Verify -> user_id int; raises HTTPException 401 on bad/expired token
uid = AuthManager.verify_token(token)

# Pull a Bearer token out of a request
token = AuthManager.get_token_from_request(request)  # "Bearer x" -> "x"'''

    sessions_example = '''from nextpy import create_session, get_auth_session, delete_session

# Sessions persist in the UserSession DB table (survive restarts,
# shared across workers); each lives 24 hours.
session_id = create_session(user_id=42)
sess = get_auth_session(session_id)
# {'user_id': 42, 'created_at': ..., 'expires_at': ...} or None

delete_session(session_id)  # True if a row was removed'''

    cookies_example = '''from fastapi import Request, Response
from nextpy import (
    set_session_cookie, get_user_id_from_request, clear_session_cookie,
)

# Login handler: create session + set HttpOnly cookie
session_id = set_session_cookie(response, user_id=user.id, secure=True)

# Any request: resolve user id from the "nextpy_session" cookie
uid = get_user_id_from_request(request)   # int or None

# Logout: delete DB row + expire the cookie
clear_session_cookie(response, session_id, secure=True)'''

    decorators_example = '''from nextpy import require_auth, require_user, require_role
from fastapi import Request

# 1. Bearer-token only (JWT); sets request.state.user_id
@require_auth
async def api_handler(request: Request):
    return {"user_id": request.state.user_id}

# 2. Cookie OR Bearer; loads the User ORM row; sets
#    request.state.user and request.state.user_id. 401 if anonymous.
#    Works on sync and async functions.
@require_user
async def dashboard(request: Request):
    return {"email": request.state.user.email}

# 3. Like require_user, plus role check on user.role -> 403 on mismatch
@require_role("admin", "moderator")
async def admin_panel(request: Request):
    ...'''

    helpers_example = '''from nextpy import get_user_from_request, current_user_id
from nextpy.server_actions import get_current_user

# Imperative resolution inside a handler (no decorator)
user = get_user_from_request(request)          # User ORM instance or None
uid  = current_user_id(request)                # int or None (cookie, then Bearer)

# Server-action helper: returns a plain dict or None
me = await get_current_user(request)
# {'id': ..., 'email': ..., 'username': ..., 'role': ...}'''

    config_example = '''# .env
JWT_SECRET=super-long-random-string
JWT_EXPIRATION_HOURS=24
SESSION_SECRET=another-random-string
MAIL_USERNAME=you@gmail.com
MAIL_PASSWORD=app-password'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>API Reference</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Authentication API</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Authentication API</h1>
                    <p class="leading-relaxed text-zinc-300">
                        JWT tokens, database-backed sessions, HttpOnly session cookies, password hashing, and auth decorators shipped in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.auth</code>. Everything below is re-exported from the top-level <code class="font-mono text-xs">nextpy</code> package, except <code class="font-mono text-xs">get_current_user</code> which lives in <code class="font-mono text-xs">nextpy.server_actions</code>. For the end-to-end login/signup walkthrough see the <Link href="/documentation/howto/auth" className="text-blue-400 hover:text-blue-300 underline underline-offset-4">Authentication how-to</Link>.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview: two auth mechanisms</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy supports <strong class="text-white">two complementary credentials</strong>:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><strong class="text-white">JWT Bearer tokens</strong> &mdash; stateless, signed with <code class="font-mono text-xs">jwt_secret</code> via <code class="font-mono text-xs">AuthManager</code>. Sent as <code class="font-mono text-xs">Authorization: Bearer &lt;token&gt;</code>. Good for API clients and mobile apps.</li>
                        <li><strong class="text-white">Database sessions + cookie</strong> &mdash; <code class="font-mono text-xs">create_session()</code> writes a row to the <code class="font-mono text-xs">UserSession</code> table; <code class="font-mono text-xs">set_session_cookie()</code> stores the session id in an HttpOnly <code class="font-mono text-xs">nextpy_session</code> cookie. Survives restarts and is shared across workers. This is what <code class="font-mono text-xs">require_user</code>/<code class="font-mono text-xs">require_role</code> resolve first.</li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-300">
                        Most helpers accept <em>either</em>: they check the session cookie first, then fall back to the Bearer token. <code class="font-mono text-xs">require_auth</code> is the exception &mdash; it only accepts Bearer tokens.
                    </p>
                </div>

                <div id="passwords" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Password hashing</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">hash_password(password: str) -&gt; str</code> &mdash; PBKDF2-HMAC-SHA256 with 260,000 iterations and a 16-byte random salt; returns <code class="font-mono text-xs">salt$hash</code>.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">verify_password(password: str, hashed: str) -&gt; bool</code> &mdash; constant-time comparison via <code class="font-mono text-xs">secrets.compare_digest</code>; returns <code class="font-mono text-xs">False</code> on malformed input instead of raising.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/auth/signup.py" snippet={passwords_example} />
                </div>

                <div id="jwt" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">AuthManager (JWT)</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">AuthManager</code> is a static-method class wrapping PyJWT. Tokens carry a <code class="font-mono text-xs">user_id</code> claim and an <code class="font-mono text-xs">exp</code> claim.
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Method</th>
                                    <th class="text-left px-4 py-3 font-semibold">Signature</th>
                                    <th class="text-left px-4 py-3 font-semibold">Behavior</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">create_token</td><td class="px-4 py-3 font-mono text-xs">(user_id, expires_delta=None, expires_in=None) -&gt; str</td><td class="px-4 py-3">Encodes a JWT. <code class="font-mono text-xs">expires_in</code> is seconds; <code class="font-mono text-xs">expires_delta</code> a timedelta. Default expiry is <code class="font-mono text-xs">jwt_expiration_hours</code> (24h).</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">verify_token</td><td class="px-4 py-3 font-mono text-xs">(token) -&gt; Optional[int]</td><td class="px-4 py-3">Decodes and returns <code class="font-mono text-xs">user_id</code>. Raises <code class="font-mono text-xs">HTTPException(401)</code> with &quot;Token expired&quot; or &quot;Invalid token&quot;.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">get_token_from_request</td><td class="px-4 py-3 font-mono text-xs">(request) -&gt; Optional[str]</td><td class="px-4 py-3">Extracts the token from an <code class="font-mono text-xs">Authorization: Bearer</code> header; returns <code class="font-mono text-xs">None</code> otherwise.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/api/secure.py" snippet={jwt_example} />
                </div>

                <div id="sessions" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Sessions</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">create_session(user_id: int) -&gt; str</code> &mdash; inserts a <code class="font-mono text-xs">UserSession</code> row (UUID id, 24-hour expiry) and opportunistically deletes expired rows. Returns the session id.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_auth_session(session_id: str) -&gt; Optional[Dict]</code> &mdash; looks up a session; returns <code class="font-mono text-xs">{'user_id', 'created_at', 'expires_at'}</code> or <code class="font-mono text-xs">None</code> when missing/expired (expired rows are deleted). <strong>Top-level alias</strong> of <code class="font-mono text-xs">auth.get_session</code> &mdash; use this name to avoid colliding with <code class="font-mono text-xs">nextpy.db.get_session</code>.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">delete_session(session_id: str) -&gt; bool</code> &mdash; removes the row; returns whether anything was deleted.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/auth/login.py" snippet={sessions_example} />
                </div>

                <div id="cookies" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Session cookies</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The cookie name is <code class="font-mono text-xs">nextpy_session</code> with <code class="font-mono text-xs">max_age=86400</code> (24h), <code class="font-mono text-xs">path=/</code>, <code class="font-mono text-xs">httponly=True</code>, <code class="font-mono text-xs">samesite=&quot;lax&quot;</code>, and <code class="font-mono text-xs">secure</code> configurable. There is <strong>no</strong> <code class="font-mono text-xs">get_session_cookie()</code> export &mdash; read the raw value via <code class="font-mono text-xs">request.cookies.get(&quot;nextpy_session&quot;)</code> if needed; prefer <code class="font-mono text-xs">get_user_id_from_request</code>.
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">set_session_cookie(response: Response, user_id: int, secure: bool = False) -&gt; str</code> &mdash; creates a DB session and sets the cookie on the response; returns the session id (keep it for logout).</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_user_id_from_request(request: Request) -&gt; Optional[int]</code> &mdash; resolves the cookie session to a user id; <code class="font-mono text-xs">None</code> when unauthenticated or expired.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">clear_session_cookie(response: Response, session_id: str, secure: bool = False) -&gt; None</code> &mdash; deletes the DB session and expires the cookie.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/auth/login.py" snippet={cookies_example} />
                </div>

                <div id="decorators" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Auth decorators</h2>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Decorator</th>
                                    <th class="text-left px-4 py-3 font-semibold">Accepts</th>
                                    <th class="text-left px-4 py-3 font-semibold">Sets on request.state</th>
                                    <th class="text-left px-4 py-3 font-semibold">Failure</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">require_auth</td><td class="px-4 py-3">Bearer JWT only</td><td class="px-4 py-3"><code class="font-mono text-xs">user_id</code></td><td class="px-4 py-3">401 &quot;Missing token&quot; / verify_token&rsquo;s 401s</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">require_user</td><td class="px-4 py-3">Cookie session or Bearer JWT</td><td class="px-4 py-3"><code class="font-mono text-xs">user</code> (ORM), <code class="font-mono text-xs">user_id</code></td><td class="px-4 py-3">401 &quot;Authentication required&quot;</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">require_role(*roles)</td><td class="px-4 py-3">Same as require_user, plus <code class="font-mono text-xs">user.role</code> in roles</td><td class="px-4 py-3"><code class="font-mono text-xs">user</code>, <code class="font-mono text-xs">user_id</code></td><td class="px-4 py-3">401 anonymous; 403 &quot;Insufficient permissions&quot;</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">require_user</code> and <code class="font-mono text-xs">require_role</code> preserve sync/async: they detect coroutine functions and wrap accordingly. Decorate functions whose first parameter is the FastAPI <code class="font-mono text-xs">Request</code>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/admin.py" snippet={decorators_example} />
                </div>

                <div id="helpers" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Imperative helpers</h2>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_user_from_request(request: Request, db=None)</code> &mdash; returns the ORM <code class="font-mono text-xs">User</code> or <code class="font-mono text-xs">None</code>. Checks the session cookie first, then the Bearer token. Opens and closes its own DB session unless you pass <code class="font-mono text-xs">db</code>.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">current_user_id(request: Request) -&gt; Optional[int]</code> &mdash; same resolution order as above but returns just the id.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_current_user(request)</code> (in <code class="font-mono text-xs">nextpy.server_actions</code>) &mdash; async server action returning a JSON-safe dict <code class="font-mono text-xs">{'id', 'email', 'username', 'role'}</code> or <code class="font-mono text-xs">None</code>; never raises.</li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">When to use what:</strong> use <code class="font-mono text-xs">require_user</code>/<code class="font-mono text-xs">require_role</code> to guard endpoints; use <code class="font-mono text-xs">require_auth</code> for pure-JWT APIs; use <code class="font-mono text-xs">get_user_from_request</code>/<code class="font-mono text-xs">current_user_id</code> inside handlers that need optional auth; use <code class="font-mono text-xs">get_current_user</code> from server actions that should return <code class="font-mono text-xs">None</code> rather than a 401.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/me.py" snippet={helpers_example} />
                </div>

                <div id="configuration" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Configuration</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Settings are read from <code class="font-mono text-xs">nextpy.config.settings</code>, which is populated from environment variables (or <code class="font-mono text-xs">.env</code>):
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Env var</th>
                                    <th class="text-left px-4 py-3 font-semibold">Setting key</th>
                                    <th class="text-left px-4 py-3 font-semibold">Default</th>
                                    <th class="text-left px-4 py-3 font-semibold">Used by</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">JWT_SECRET</td><td class="px-4 py-3 font-mono text-xs">jwt_secret</td><td class="px-4 py-3">&quot;change-me&quot;</td><td class="px-4 py-3">AuthManager.create_token / verify_token</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">JWT_EXPIRATION_HOURS</td><td class="px-4 py-3 font-mono text-xs">jwt_expiration_hours</td><td class="px-4 py-3">24</td><td class="px-4 py-3">AuthManager.create_token default expiry</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">(fixed)</td><td class="px-4 py-3 font-mono text-xs">jwt_algorithm</td><td class="px-4 py-3">&quot;HS256&quot;</td><td class="px-4 py-3">encode/decode algorithm</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">SESSION_SECRET</td><td class="px-4 py-3 font-mono text-xs">session_secret</td><td class="px-4 py-3">&quot;change-me&quot;</td><td class="px-4 py-3">Defined in config; session cookies themselves are opaque UUIDs stored server-side</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="text-base leading-7 text-zinc-300">
                        <strong class="text-white">Security note:</strong> always set <code class="font-mono text-xs">JWT_SECRET</code> in production &mdash; the default <code class="font-mono text-xs">change-me</code> lets anyone forge tokens. Session cookies are HttpOnly and the session id is a random UUID, so <code class="font-mono text-xs">SESSION_SECRET</code> is not currently used to sign them.
                    </p>
                    <EnhancedCodeBlock lang="bash" filename=".env" snippet={config_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/platform-utils" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Platform Utilities
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/state-sync-api" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                State Sync API
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
                        <li><a href="#passwords" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Password hashing</a></li>
                        <li><a href="#jwt" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">AuthManager (JWT)</a></li>
                        <li><a href="#sessions" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Sessions</a></li>
                        <li><a href="#cookies" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Session cookies</a></li>
                        <li><a href="#decorators" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Auth decorators</a></li>
                        <li><a href="#helpers" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Imperative helpers</a></li>
                        <li><a href="#configuration" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Configuration</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Authentication API - NextPy Docs"}}


default = AuthApiReference
