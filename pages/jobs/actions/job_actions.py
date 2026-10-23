"""
Job listing server actions — CRUD for jobs + applications.
All use the generic CRUD pattern with WebSocket broadcasts.
"""

from fastapi import Request
from nextpy.db import get_session, Job, Application, User, apply_filters, paginate, count_by
from nextpy.auth import get_user_id_from_request
from nextpy.server_actions import server_action


def _broadcast(channel, message_type, data, action="updated"):
    """Broadcast a CRUD event via WebSocket."""
    try:
        from nextpy.server.app import broadcast_to_channel
        import asyncio
        asyncio.create_task(broadcast_to_channel(channel, {
            "type": message_type,
            "action": action,
            "data": data,
        }))
    except Exception:
        pass


def _job_to_dict(job):
    """Serialize a Job model to a dict."""
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


def _application_to_dict(app):
    """Serialize an Application model without per-row database queries.

    ``Application.applicant`` and ``Application.job`` are joined eagerly by the
    ORM, so this is safe to call in a loop after a normal query.
    """
    applicant = None
    if getattr(app, "applicant", None) is not None:
        u = app.applicant
        applicant = {
            "id": u.id,
            "full_name": u.full_name or u.username,
            "email": u.email,
        }
    job = None
    if getattr(app, "job", None) is not None:
        j = app.job
        job = {"id": j.id, "title": j.title, "company": j.company}
    return {
        "id": app.id,
        "job_id": app.job_id,
        "applicant_id": app.applicant_id,
        "cover_letter": app.cover_letter or "",
        "status": app.status or "pending",
        "created_at": app.created_at.isoformat() if app.created_at else None,
        "applicant": applicant,
        "job": job,
    }


# ── Job CRUD ──

@server_action()
async def create_job(
    request: Request,
    title: str = "",
    company: str = "",
    location: str = "",
    description: str = "",
    salary_min: int = 0,
    salary_max: int = 0,
    job_type: str = "full_time",
    experience_level: str = "mid",
):
    """Create a new job listing."""
    user_id = get_user_id_from_request(request)
    if user_id is None:
        return {"success": False, "error": "You must be logged in to post a job"}

    title = (title or "").strip()
    company = (company or "").strip()
    description = (description or "").strip()
    if not title or not company or not description:
        return {"success": False, "error": "Title, company and description are required"}

    try:
        salary_min = int(salary_min) if salary_min else 0
        salary_max = int(salary_max) if salary_max else 0
    except (ValueError, TypeError):
        salary_min, salary_max = 0, 0

    db = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.role != "employer":
            user.role = "employer"
            db.commit()

        job = Job(
            title=title,
            company=company,
            location=location,
            description=description,
            salary_max=max(salary_max, 0),
            salary_min=max(salary_min, 0),
            job_type=job_type if job_type in ("full_time", "part_time", "contract", "internship") else "full_time",
            experience_level=experience_level if experience_level in ("entry", "mid", "senior", "lead") else "mid",
            employer_id=user_id,
            is_active=True,
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        data = _job_to_dict(job)
        _broadcast("jobs", "JOB_CHANGED", data, "created")
        return {"success": True, "data": data}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()


@server_action()
async def update_job(
    request: Request,
    job_id: int = 0,
    title: str = "",
    company: str = "",
    location: str = "",
    description: str = "",
    salary_min: str = "",
    salary_max: str = "",
    job_type: str = "full_time",
    experience_level: str = "mid",
):
    """Update an existing job listing."""
    user_id = get_user_id_from_request(request)
    if user_id is None:
        return {"success": False, "error": "Not authenticated"}

    title = (title or "").strip()
    company = (company or "").strip()
    description = (description or "").strip()
    if not title or not company or not description:
        return {"success": False, "error": "Title, company and description are required"}

    try:
        job_id = int(job_id)
    except (ValueError, TypeError):
        return {"success": False, "error": "Invalid job"}

    try:
        salary_min = int(salary_min) if str(salary_min).strip() else 0
        salary_max = int(salary_max) if str(salary_max).strip() else 0
    except (ValueError, TypeError):
        return {"success": False, "error": "Salary must be a number"}

    db = get_session()
    try:
        job = db.query(Job).filter(Job.id == job_id, Job.employer_id == user_id).first()
        if not job:
            return {"success": False, "error": "Job not found or not yours"}

        job.title = title
        job.company = company
        job.location = (location or "").strip()
        job.description = description
        job.salary_min = max(salary_min, 0)
        job.salary_max = max(salary_max, 0)
        if job_type in ("full_time", "part_time", "contract", "internship"):
            job.job_type = job_type
        if experience_level in ("entry", "mid", "senior", "lead"):
            job.experience_level = experience_level

        db.commit()
        db.refresh(job)
        data = _job_to_dict(job)
        _broadcast("jobs", "JOB_CHANGED", data, "updated")
        return {"success": True, "data": data}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()


@server_action()
async def delete_job(request: Request, job_id: int = 0):
    """Delete (deactivate) a job listing."""
    user_id = get_user_id_from_request(request)
    if user_id is None:
        return {"success": False, "error": "Not authenticated"}

    db = get_session()
    try:
        job = db.query(Job).filter(Job.id == job_id, Job.employer_id == user_id).first()
        if not job:
            return {"success": False, "error": "Job not found or not yours"}

        job.is_active = False
        db.commit()
        _broadcast("jobs", "JOB_CHANGED", {"id": job_id}, "deleted")
        return {"success": True, "message": "Job deleted"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()


@server_action()
async def get_my_jobs(request: Request):
    """Get all jobs posted by the current employer."""
    user_id = get_user_id_from_request(request)
    if user_id is None:
        return {"success": False, "error": "Not authenticated"}

    db = get_session()
    try:
        jobs = db.query(Job).filter(Job.employer_id == user_id).order_by(Job.created_at.desc()).all()
        job_ids = [job.id for job in jobs]
        counts = count_by(
            db, Application, "job_id", {"job_id": job_ids} if job_ids else None
        )
        result = []
        for job in jobs:
            data = _job_to_dict(job)
            data["app_count"] = counts.get(job.id, 0)
            result.append(data)
        return {"success": True, "data": result}
    finally:
        db.close()


@server_action()
async def list_jobs(
    search: str = "",
    job_type: str = "",
    experience_level: str = "",
    page: int = 1,
    per_page: int = 20,
):
    """List active jobs with filters and pagination."""
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
            "success": True,
            "data": [_job_to_dict(job) for job in result.items],
            "pagination": result.to_dict(),
        }
    finally:
        db.close()


# ── Application CRUD ──

@server_action()
async def apply_to_job(request: Request, job_id: int = 0, cover_letter: str = ""):
    """Apply to a job."""
    user_id = get_user_id_from_request(request)
    if user_id is None:
        return {"success": False, "error": "You must be logged in to apply"}

    db = get_session()
    try:
        job = db.query(Job).filter(Job.id == job_id, Job.is_active == True).first()
        if not job:
            return {"success": False, "error": "Job not found"}
        if job.employer_id == user_id:
            return {"success": False, "error": "You cannot apply to your own job"}

        existing = (
            db.query(Application)
            .filter(Application.job_id == job_id, Application.applicant_id == user_id)
            .first()
        )
        if existing:
            return {"success": False, "error": "You already applied to this job"}

        application = Application(
            job_id=job_id,
            applicant_id=user_id,
            cover_letter=cover_letter,
            status="pending",
        )
        db.add(application)
        db.commit()
        db.refresh(application)

        data = _application_to_dict(application)
        _broadcast("applications", "APPLICATION_CHANGED", data, "created")
        return {"success": True, "data": data}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()


@server_action()
async def get_my_applications(request: Request):
    """Get all applications made by the current job seeker."""
    user_id = get_user_id_from_request(request)
    if user_id is None:
        return {"success": False, "error": "Not authenticated"}

    db = get_session()
    try:
        apps = (
            db.query(Application)
            .filter(Application.applicant_id == user_id)
            .order_by(Application.created_at.desc())
            .all()
        )
        return {"success": True, "data": [_application_to_dict(a) for a in apps]}
    finally:
        db.close()


@server_action()
async def get_job_applications(request: Request, job_id: int = 0):
    """Get all applications for a specific job (employer only)."""
    user_id = get_user_id_from_request(request)
    if user_id is None:
        return {"success": False, "error": "Not authenticated"}

    db = get_session()
    try:
        job = db.query(Job).filter(Job.id == job_id, Job.employer_id == user_id).first()
        if not job:
            return {"success": False, "error": "Job not found or not yours"}

        apps = (
            db.query(Application)
            .filter(Application.job_id == job_id)
            .order_by(Application.created_at.desc())
            .all()
        )
        return {"success": True, "data": [_application_to_dict(a) for a in apps]}
    finally:
        db.close()


@server_action()
async def update_application_status(request: Request, application_id: int = 0, status: str = "pending"):
    """Update an application's status (employer only)."""
    user_id = get_user_id_from_request(request)
    if user_id is None:
        return {"success": False, "error": "Not authenticated"}
    if status not in ("pending", "accepted", "rejected"):
        return {"success": False, "error": "Invalid status"}

    db = get_session()
    try:
        app = db.query(Application).filter(Application.id == application_id).first()
        if not app:
            return {"success": False, "error": "Application not found"}

        job = db.query(Job).filter(Job.id == app.job_id, Job.employer_id == user_id).first()
        if not job:
            return {"success": False, "error": "Not authorized"}

        app.status = status
        db.commit()
        db.refresh(app)

        data = _application_to_dict(app)
        _broadcast("applications", "APPLICATION_CHANGED", data, "updated")
        return {"success": True, "data": data}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()
