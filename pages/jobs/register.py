"""
JobHub - Register page. Interactive PSX component with server-action auth.
"""

from nextpy.psx import component, interactive_component, useState, useEffect, callServerAction, Motion


@interactive_component
def RegisterPage(props=None):
    [email, setEmail] = useState("")
    [username, setUsername] = useState("")
    [full_name, setFullName] = useState("")
    [password, setPassword] = useState("")
    [showPassword, setShowPassword] = useState(False)
    [role, setRole] = useState("job_seeker")
    [error, setError] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def handle_register(e):
        setError("")
        params = {
            "email": email,
            "username": username,
            "full_name": full_name,
            "password": password,
            "role": role,
        }
        callServerAction("register", params)

    def handle_result():
        if _server_result:
            if _server_result.get("success"):
                window.nextpyHardNavigate("/jobs/dashboard")
            else:
                setError(_server_result.get("error", "Registration failed"))

    useEffect(handle_result, [_server_result])

    input_cls = "w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-gray-900 placeholder-gray-400 transition focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-indigo-500/10"

    role_btn = "flex-1 rounded-xl border-2 px-1 py-3 text-center text-sm font-semibold transition-all active:scale-[0.98] "

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
                    <h1 class="text-3xl font-bold tracking-tight text-gray-900">Create your account</h1>
                    <p class="mt-2 text-gray-500">Join JobHub and start your journey</p>
                </div>

                <div class="rounded-2xl border border-gray-200 bg-white p-8 shadow-xl shadow-gray-900/5">
                    {if error:
                        <div class="mb-5 flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-4">
                            <span class="mt-0.5 text-red-500"></span>
                            <p class="text-sm font-medium text-red-700" data-state-error></p>
                        </div>
                    }

                    <form onsubmit={handle_register} class="space-y-5">
                        <div>
                            <label class="mb-1.5 block text-sm font-semibold text-gray-700">I am a...</label>
                            <div class="flex gap-2">
                                <button type="button" onclick={lambda e: setRole("job_seeker")}
                                    class={"flex-1 rounded-xl border-2 px-1 py-3 text-center text-sm font-semibold transition-all active:scale-[0.98] border-indigo-600 bg-indigo-50 text-indigo-700" if role == "job_seeker" else "flex-1 rounded-xl border-2 px-1 py-3 text-center text-sm font-semibold transition-all active:scale-[0.98] border-gray-200 bg-white text-gray-500 hover:border-gray-300"}>
                                    Job Seeker
                                </button>
                                <button type="button" onclick={lambda e: setRole("employer")}
                                    class={"flex-1 rounded-xl border-2 px-1 py-3 text-center text-sm font-semibold transition-all active:scale-[0.98] border-indigo-600 bg-indigo-50 text-indigo-700" if role == "employer" else "flex-1 rounded-xl border-2 px-1 py-3 text-center text-sm font-semibold transition-all active:scale-[0.98] border-gray-200 bg-white text-gray-500 hover:border-gray-300"}>
                                    Employer
                                </button>
                            </div>
                        </div>

                        <div>
                            <label class="mb-1.5 block text-sm font-semibold text-gray-700">Full name</label>
                            <input type="text" value={full_name} oninput={lambda e: setFullName(e.target.value)}
                                required placeholder="John Doe" autocomplete="name"
                                class={input_cls} />
                        </div>
                        <div>
                            <label class="mb-1.5 block text-sm font-semibold text-gray-700">Email</label>
                            <input type="email" value={email} oninput={lambda e: setEmail(e.target.value)}
                                required placeholder="you@example.com" autocomplete="email"
                                class={input_cls} />
                        </div>
                        <div>
                            <label class="mb-1.5 block text-sm font-semibold text-gray-700">Username</label>
                            <input type="text" value={username} oninput={lambda e: setUsername(e.target.value)}
                                required placeholder="johndoe" autocomplete="username"
                                class={input_cls} />
                        </div>
                        <div>
                            <label class="mb-1.5 block text-sm font-semibold text-gray-700">Password</label>
                            <div class="relative">
                                <input type={"text" if showPassword else "password"} value={password}
                                    oninput={lambda e: setPassword(e.target.value)}
                                    required minlength="6" placeholder="At least 6 characters" autocomplete="new-password"
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
                            <span>{"Creating account..." if _server_loading else "Create account"}</span>
                        </button>
                    </form>

                    <p class="mt-6 text-center text-sm text-gray-500">
                        Already have an account?{" "}
                        <a href="/jobs/login" class="font-semibold text-indigo-600 transition hover:text-indigo-500">Log in</a>
                    </p>
                </div>
            </Motion>
        </div>
    )


default = RegisterPage
