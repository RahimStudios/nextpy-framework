"""
JobHub — Browse / search jobs page.

Jobs are fetched during SSR so the first paint contains real results and
GET filters (?search=&job_type=&experience_level=) work without relying on
client-side list re-rendering.
"""

from nextpy.psx import interactive_component
from urllib.parse import urlencode


def job_type_label(jt):
    labels = {"full_time": "Full-time", "part_time": "Part-time", "contract": "Contract", "internship": "Internship"}
    return labels.get(jt, jt)


@interactive_component
def JobsBrowse(props=None):
    props = props or {}
    search = props.get("search", "") or ""
    job_type = props.get("job_type", "") or ""
    experience_level = props.get("experience_level", "") or ""
    per_page = int(props.get("per_page") or 6)
    if per_page < 1:
        per_page = 6
    if per_page > 50:
        per_page = 50
    jobs = props.get("jobs") or []
    pagination = props.get("pagination") or {}
    page = int(pagination.get("page") or 1)
    total = int(pagination.get("total") or len(jobs))
    if not isinstance(jobs, list):
        jobs = []
    jobs = [dict(job) for job in jobs]
    for job in jobs:
        job["type_label"] = job_type_label(job.get("job_type", "full_time"))
        job["location"] = job.get("location") or "Remote"

    JOB_TYPES = [
        ("", "All Types"),
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("contract", "Contract"),
        ("internship", "Internships"),
    ]
    LEVELS = [
        ("", "All Levels"),
        ("entry", "Entry"),
        ("mid", "Mid"),
        ("senior", "Senior"),
        ("lead", "Lead"),
    ]

    job_type_options = "".join(
        f'<option value="{val}" {"selected" if val == job_type else ""}>{label}</option>'
        for val, label in JOB_TYPES
    )
    level_options = "".join(
        f'<option value="{val}" {"selected" if val == experience_level else ""}>{label}</option>'
        for val, label in LEVELS
    )

    def page_url(target_page):
        params = {"page": target_page}
        if search:
            params["search"] = search
        if job_type:
            params["job_type"] = job_type
        if experience_level:
            params["experience_level"] = experience_level
        if per_page != 6:
            params["per_page"] = per_page
        return "/jobs/browse?" + urlencode(params)

    prev_url = page_url(max(1, page - 1))
    next_url = page_url(page + 1)
    page_count = int(pagination.get("pages") or 0)
    has_prev = pagination.get("has_prev")
    has_next = pagination.get("has_next")
    prev_html = (
        f'<a href="{prev_url}" class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Previous</a>'
        if has_prev else "<span></span>"
    )
    next_html = (
        f'<a href="{next_url}" class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Next</a>'
        if has_next else "<span></span>"
    )
    pagination_html = (
        '<div class="flex items-center justify-between pt-4 mt-8 border-t border-gray-200">'
        + prev_html
        + f'<span class="text-sm text-gray-500">Page {page} of {page_count}</span>'
        + next_html
        + "</div>"
    ) if page_count > 1 else ""
    return (
        <div>
            <div class="mb-8">
                <h1 class="text-3xl font-bold text-gray-900">Browse Jobs</h1>
                <p class="mt-1 text-gray-600">{total} positions available</p>
            </div>

            <form method="GET" action="/jobs/browse" class="p-6 mb-8 bg-white border border-gray-200 shadow-sm rounded-xl">
                <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    <div class="sm:col-span-2">
                        <label class="block mb-1 text-sm font-medium text-gray-700">Search</label>
                        <input name="search" value={search} placeholder="Job title, company..."
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
                        <label class="block mb-1 text-sm font-medium text-gray-700">Experience</label>
                        <select name="experience_level"
                            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
                            {level_options}
                        </select>
                    </div>
                </div>
                <div class="flex items-center gap-3 mt-4">
                    <button type="submit" class="rounded-lg bg-indigo-600 px-5 py-2.5 font-semibold text-white hover:bg-indigo-700">Search</button>
                    <a href="/jobs/browse" class="rounded-lg px-5 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-100">Clear filters</a>
                </div>
            </form>

            {if len(jobs) == 0:
                <div class="p-12 text-center bg-white border border-gray-300 border-dashed rounded-xl">
                    <p class="text-lg font-medium text-gray-500">No jobs match your filters.</p>
                    <a href="/jobs/browse" class="inline-block mt-3 text-sm font-medium text-indigo-600 hover:text-indigo-500">Clear filters</a>
                </div>
            }

            <div class="space-y-4">
                {for job in jobs:
                    <a href="/jobs/{job['id']}"
                        class="block p-6 transition bg-white border border-gray-200 shadow-sm group rounded-xl hover:shadow-md hover:border-indigo-300">
                        <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                            <div class="flex-1">
                                <div class="flex flex-wrap items-center gap-2 mb-2">
                                    <span class="inline-block rounded-full bg-indigo-100 px-2.5 py-0.5 text-xs font-medium text-indigo-700">
                                        {job["type_label"]}
                                    </span>
                                    <span class="inline-block rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-700">
                                        {job.get("experience_level", "mid").title()}
                                    </span>
                                </div>
                                <h3 class="text-lg font-semibold text-gray-900 group-hover:text-indigo-600">{job["title"]}</h3>
                                <p class="mt-1 text-sm text-gray-600">{job["company"]}</p>
                                <p class="mt-2 text-sm text-gray-500 line-clamp-2">{job.get("description", "")[:150]}</p>
                            </div>
                            <div class="flex flex-col items-end gap-2 text-sm text-gray-500 sm:min-w-[140px]">
                                <span>{job["location"]}</span>
                            </div>
                        </div>
                    </a>
                }
            </div>

            {pagination_html}
        </div>
    )


def _serialize_job(job):
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location or "",
        "description": job.description or "",
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "job_type": job.job_type or "full_time",
        "experience_level": job.experience_level or "mid",
        "employer_id": job.employer_id,
        "is_active": job.is_active,
        "created_at": job.created_at.isoformat() if job.created_at else None,
    }


def getServerSideProps(context):
    from nextpy.db import get_session, Job, apply_filters, paginate

    query_params = context.get("query", {}) or {}
    search = (query_params.get("search", "") or "").strip()
    job_type = (query_params.get("job_type", "") or "").strip()
    experience_level = (query_params.get("experience_level", "") or "").strip()
    try:
        page = max(1, int(query_params.get("page", 1) or 1))
    except (TypeError, ValueError):
        page = 1
    try:
        per_page = min(50, max(1, int(query_params.get("per_page", 6) or 6)))
    except (TypeError, ValueError):
        per_page = 6

    db = get_session()
    try:
        query = apply_filters(
            db.query(Job),
            Job,
            {"is_active": True, "job_type": job_type, "experience_level": experience_level},
            allowed=("is_active", "job_type", "experience_level"),
            search=search,
            search_fields=("title", "company", "description"),
        )
        result = paginate(query.order_by(Job.created_at.desc()), page, per_page)
        return {
            "props": {
                "search": search,
                "job_type": job_type,
                "experience_level": experience_level,
                "per_page": per_page,
                "jobs": [_serialize_job(j) for j in result.items],
                "pagination": result.to_dict(),
            }
        }
    finally:
        db.close()


streaming = True
default = JobsBrowse
