"""
JobHub - Dashboard page.
Employer sees their posted jobs + applications. Job seeker sees their applications.

The authenticated user and their data are resolved during SSR so the page
never flashes "Please log in" after a successful login/registration.
"""

from nextpy.psx import interactive_component, useState, callServerAction, psx
import html as _html


def _text(value):
    return _html.escape(str(value if value is not None else ""))


def _attr(value):
    return _html.escape(str(value if value is not None else ""), quote=True)


def _jobs_section(jobs):
    if not jobs:
        return (
            '<div class="p-12 text-center bg-white border border-gray-300 border-dashed rounded-xl">'
            '<p class="text-gray-500">You haven\'t posted any jobs yet.</p>'
            '<a href="/jobs/create" class="inline-block mt-3 text-sm font-medium text-indigo-600">Post your first job</a>'
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
            f'<div class="p-6 bg-white border border-gray-200 shadow-sm rounded-xl">'
            f'<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">'
            f'<div class="flex-1">'
            f'<div class="flex items-center gap-2">'
            f'<h3 class="font-semibold text-gray-900"><a href="/jobs/{jid}" class="hover:text-indigo-600">{title}</a></h3>'
            f'<span class="rounded-full px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700">Active</span>'
            f'</div>'
            f'<p class="mt-1 text-sm text-gray-500">{company} - {location}</p>'
            f'</div>'
            f'<div class="flex items-center gap-3">'
            f'<span class="text-sm text-gray-500">{app_count} application{suffix}</span>'
            f'<a href="/jobs/edit?id={jid}" class="text-sm font-medium text-indigo-600 hover:text-indigo-800">Edit</a>'
            f'<button data-handler-click="handle_open_delete" data-job-id="{jid}" '
            f'data-job-title="{_attr(title_raw)}" class="text-sm font-medium text-red-600 hover:text-red-800">Delete</button>'
            f'</div></div></div>'
        )
    return '<div class="space-y-4">' + "".join(cards) + '</div>'


def _applications_section(apps):
    if not apps:
        return (
            '<div class="p-12 text-center bg-white border border-gray-300 border-dashed rounded-xl">'
            '<p class="text-gray-500">You haven\'t applied to any jobs yet.</p>'
            '<a href="/jobs/browse" class="inline-block mt-3 text-sm font-medium text-indigo-600">Browse jobs</a>'
            '</div>'
        )

    cards = []
    for app in apps:
        job = app.get("job") or {}
        job_title = _text(job.get("title") or "Job no longer available")
        company = _text(job.get("company"))
        applied = _text((app.get("created_at") or "")[:10])
        status = str(app.get("status") or "pending")
        status_text = _text(status.title())
        status_class = (
            "bg-yellow-100 text-yellow-700" if status == "pending"
            else "bg-green-100 text-green-700" if status == "accepted"
            else "bg-red-100 text-red-700"
        )
        if job.get("id"):
            title_html = f'<a href="/jobs/{int(job["id"])}" class="font-semibold text-gray-900 hover:text-indigo-600">{job_title}</a>'
        else:
            title_html = f'<span class="font-semibold text-gray-900">{job_title}</span>'
        cards.append(
            f'<div class="flex items-center justify-between p-5 bg-white border border-gray-200 shadow-sm rounded-xl">'
            f'<div>{title_html}<p class="text-sm text-gray-500">{company}{" - Applied " if company else "Applied "}{applied}</p></div>'
            f'<span class="rounded-full px-3 py-1 text-xs font-medium {status_class}">{status_text}</span>'
            f'</div>'
        )
    return '<div class="space-y-3">' + "".join(cards) + '</div>'


@interactive_component
def DashboardPage(props=None):
    props = props or {}
    user = props.get("user")
    my_jobs = props.get("my_jobs") or []
    my_apps = props.get("my_apps") or []
    if not isinstance(my_jobs, list):
        my_jobs = []
    if not isinstance(my_apps, list):
        my_apps = []

    is_employer = bool(user and user.get("role") == "employer")

    [confirming_delete, setConfirmingDelete] = useState(None)
    [delete_title, setDeleteTitle] = useState("")
    [deleting, setDeleting] = useState(False)
    [delete_error, setDeleteError] = useState("")
    [_server_result, _setServerResult] = useState(None)

    def handle_open_delete(e):
        setConfirmingDelete(int(e.currentTarget.dataset.jobId))
        setDeleteTitle(e.currentTarget.dataset.jobTitle)
        setDeleteError("")

    def handle_cancel_delete(e):
        setConfirmingDelete(None)
        setDeleteTitle("")
        setDeleteError("")

    def handle_delete_job(e):
        setDeleting(True)
        setDeleteError("")
        callServerAction("delete_job", {"job_id": int(confirming_delete)})
        if _server_result and _server_result.get("success"):
            window.spaReload()
        else:
            if _server_result:
                setDeleteError(_server_result.get("error", "Failed to delete job."))
            else:
                setDeleteError("Failed to delete job.")
            setDeleting(False)

    def handle_update_status(app_id, new_status):
        callServerAction("update_application_status", {"application_id": app_id, "status": new_status})
        window.spaReload()

    if not user:
        content = (
            '<div class="py-16 text-center">'
            '<h1 class="text-2xl font-bold text-gray-900">Please log in</h1>'
            '<a href="/jobs/login" class="inline-block mt-4 text-indigo-600 hover:text-indigo-500">Go to login</a>'
            '</div>'
        )
    else:
        name = _text(user.get("full_name") or user.get("username") or "")
        email = _text(user.get("email"))
        role_label = "Employer Dashboard" if is_employer else "Job Seeker Dashboard"
        section = _jobs_section(my_jobs) if is_employer else _applications_section(my_apps)
        content = (
            f'<div><div class="mb-8">'
            f'<h1 class="text-3xl font-bold text-gray-900">Welcome, {name}</h1>'
            f'<p class="mt-1 text-gray-600">{role_label} - {email}</p>'
            f'</div>{section}</div>'
        )

    content_element = psx(content)

    return (
        <div>
            {content_element}

            {if confirming_delete:
                <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40">
                    <div class="w-full max-w-md p-6 bg-white shadow-2xl rounded-xl">
                        <h3 class="mb-2 text-lg font-semibold text-gray-900">Delete job posting?</h3>
                        <p class="mb-4 text-sm text-gray-600">
                            Are you sure you want to delete
                            <span data-state-delete_title class="font-semibold text-gray-900"></span>?
                            This action cannot be undone.
                        </p>
                        <div data-state-delete_error data-state-toggle style="display: none" class="p-3 mb-4 text-sm text-red-700 rounded-lg bg-red-50"></div>
                        <div class="flex justify-end gap-3">
                            <button type="button" data-handler-click="handle_cancel_delete"
                                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50">
                                Cancel
                            </button>
                            <button type="button" data-handler-click="handle_delete_job"
                                class="px-5 py-2 text-sm font-semibold text-white bg-red-600 rounded-lg hover:bg-red-700 disabled:opacity-50">
                                Delete Job
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


def _application_to_dict(app):
    job = getattr(app, "job", None)
    return {
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


def getServerSideProps(context):
    from nextpy.db import get_session, User, Job, Application, count_by
    from nextpy.auth import get_user_id_from_request

    request = context.get("request") or context.get("req")
    user_id = get_user_id_from_request(request) if request else None
    if user_id is None:
        return {"props": {"user": None, "is_employer": False, "my_jobs": [], "my_apps": []}}

    db = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            return {"props": {"user": None, "is_employer": False, "my_jobs": [], "my_apps": []}}

        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name or "",
            "role": user.role or "job_seeker",
        }

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
        my_jobs = [_job_to_dict(job, counts.get(job.id, 0)) for job in jobs]

        applications = (
            db.query(Application)
            .filter(Application.applicant_id == user.id)
            .order_by(Application.created_at.desc())
            .all()
        )
        my_apps = [_application_to_dict(app) for app in applications]

        return {
            "props": {
                "user": user_data,
                "is_employer": bool(user_data.get("role") == "employer"),
                "my_jobs": my_jobs,
                "my_apps": my_apps,
            }
        }
    finally:
        db.close()


default = DashboardPage
