"""
JobHub - Login page. Uses interactive_component with callServerAction.
"""

from nextpy.psx import component, interactive_component, useState, callServerAction


@interactive_component
def LoginPage(props=None):
    [email, setEmail] = useState("")
    [password, setPassword] = useState("")
    [error, setError] = useState("")
    [loading, setLoading] = useState(False)
    [_server_result, _setServerResult] = useState(None)

    def handle_login(e):
        setLoading(True)
        setError("")
        callServerAction("login", {"email": email, "password": password})
        if _server_result and _server_result.get("success"):
            window.nextpyHardNavigate("/jobs/dashboard")
        else:
            if _server_result:
                setError(_server_result.get("error", "Login failed"))
            else:
                setError("Login failed")
            setLoading(False)

    return (
        <div class="max-w-md mx-auto">
            <div class="mb-8 text-center">
                <h1 class="text-3xl font-bold text-gray-900">Welcome back</h1>
                <p class="mt-2 text-gray-600">Log in to your JobHub account</p>
            </div>
            <div class="p-8 bg-white border border-gray-200 shadow-sm rounded-xl">
                <div data-state-error data-state-toggle style="display: none" class="p-3 mb-4 text-sm text-red-700 rounded-lg bg-red-50"></div>
                <form onsubmit={handle_login} class="space-y-5">
                    <div>
                        <label class="block mb-1 text-sm font-medium text-gray-700">Email</label>
                        <input type="email" value={email} oninput={lambda e: setEmail(e.target.value)}
                            required placeholder="you@example.com"
                            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                    </div>
                    <div>
                        <label class="block mb-1 text-sm font-medium text-gray-700">Password</label>
                        <input type="password" value={password} oninput={lambda e: setPassword(e.target.value)}
                            required placeholder="Your password"
                            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                    </div>
                    <button type="submit"
                        class="w-full rounded-lg bg-indigo-600 px-4 py-2.5 font-semibold text-white hover:bg-indigo-700 disabled:opacity-50">
                        <p>login</p>
                    </button>
                </form>
                <p class="mt-6 text-sm text-center text-gray-600">
                    Don't have an account?{" "}
                    <a href="/jobs/register" class="font-medium text-indigo-600 hover:text-indigo-500">Sign up</a>
                </p>
            </div>
        </div>
    )


default = LoginPage
