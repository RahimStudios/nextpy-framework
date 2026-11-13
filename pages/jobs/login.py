"""
JobHub - Login page. Interactive PSX component with server-action auth.
"""

from nextpy.psx import component, interactive_component, useState, useEffect, callServerAction, Motion


@interactive_component
def LoginPage(props=None):
    [email, setEmail] = useState("")
    [password, setPassword] = useState("")
    [showPassword, setShowPassword] = useState(False)
    [error, setError] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def handle_login(e):
        setError("")
        callServerAction("login", {"email": email, "password": password})

    def handle_result():
        if _server_result:
            if _server_result.get("success"):
                window.nextpyHardNavigate("/jobs/dashboard")
            else:
                setError(_server_result.get("error", "Login failed"))

    useEffect(handle_result, [_server_result])

    input_cls = "w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-gray-900 placeholder-gray-400 transition focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-indigo-500/10"

    return (
        <div class="flex min-h-[70vh] items-center justify-center px-4 py-12">
            <Motion
                initial={{"opacity": 0, "transform": "translateY(24px)"}}
                animate={{"opacity": 1, "transform": "translateY(0px)"}}
                transition={{"duration": 0.5, "easing": "ease-out"}}
                className="w-full max-w-md"
            >
                <div class="mb-8 text-center">
                    <div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-600 to-violet-600 text-2xl font-bold text-white shadow-lg shadow-indigo-600/30">
                        J
                    </div>
                    <h1 class="text-3xl font-bold tracking-tight text-gray-900">Welcome back</h1>
                    <p class="mt-2 text-gray-500">Log in to your JobHub account</p>
                </div>

                <div class="rounded-2xl border border-gray-200 bg-white p-8 shadow-xl shadow-gray-900/5">
                    <div data-state-error data-state-toggle style="display: none" class="mb-5 p-3 text-sm text-red-700 rounded-lg bg-red-50"></div>

                    <form onsubmit={handle_login} class="space-y-5">
                        <div>
                            <label class="mb-1.5 block text-sm font-semibold text-gray-700">Email</label>
                            <input type="email" value={email} oninput={lambda e: setEmail(e.target.value)}
                                required placeholder="you@example.com" autocomplete="email"
                                class={input_cls} />
                        </div>
                        <div>
                            <label class="mb-1.5 block text-sm font-semibold text-gray-700">Password</label>
                            <div class="relative">
                                <input type={"text" if showPassword else "password"} value={password}
                                    oninput={lambda e: setPassword(e.target.value)}
                                    required placeholder="Your password" autocomplete="current-password"
                                    class={input_cls + " pr-12"} />
                                <button type="button" onclick={lambda e: setShowPassword(not showPassword)}
                                    class="absolute right-3 top-1/2 -translate-y-1/2 text-sm font-medium text-gray-400 transition hover:text-indigo-600">
                                    {"Hide" if showPassword else "Show"}
                                </button>
                            </div>
                        </div>
                        <button type="submit" disabled={_server_loading}
                            class="group flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 px-4 py-3.5 font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all hover:shadow-xl hover:shadow-indigo-600/30 hover:brightness-110 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60 disabled:active:scale-100">
                            {if _server_loading:
                                <span class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white"></span>
                            }
                            <span>{"Signing in..." if _server_loading else "Sign in"}</span>
                        </button>
                    </form>

                    <p class="mt-6 text-center text-sm text-gray-500">
                        Don't have an account?{" "}
                        <a href="/jobs/register" class="font-semibold text-indigo-600 transition hover:text-indigo-500">Sign up free</a>
                    </p>
                </div>
            </Motion>
        </div>
    )


default = LoginPage
