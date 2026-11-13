"""
JobHub - Create job listing page. Uses interactive_component with callServerAction.
"""

from nextpy.psx import component, interactive_component, useState, useEffect, callServerAction, Motion


@interactive_component
def CreateJobForm(props=None):
    [title, setTitle] = useState("")
    [company, setCompany] = useState("")
    [location, setLocation] = useState("")
    [description, setDescription] = useState("")
    [salaryMin, setSalaryMin] = useState("")
    [salaryMax, setSalaryMax] = useState("")
    [jobType, setJobType] = useState("full_time")
    [experienceLevel, setExperienceLevel] = useState("mid")
    [error, setError] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def handle_create(e):
        setError("")
        params = {
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "salary_min": int(salaryMin) if salaryMin else 0,
            "salary_max": int(salaryMax) if salaryMax else 0,
            "job_type": jobType,
            "experience_level": experienceLevel,
        }
        callServerAction("create_job", params)

    def handle_result():
        if _server_result:
            if _server_result.get("success"):
                window.navigateTo("/jobs/dashboard")
            else:
                setError(_server_result.get("error", "Failed to create job."))

    useEffect(handle_result, [_server_result])

    return (
        <div class="max-w-2xl mx-auto">
            <Motion
                initial={{"opacity": 0, "transform": "translateY(24px)"}}
                animate={{"opacity": 1, "transform": "translateY(0px)"}}
                transition={{"duration": 0.5, "easing": "ease-out"}}
            >
            <div class="mb-8">
                <h1 class="text-3xl font-bold tracking-tight text-gray-900">Post a New Job</h1>
                <p class="mt-1 text-gray-500">Fill out the details below to list your job opening.</p>
            </div>
            <div class="rounded-2xl border border-gray-200 bg-white p-8 shadow-xl shadow-gray-900/5">
                {if error:
                    <div class="p-3 mb-4 text-sm text-red-700 rounded-lg bg-red-50" data-state-error></div>
                }
                <form onsubmit={handle_create} class="space-y-6">
                    <div class="grid gap-6 sm:grid-cols-2">
                        <div class="sm:col-span-2">
                            <label class="block mb-1 text-sm font-medium text-gray-700">Job Title *</label>
                            <input type="text" value={title} oninput={lambda e: setTitle(e.target.value)}
                                required placeholder="e.g. Senior React Developer"
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Company *</label>
                            <input type="text" value={company} oninput={lambda e: setCompany(e.target.value)}
                                required placeholder="e.g. Acme Corp"
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Location</label>
                            <input type="text" value={location} oninput={lambda e: setLocation(e.target.value)}
                                placeholder="e.g. New York, NY or Remote"
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Job Type</label>
                            <select value={jobType} oninput={lambda e: setJobType(e.target.value)}
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
                                <option value="full_time">Full-time</option>
                                <option value="part_time">Part-time</option>
                                <option value="contract">Contract</option>
                                <option value="internship">Internship</option>
                            </select>
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Experience Level</label>
                            <select value={experienceLevel} oninput={lambda e: setExperienceLevel(e.target.value)}
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
                                <option value="entry">Entry Level</option>
                                <option value="mid">Mid Level</option>
                                <option value="senior">Senior Level</option>
                                <option value="lead">Lead / Principal</option>
                            </select>
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Min Salary ($)</label>
                            <input type="number" value={salaryMin} oninput={lambda e: setSalaryMin(e.target.value)}
                                min="0" placeholder="e.g. 50000"
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Max Salary ($)</label>
                            <input type="number" value={salaryMax} oninput={lambda e: setSalaryMax(e.target.value)}
                                min="0" placeholder="e.g. 90000"
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                        </div>
                    </div>
                    <div>
                        <label class="block mb-1 text-sm font-medium text-gray-700">Job Description *</label>
                        <textarea rows="8" value={description} oninput={lambda e: setDescription(e.target.value)}
                            required placeholder="Describe the role, responsibilities, requirements, and benefits..."
                            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
                        </textarea>
                    </div>
                    <div class="flex items-center gap-4">
                        <button type="submit" disabled={_server_loading}
                            class="flex items-center gap-2 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 px-6 py-3 font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all hover:shadow-xl hover:brightness-110 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60">
                            {if _server_loading:
                                <span class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white"></span>
                            }
                            <span>{"Publishing..." if _server_loading else "Publish"}</span>
                        </button>
                        <a href="/jobs/dashboard" class="text-sm font-semibold text-gray-500 transition hover:text-gray-800">Cancel</a>
                    </div>
                </form>
            </div>
            </Motion>
        </div>
    )


default = CreateJobForm
