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
                    NextPy ships session-based auth in <code>nextpy.auth</code>: password hashing, server-side sessions, cookie helpers, and decorators that guard API routes and pages.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <div class="flex items-center justify-between">
                        <h3 class="font-semibold text-gray-100">Password Hashing</h3>
                        <span class="px-2 py-1 text-xs font-medium text-green-400 bg-green-900/30 rounded-full">Stable</span>
                    </div>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.auth import hash_password, verify_password

# Store only the hash
hashed = hash_password("user-password")

# Verify on login
ok = verify_password("user-password", hashed)</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <div class="flex items-center justify-between">
                        <h3 class="font-semibold text-gray-100">Session Cookies</h3>
                        <span class="px-2 py-1 text-xs font-medium text-green-400 bg-green-900/30 rounded-full">Stable</span>
                    </div>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.auth import (
    create_session, set_session_cookie,
    get_user_id_from_request, clear_session_cookie,
)

# After verifying credentials
session_id = create_session(user.id)
set_session_cookie(response, user.id)

# On later requests
user_id = get_user_id_from_request(request)

# On logout
clear_session_cookie(response, session_id)</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <div class="flex items-center justify-between">
                        <h3 class="font-semibold text-gray-100">Route Guards</h3>
                        <span class="px-2 py-1 text-xs font-medium text-green-400 bg-green-900/30 rounded-full">Stable</span>
                    </div>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.auth import require_auth, require_role

@require_auth
async def dashboard(request):
    user_id = get_user_id_from_request(request)
    return {"user_id": user_id}

@require_role("admin")
async def admin_panel(request):
    return {"ok": True}</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Client Login Flow</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import interactive_component, useState, useEffect, callServerAction

@interactive_component
def LoginForm():
    [email, setEmail] = useState("")
    [password, setPassword] = useState("")
    [_server_result, _set] = useState(None)

    def submit(e):
        e.preventDefault()
        callServerAction("login", {"email": email, "password": password})

    def on_result():
        if _server_result and _server_result.get("success"):
            window.navigateTo("/dashboard")

    useEffect(on_result, [_server_result])</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Security Best Practices</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li>Always use HTTPS in production</li>
                    <li>Store secrets in environment variables</li>
                    <li>Use strong, random secret keys</li>
                    <li>Implement rate limiting on auth endpoints</li>
                    <li>Hash passwords with the built-in hash_password helper</li>
                    <li>Set secure cookie flags (HttpOnly, Secure, SameSite)</li>
                    <li>Implement CSRF protection for forms</li>
                </ul>
            </div>
        </section>
    """)


default = AuthenticationGuide
