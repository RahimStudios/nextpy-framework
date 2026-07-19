from nextpy.psx import psx, component, register_component


@component
def AuthenticationGuide(props):
    return psx("""
        <section id="authentication" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">Authentication</h2>
                <p class="mt-2 text-gray-400">
                    Implement secure authentication in your NextPy applications with built-in support and best practices.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-rose-400">Authentication Overview</h3>
                <p class="mt-2 text-sm text-rose-300">
                    NextPy provides flexible authentication options including session-based auth, JWT tokens, OAuth integration, and support for popular authentication providers.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Session-based Auth</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.auth import SessionAuth

# Initialize auth
auth = SessionAuth(secret_key="your-secret")

# Protect a route
@auth.require_login
async def dashboard(request):
    user = auth.get_user(request)
    return {"user": user}

# Login endpoint
async def login(request, params):
    data = await request.json()
    user = auth.authenticate(data["email"], data["password"])
    if user:
        auth.login(request, user)
        return {"success": True}
    return {"success": False}</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">JWT Authentication</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.auth import JWTAuth

# Initialize JWT auth
auth = JWTAuth(
    secret_key="your-secret",
    algorithm="HS256"
)

# Generate token
token = auth.create_token(user_id=123)

# Verify token
user = auth.verify_token(token)</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">OAuth Integration</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.auth import OAuthProvider

oauth = OAuthProvider(
    client_id="your-client-id",
    client_secret="your-secret",
    redirect_uri="http://localhost:8000/auth/callback"
)

# Redirect to OAuth provider
async def login_with_google(request):
    return oauth.redirect("google")

# Handle callback
async def auth_callback(request):
    user = await oauth.authenticate("google", request)
    auth.login(request, user)
    return redirect("/dashboard")</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Protected Components</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import component
from nextpy.auth import require_auth

@component
@require_auth
def ProtectedPage(props):
    user = props.get("user")
    return (
        <div>
            <h1>Welcome, {user["name"]}</h1>
            <p>This is a protected page</p>
        </div>
    )</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Security Best Practices</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li>Always use HTTPS in production</li>
                    <li>Store secrets in environment variables</li>
                    <li>Use strong, random secret keys</li>
                    <li>Implement rate limiting on auth endpoints</li>
                    <li>Hash passwords with bcrypt or argon2</li>
                    <li>Set secure cookie flags (HttpOnly, Secure, SameSite)</li>
                    <li>Implement CSRF protection for forms</li>
                </ul>
            </div>
        </section>
    """)
