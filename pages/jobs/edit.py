"""
JobHub - Edit job listing page.
"""

from nextpy.psx import interactive_component, useState, callServerAction


@interactive_component
def EditJobForm(props=None):
    props = props or {}
    job = props.get("job")

    [saving, setSaving] = useState(False)
    [error, setError] = useState("")
    [_server_result, _setServerResult] = useState(None)

    def handle_update(e):
        setSaving(True)
        setError("")
        callServerAction("update_job", {
            "job_id": int(e.target.elements.job_id.value),
            "title": e.target.elements.job_title.value,
            "company": e.target.elements.company.value,
            "location": e.target.elements.location.value,
            "description": e.target.elements.description.value,
            "salary_min": e.target.elements.salary_min.value,
            "salary_max": e.target.elements.salary_max.value,
            "job_type": e.target.elements.job_type.value,
            "experience_level": e.target.elements.experience_level.value,
        })
        if _server_result and _server_result.get("success"):
            window.nextpyHardNavigate("/jobs/dashboard")
        else:
            if _server_result:
                setError(_server_result.get("error", "Failed to update job."))
            else:
                setError("Failed to update job.")
            setSaving(False)

    if not job:
        return (
            <div class="py-16 text-center">
                <h1 class="text-2xl font-bold text-gray-900">Job not found</h1>
                <p class="mt-2 text-gray-600">You can only edit jobs that you posted.</p>
                <a href="/jobs/dashboard" class="inline-block mt-4 text-indigo-600 hover:text-indigo-500">Back to dashboard</a>
            </div>
        )

    job_types = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("contract", "Contract"),
        ("internship", "Internship"),
    ]
    experience_levels = [
        ("entry", "Entry Level"),
        ("mid", "Mid Level"),
        ("senior", "Senior Level"),
        ("lead", "Lead / Principal"),
    ]
    job_type_options = "".join(
        f'<option value="{value}" {"selected" if job.get("job_type") == value else ""}>{label}</option>'
        for value, label in job_types
    )
    experience_options = "".join(
        f'<option value="{value}" {"selected" if job.get("experience_level") == value else ""}>{label}</option>'
        for value, label in experience_levels
    )

    return (
        <div class="max-w-2xl mx-auto">
            <div class="mb-8">
                <a href="/jobs/dashboard" class="text-sm font-medium text-gray-500 hover:text-indigo-600">Back to dashboard</a>
                <h1 class="mt-3 text-3xl font-bold text-gray-900">Edit Job Posting</h1>
                <p class="mt-1 text-gray-600">Update the details for this job listing.</p>
            </div>
            <div class="p-8 bg-white border border-gray-200 shadow-sm rounded-xl">
                {if error:
                    <div class="p-3 mb-4 text-sm text-red-700 rounded-lg bg-red-50">{error}</div>
                }
                <form onsubmit={handle_update} class="space-y-6">
                    <input type="hidden" name="job_id" value={job["id"]} />
                    <div class="grid gap-6 sm:grid-cols-2">
                        <div class="sm:col-span-2">
                            <label class="block mb-1 text-sm font-medium text-gray-700">Job Title *</label>
                            <input type="text" name="job_title" value={job["title"]} required
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Company *</label>
                            <input type="text" name="company" value={job["company"]} required
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Location</label>
                            <input type="text" name="location" value={job.get("location", "")}
                                placeholder="e.g. New York, NY or Remote"
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Job Type</label>
                            <select name="job_type"
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
                                {job_type_options}
                            </select>
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Experience Level</label>
                            <select name="experience_level"
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
                                {experience_options}
                            </select>
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Min Salary ($)</label>
                            <input type="number" name="salary_min" min="0" value={job.get("salary_min", 0)}
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                        </div>
                        <div>
                            <label class="block mb-1 text-sm font-medium text-gray-700">Max Salary ($)</label>
                            <input type="number" name="salary_max" min="0" value={job.get("salary_max", 0)}
                                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
                        </div>
                    </div>
                    <div>
                        <label class="block mb-1 text-sm font-medium text-gray-700">Job Description *</label>
                        <textarea name="description" rows="8" required
                            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">{job.get("description", "")}</textarea>
                    </div>
                    <div class="flex items-center gap-4">
                        <button type="submit"
                            class="px-6 py-3 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50">
                            Save Changes
                        </button>
                        <a href="/jobs/dashboard" class="text-sm font-medium text-gray-600 hover:text-gray-800">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    )


def getServerSideProps(context):
    from nextpy.db import get_session, Job
    from nextpy.auth import get_user_id_from_request

    request = context.get("request") or context.get("req")
    user_id = get_user_id_from_request(request) if request else None
    if user_id is None:
        return {"props": {"job": None}}

    query = context.get("query", {}) or {}
    try:
        job_id = int(query.get("id", 0))
    except (ValueError, TypeError):
        return {"props": {"job": None}}

    db = get_session()
    try:
        job = (
            db.query(Job)
            .filter(Job.id == job_id, Job.employer_id == user_id, Job.is_active == True)
            .first()
        )
        if job is None:
            return {"props": {"job": None}}
        return {
            "props": {
                "job": {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location or "",
                    "description": job.description or "",
                    "salary_min": job.salary_min or 0,
                    "salary_max": job.salary_max or 0,
                    "job_type": job.job_type or "full_time",
                    "experience_level": job.experience_level or "mid",
                }
            }
        }
    finally:
        db.close()


default = EditJobForm
