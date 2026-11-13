"""
JobHub - Dashboard page.
Employer sees their posted jobs + incoming applications.
Job seeker sees their own applications.

The authenticated user and their data are resolved during SSR so the page
never flashes "Please log in" after a successful login/registration.
"""

from nextpy.psx import interactive_component, useState, useEffect, callServerAction, psx, Motion
import html as _html


def _text(value):
    return _html.escape(str(value if value is not None else ""))


def _attr(value):
    return _html.escape(str(value if value is not None else ""), quote=True)


def _status_badge(status):
    status = str(status or "pending")
    cls = (
        "bg-yellow-100 text-yellow-700" if status == "pending"
        else "bg-green-100 text-green-700" if status == "accepted"
        else "bg-red-100 text-red-700" if status == "rejected"
        else "bg-gray-100 text-gray-600"
    )
    return f'<span class="rounded-full px-3 py-1 text-xs font-semibold {cls}">{_text(status.title())}</span>'


def _jobs_section(jobs):
    if not jobs:
        return (
            '<div class="rounded-2xl border border-gray-300 border-dashed bg-white p-12 text-center">'
            '<p class="text-gray-500">You haven\'t posted any jobs yet.</p>'
            '<a href="/jobs/create" class="mt-3 inline-block text-sm font-semibold text-indigo-600 hover:text-indigo-500">Post your first job</a>'
            '</div>'
        )

    cards = []
    for job in jobs:
        jid = int(job.get("id") or 0)
        title_raw = str(job.get("title") or "")
        title = _text(title_raw)
        company = _text(job.get("company"))
        location = _text(job.get("location") or "Remote")
        app_count = int(job.get("app_count") or 0)
        suffix = "s" if app_count != 1 else ""
        cards.append(
            f'<div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition hover:border-indigo-300 hover:shadow-md">'
            f'<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">'
            f'<div class="flex-1">'
            f'<div class="flex items-center gap-2">'
            f'<h3 class="font-semibold text-gray-900"><a href="/jobs/{jid}" class="transition hover:text-indigo-600">{title}</a></h3>'
            f'<span class="rounded-full bg-green-100 px-2 py-0.5 text-xs font-semibold text-green-700">Active</span>'
            f'</div>'
            f'<p class="mt-1 text-sm text-gray-500">{company} &middot; {location}</p>'
            f'</div>'
            f'<div class="flex items-center gap-4">'
            f'<span class="text-sm font-medium text-gray-500">{app_count} application{suffix}</span>'
            f'<a href="/jobs/edit?id={jid}" class="text-sm font-semibold text-indigo-600 transition hover:text-indigo-800">Edit</a>'
            f'<button data-handler-click="handle_open_delete" data-job-id="{jid}" '
            f'data-job-title="{_attr(title_raw)}" class="text-sm font-semibold text-red-500 transition hover:text-red-700">Delete</button>'
            f'</div></div></div>'
        )
    return '<div class="space-y-4">' + "".join(cards) + '</div>'


def _applications_section(apps, show_job=True):
    if not apps:
        return (
            '<div class="rounded-2xl border border-gray-300 border-dashed bg-white p-12 text-center">'
            '<p class="text-gray-500">No applications yet.</p>'
            '<a href="/jobs/browse" class="mt-3 inline-block text-sm font-semibold text-indigo-600 hover:text-indigo-500">Browse jobs</a>'
            '</div>'
        )

    cards = []
    for app in apps:
        job = app.get("job") or {}
        applicant = app.get("applicant") or {}
        applied = _text((app.get("created_at") or "")[:10])
        status = str(app.get("status") or "pending")

        if show_job:
            # Employer view: show applicant + which job they applied to
            who = _text(applicant.get("full_name") or applicant.get("email") or "Anonymous")
            job_title = _text(job.get("title") or "Unknown job")
            left = (
                f'<p class="font-semibold text-gray-900">{who}</p>'
                f'<p class="text-sm text-gray-500">Applied to <span class="font-medium text-gray-700">{job_title}</span>'
                f'{" &middot; " + applied if applied else ""}</p>'
            )
        else:
            # Job seeker view: show the job they applied to
            job_title = _text(job.get("title") or "Job no longer available")
            company = _text(job.get("company"))
            if job.get("id"):
                title_html = f'<a href="/jobs/{int(job["id"])}" class="font-semibold text-gray-900 transition hover:text-indigo-600">{job_title}</a>'
            else:
                title_html = f'<span class="font-semibold text-gray-900">{job_title}</span>'
            left = (
                f'{title_html}<p class="text-sm text-gray-500">{company}{" &middot; Applied " if company else "Applied "}{applied}</p>'
            )

        status_html = _status_badge(status)
        actions = ""
        if show_job:
            app_id = int(app.get("id") or 0)
            if status == "pending":
                actions = (
                    f'<div class="flex items-center gap-2">'
                    f'<button data-handler-click="handle_update_status" data-app-id="{app_id}" data-new-status="accepted" '
                    f'class="rounded-lg bg-green-600 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-green-700">Accept</button>'
                    f'<button data-handler-click="handle_update_status" data-app-id="{app_id}" data-new-status="rejected" '
                    f'class="rounded-lg bg-red-100 px-3 py-1.5 text-xs font-semibold text-red-700 transition hover:bg-red-200">Reject</button>'
                    f'</div>'
                )
            elif status != "accepted":
                actions = (
                    f'<button data-handler-click="handle_update_status" data-app-id="{app_id}" data-new-status="accepted" '
                    f'class="rounded-lg bg-green-600 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-green-700">Accept</button>'
                )

        cards.append(
            f'<div class="flex items-center justify-between gap-4 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm transition hover:border-indigo-200">'
            f'<div class="min-w-0">{left}</div>'
            f'<div class="flex shrink-0 items-center gap-3">{status_html}{actions}</div>'
            f'</div>'
        )
    return '<div class="space-y-3">' + "".join(cards) + '</div>'


@interactive_component
def DashboardPage(props=None):
    props = props or {}
    user = props.get("user")
    my_jobs = props.get("my_jobs") or []
    my_apps = props.get("my_apps") or []
    received_apps = props.get("received_apps") or []
    if not isinstance(my_jobs, list):
        my_jobs = []
    if not isinstance(my_apps, list):
        my_apps = []
    if not isinstance(received_apps, list):
        received_apps = []

    is_employer = bool(user and user.get("role") == "employer")

    [confirming_delete, setConfirmingDelete] = useState(None)
    [delete_title, setDeleteTitle] = useState("")
    [delete_error, setDeleteError] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def handle_open_delete(e):
        setConfirmingDelete(int(e.currentTarget.dataset.jobId))
        setDeleteTitle(e.currentTarget.dataset.jobTitle)
        setDeleteError("")

    def handle_cancel_delete(e):
        setConfirmingDelete(None)
        setDeleteTitle("")
        setDeleteError("")

    def handle_delete_job(e):
        setDeleteError("")
        callServerAction("delete_job", {"job_id": int(confirming_delete)})

    def handle_update_status(e):
        app_id = int(e.currentTarget.dataset.appId)
        new_status = e.currentTarget.dataset.newStatus
        callServerAction("update_application_status", {"application_id": app_id, "status": new_status})

    def handle_result():
        if _server_result:
            if _server_result.get("success"):
                window.spaReload()
            else:
                setDeleteError(_server_result.get("error", "Failed to delete job."))

    useEffect(handle_result, [_server_result])

    if not user:
        content = (
            '<div class="py-16 text-center">'
            '<h1 class="text-2xl font-bold text-gray-900">Please log in</h1>'
            '<a href="/jobs/login" class="mt-4 inline-block text-indigo-600 hover:text-indigo-500">Go to login</a>'
            '</div>'
        )
    else:
        name = _text(user.get("full_name") or user.get("username") or "")
        email = _text(user.get("email"))
        role_label = "Employer Dashboard" if is_employer else "Job Seeker Dashboard"
        if is_employer:
            section = (
                '<h2 class="mb-4 text-xl font-bold text-gray-900">Your job postings</h2>'
                + _jobs_section(my_jobs)
                + '<h2 class="mb-4 mt-12 text-xl font-bold text-gray-900">Applications</h2>'
                + _applications_section(received_apps, show_job=True)
            )
        else:
            section = (
                '<h2 class="mb-4 text-xl font-bold text-gray-900">Your applications</h2>'
                + _applications_section(my_apps, show_job=False)
            )
        content = (
            f'<div><div class="mb-8">'
            f'<h1 class="text-3xl font-bold tracking-tight text-gray-900">Welcome, {name}</h1>'
            f'<p class="mt-1 text-gray-500">{role_label} &middot; {email}</p>'
            f'</div>{section}</div>'
        )

    content_element = psx(content)

    return (
        <div>
            {content_element}

            {if confirming_delete:
                <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4 backdrop-blur-sm">
                    <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
                        <h3 class="mb-2 text-lg font-bold text-gray-900">Delete job posting?</h3>
                        <p class="mb-1 text-sm text-gray-600">Are you sure you want to delete</p>
                        <p class="mb-4 truncate text-sm font-semibold text-gray-900">{delete_title}</p>
                        <p class="mb-4 text-xs text-gray-400">This action cannot be undone.</p>
                        {if delete_error:
                            <div class="mb-4 rounded-xl border border-red-200 bg-red-50 p-3 text-sm font-medium text-red-700" data-state-delete_error></div>
                        }
                        <div class="flex justify-end gap-3">
                            <button type="button" data-handler-click="handle_cancel_delete"
                                class="rounded-xl px-4 py-2.5 text-sm font-semibold text-gray-700 transition hover:bg-gray-100">
                                Cancel
                            </button>
                            <button type="button" data-handler-click="handle_delete_job" disabled={_server_loading}
                                class="rounded-xl bg-red-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-red-700 disabled:opacity-60">
                                {"Deleting..." if _server_loading else "Delete Job"}
                            </button>
                        </div>
                    </div>
                </div>
            }
        </div>
    )


def _job_to_dict(job, app_count=0):
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location or "",
        "description": job.description or "",
        "job_type": job.job_type or "full_time",
        "experience_level": job.experience_level or "mid",
        "is_active": job.is_active,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "app_count": app_count,
    }


def _application_to_dict(app, include_applicant=False):
    job = getattr(app, "job", None)
    data = {
        "id": app.id,
        "job_id": app.job_id,
        "applicant_id": app.applicant_id,
        "cover_letter": app.cover_letter or "",
        "status": app.status or "pending",
        "created_at": app.created_at.isoformat() if app.created_at else None,
        "job": {
            "id": job.id,
            "title": job.title,
            "company": job.company,
        } if job else None,
    }
    if include_applicant:
        applicant = getattr(app, "applicant", None)
        data["applicant"] = {
            "id": applicant.id,
            "email": applicant.email,
            "full_name": applicant.full_name or "",
            "username": applicant.username or "",
        } if applicant else None
    return data


def getServerSideProps(context):
    from nextpy.db import get_session, User, Job, Application, count_by
    from nextpy.auth import get_user_id_from_request

    request = context.get("request") or context.get("req")
    user_id = get_user_id_from_request(request) if request else None
    if user_id is None:
        return {"props": {"user": None, "is_employer": False, "my_jobs": [], "my_apps": [], "received_apps": []}}

    db = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            return {"props": {"user": None, "is_employer": False, "my_jobs": [], "my_apps": [], "received_apps": []}}

        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name or "",
            "role": user.role or "job_seeker",
        }
        is_employer = user_data.get("role") == "employer"

        result = {
            "user": user_data,
            "is_employer": is_employer,
            "my_jobs": [],
            "my_apps": [],
            "received_apps": [],
        }

        if is_employer:
            jobs = (
                db.query(Job)
                .filter(Job.employer_id == user.id, Job.is_active == True)
                .order_by(Job.created_at.desc())
                .all()
            )
            job_ids = [job.id for job in jobs]
            counts = count_by(
                db, Application, "job_id", {"job_id": job_ids} if job_ids else None
            )
            result["my_jobs"] = [_job_to_dict(job, counts.get(job.id, 0)) for job in jobs]

            if job_ids:
                received = (
                    db.query(Application)
                    .filter(Application.job_id.in_(job_ids))
                    .order_by(Application.created_at.desc())
                    .limit(50)
                    .all()
                )
                result["received_apps"] = [
                    _application_to_dict(app, include_applicant=True) for app in received
                ]
        else:
            applications = (
                db.query(Application)
                .filter(Application.applicant_id == user.id)
                .order_by(Application.created_at.desc())
                .all()
            )
            result["my_apps"] = [_application_to_dict(app) for app in applications]

        return {"props": result}
    finally:
        db.close()


default = DashboardPage
