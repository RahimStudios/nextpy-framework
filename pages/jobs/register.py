"""
JobHub - Register page. Uses interactive_component with callServerAction.
"""

from nextpy.psx import component, interactive_component, useState, callServerAction


@interactive_component
def RegisterPage(props=None):
    [email, setEmail] = useState("")
    [username, setUsername] = useState("")
    [full_name, setFullName] = useState("")
    [password, setPassword] = useState("")
    [role, setRole] = useState("job_seeker")
    [error, setError] = useState("")
    [loading, setLoading] = useState(False)
    [_server_result, _setServerResult] = useState(None)

    def handle_register(e):
        setLoading(True)
        setError("")
        params = {
            "email": email,
            "username": username,
            "full_name": full_name,
            "password": password,
            "role": role,
        }
        callServerAction("register", params)
        if _server_result and _server_result.get("success"):
            window.nextpyHardNavigate("/jobs/dashboard")
        else:
            if _server_result:
                setError(_server_result.get("error", "Registration failed"))
            else:
                setError("Registration failed")
            setLoading(False)

    return (
        <div class="max-w-md mx-auto">
            <div class="mb-8 text-center">
                <h1 class="text-3xl font-bold text-gray-900">Create your account</h1>
                <p class="mt-2 text-gray-600">Join JobHub and start your journey</p>
            </div>
            <div class="p-8 bg-white border border-gray-200 shadow-sm rounded-xl">
                <div data-state-error data-state-toggle style="display: none" class="p-3 mb-4 text-sm text-red-700 rounded-lg bg-red-50"></div>
                <form onsubmit={handle_register} class="space-y-5">
                    <div>
                        <label class="block mb-2 text-sm font-medium text-gray-700">I am a...</label>
                        <div class="grid grid-cols-2 gap-2">
                            {if role == "job_seeker":
                                <button type="button" onclick={lambda e: setRole("job_seeker")}
                                    class="rounded-lg border-2 border-indigo-600 bg-indigo-50 px-4 py-2.5 text-center text-sm font-medium text-indigo-700">
                                    Job Seeker
                                </button>
                            }
                            {if role != "job_seeker":
                                <button type="button" onclick={lambda e: setRole("job_seeker")}
                                    class="rounded-lg border-2 border-gray-200 bg-white px-4 py-2.5 text-center text-sm font-medium text-gray-600">
                                    Job Seeker
                                </button>
                            }
                            {if role == "employer":
                                <button type="button" onclick={lambda e: setRole("employer")}
                                    class="rounded-lg border-2 border-indigo-600 bg-indigo-50 px-4 py-2.5 text-center text-sm font-medium text-indigo-700">
                                    Employer
                                </button>
                            }
                            {if role != "employer":
                                <button type="button" onclick={lambda e: setRole("employer")}
                                    class="rounded-lg border-2 border-gray-200 bg-white px-4 py-2.5 text-center text-sm font-medium text-gray-600">
                                    Employer
                                </button>
                            }
                        </div>
                    </div>
                    <div>
                        <label class="block mb-1 text-sm font-medium text-gray-700">Full name</label>
                        <input type="text" value={full_name} oninput={lambda e: setFullName(e.target.value)}
                            required placeholder="John Doe"
                            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                    </div>
                    <div>
                        <label class="block mb-1 text-sm font-medium text-gray-700">Email</label>
                        <input type="email" value={email} oninput={lambda e: setEmail(e.target.value)}
                            required placeholder="you@example.com"
                            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                    </div>
                    <div>
                        <label class="block mb-1 text-sm font-medium text-gray-700">Username</label>
                        <input type="text" value={username} oninput={lambda e: setUsername(e.target.value)}
                            required placeholder="johndoe"
                            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                    </div>
                    <div>
                        <label class="block mb-1 text-sm font-medium text-gray-700">Password</label>
                        <input type="password" value={password} oninput={lambda e: setPassword(e.target.value)}
                            required minlength="6" placeholder="At least 6 characters"
                            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                    </div>
                    <button type="submit" 
                        class="w-full rounded-lg bg-indigo-600 px-4 py-2.5 font-semibold text-white hover:bg-indigo-700 disabled:opacity-50">
                        
                            <p>Create account</p>
                        
                    </button>
                </form>
                <p class="mt-6 text-sm text-center text-gray-600">
                    Already have an account?{" "}
                    <a href="/jobs/login" class="font-medium text-indigo-600 hover:text-indigo-500">Log in</a>
                </p>
            </div>
        </div>
    )


default = RegisterPage
