"""
Small, protected SQLAlchemy admin site for NextPy applications.
Enhanced with Django-like features and a modern UI.
"""

import os
from datetime import date, datetime
from decimal import Decimal
from html import escape
from typing import Any, Callable, Dict, Iterable, List, Optional, Type, Union

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import Boolean, Date, DateTime, Float, Integer, Numeric, Text, inspect, or_, select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeMeta, Session

from .db import get_session


# ----------------------------------------------------------------------
# Optional history model – define it in your app if you want logging.
# You can also use your own custom history model.
# ----------------------------------------------------------------------
class AdminLog:
    """Example history model. Replace with your own if desired."""
    id = None  # Placeholder – actual model should be defined by developer
    # ... you can define your own AdminLog model with fields:
    # id, user, action (created/changed/deleted), model, object_id, object_repr, change_message, timestamp
    pass


class AdminSite:
    """Register SQLAlchemy models and expose a Django-style admin."""

    def __init__(self, title: str = "NextPy Admin"):
        self.title = title
        self.models: Dict[str, Type[Any]] = {}
        self.model_options: Dict[str, Dict[str, Any]] = {}
        self.security = HTTPBasic(auto_error=False)
        self.log_model: Optional[Type[Any]] = None  # If set, history will be recorded
        self.template_override: Dict[str, str] = {}  # model -> HTML file path

    def register(
        self,
        model: Type[Any],
        name: Optional[str] = None,
        *,
        list_display: Optional[List[str]] = None,
        search_fields: Optional[List[str]] = None,
        list_filter: Optional[List[str]] = None,
        actions: Optional[List[Callable]] = None,
        inlines: Optional[List[Type[Any]]] = None,
        form_fields: Optional[Dict[str, Dict[str, Any]]] = None,
        template: Optional[str] = None,
    ) -> Type[Any]:
        """Register a model with optional admin configuration."""
        if not isinstance(model, DeclarativeMeta):
            raise TypeError("Admin models must be SQLAlchemy declarative models")
        model_name = name or model.__name__.lower()
        self.models[model_name] = model
        self.model_options[model_name] = {
            "list_display": list_display or [column.key for column in inspect(model).columns],
            "search_fields": search_fields or [],
            "list_filter": list_filter or [],
            "actions": actions or [],
            "inlines": inlines or [],
            "form_fields": form_fields or {},
            "template": template,
        }
        return model

    def unregister(self, model_or_name: Any) -> None:
        name = model_or_name if isinstance(model_or_name, str) else model_or_name.__name__.lower()
        self.models.pop(name, None)
        self.model_options.pop(name, None)

    def _authenticate(self, credentials: Optional[HTTPBasicCredentials]) -> None:
        """Authenticate an admin using env credentials or a DB superuser."""
        import secrets

        env_username = os.getenv("NEXTPY_ADMIN_USERNAME")
        env_password = os.getenv("NEXTPY_ADMIN_PASSWORD")
        env_configured = bool(env_username and env_password)

        if credentials:
            if env_configured:
                username_ok = secrets.compare_digest(credentials.username, env_username)
                password_ok = secrets.compare_digest(credentials.password, env_password)
                if username_ok and password_ok:
                    return

            try:
                from .auth import verify_password
                from .db import User

                db = get_session()
                try:
                    user = (
                        db.query(User)
                        .filter(
                            or_(
                                User.username == credentials.username,
                                User.email == credentials.username,
                            )
                        )
                        .first()
                    )
                    if (
                        user
                        and getattr(user, "is_active", True)
                        and (user.role or "").lower() in {"superuser", "admin", "staff"}
                        and user.hashed_password
                        and verify_password(credentials.password, user.hashed_password)
                    ):
                        return
                finally:
                    db.close()
            except Exception:
                pass

        if not credentials and not env_configured:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "No admin credentials configured. Run "
                    "'nextpy createsuperuser' or set NEXTPY_ADMIN_USERNAME "
                    "and NEXTPY_ADMIN_PASSWORD."
                ),
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication required",
            headers={"WWW-Authenticate": "Basic"},
        )

    def _model(self, name: str) -> Type[Any]:
        model = self.models.get(name)
        if model is None:
            raise HTTPException(status_code=404, detail="Unknown admin model")
        return model

    @staticmethod
    def _columns(model: Type[Any]) -> list[str]:
        return [column.key for column in inspect(model).columns]

    @staticmethod
    def _serialize(value: Any) -> Any:
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, Decimal):
            return str(value)
        return value

    def _serialize_row(self, row: Any, columns: Iterable[str]) -> Dict[str, Any]:
        return {column: self._serialize(getattr(row, column)) for column in columns}

    @staticmethod
    def _query_int(request: Request, name: str, default: int, minimum: int, maximum: int) -> int:
        """Read a bounded integer query parameter safely."""
        try:
            value = int(request.query_params.get(name, str(default)))
        except (TypeError, ValueError):
            value = default
        return min(max(value, minimum), maximum)

    @staticmethod
    def _editable_columns(model: Type[Any]) -> list[Any]:
        return [
            column for column in inspect(model).columns
            if not column.primary_key and column.default is None and column.server_default is None
        ]

    @staticmethod
    def _coerce_value(column: Any, value: Any) -> Any:
        if value is None or value == "":
            return None
        column_type = column.type
        if isinstance(column_type, Boolean):
            if isinstance(value, bool):
                return value
            normalized = str(value).strip().lower()
            if normalized in {"1", "true", "yes", "on"}:
                return True
            if normalized in {"0", "false", "no", "off", ""}:
                return False
            raise ValueError(f"{column.key} must be true or false")
        if isinstance(column_type, Integer):
            return int(value)
        if isinstance(column_type, (Float, Numeric)):
            return float(value)
        if isinstance(column_type, DateTime):
            return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if isinstance(column_type, Date):
            return date.fromisoformat(str(value))
        if isinstance(column_type, (Text,)):
            return str(value)
        return value

    # ------------------------------------------------------------------
    # Logging / History
    # ------------------------------------------------------------------
    def set_log_model(self, log_model: Type[Any]) -> None:
        """Define the model used for history logging."""
        self.log_model = log_model

    def _log_action(
        self,
        session: Session,
        user: Optional[str],
        action: str,
        model_name: str,
        object_id: Any,
        object_repr: str,
        change_message: str = "",
    ) -> None:
        if not self.log_model:
            return
        try:
            log_entry = self.log_model(
                user=user,
                action=action,
                model=model_name,
                object_id=str(object_id),
                object_repr=object_repr,
                change_message=change_message,
                timestamp=datetime.utcnow(),
            )
            session.add(log_entry)
        except Exception:
            # Logging should never break the main operation
            pass

    # ------------------------------------------------------------------
    # UI Helpers
    # ------------------------------------------------------------------
    def _sidebar_html(self, active_model: Optional[str] = None) -> str:
        links = []
        for name in sorted(self.models):
            active_class = ' class="active"' if name == active_model else ""
            icon = name[0].upper()
            links.append(
                f'<a href="/admin/{escape(name)}"{active_class}>'
                f'<span class="model-icon">{escape(icon)}</span>'
                f'<span>{escape(name)}</span>'
                f'</a>'
            )
        return f"""
        <aside class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <a href="/admin" class="brand">
                    <span class="logo">N</span>
                    <span>{escape(self.title)}</span>
                </a>
                <button class="sidebar-toggle" onclick="toggleSidebar()" aria-label="Toggle navigation">☰</button>
            </div>
            <nav>
                {''.join(links)}
            </nav>
        </aside>
        """

    def _topbar_html(self, page_title: str) -> str:
        return f"""
        <header class="topbar">
            <h1>{escape(page_title)}</h1>
        </header>
        """

    def _page(self, heading: str, body: str, active_model: Optional[str] = None) -> str:
        # Template override (if specified)
        if active_model and self.model_options.get(active_model, {}).get("template"):
            try:
                with open(self.model_options[active_model]["template"], "r") as f:
                    template = f.read()
                return template.format(
                    title=self.title,
                    heading=heading,
                    body=body,
                    sidebar=self._sidebar_html(active_model),
                    topbar=self._topbar_html(heading),
                )
            except Exception:
                pass  # fall through to default

        return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(heading)} | {escape(self.title)}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #f8fafc;
            --surface: #ffffff;
            --text: #0f172a;
            --text-secondary: #475569;
            --border: #e2e8f0;
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --danger: #dc2626;
            --danger-hover: #b91c1c;
            --success: #16a34a;
            --warning: #d97706;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
            --radius: 0.5rem;
            --transition: all 0.2s ease;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.5;
            display: flex;
            min-height: 100vh;
        }}
        a {{ color: var(--primary); text-decoration: none; transition: var(--transition); }}
        a:hover {{ color: var(--primary-hover); }}

        /* Sidebar */
        .sidebar {{
            width: 260px;
            background: var(--surface);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            position: fixed;
            top: 0; left: 0; bottom: 0;
            z-index: 100;
            transition: transform 0.3s ease;
        }}
        .sidebar-header {{
            padding: 1.25rem 1rem;
            border-bottom: 1px solid var(--border);
            display: flex; align-items: center; justify-content: space-between;
        }}
        .brand {{ display: flex; align-items: center; gap: 0.75rem; font-weight: 600; color: var(--text); }}
        .brand .logo {{
            display: inline-flex; align-items: center; justify-content: center;
            width: 32px; height: 32px;
            background: var(--primary); color: white; border-radius: 8px;
            font-size: 1.2rem; font-weight: 700;
        }}
        .sidebar nav {{ padding: 0.5rem; overflow-y: auto; flex: 1; }}
        .sidebar nav a {{
            display: flex; align-items: center; gap: 0.75rem;
            padding: 0.625rem 0.75rem; border-radius: 8px;
            color: var(--text-secondary); font-weight: 500; margin-bottom: 2px;
            transition: var(--transition);
        }}
        .sidebar nav a:hover {{ background: #f1f5f9; color: var(--text); }}
        .sidebar nav a.active {{ background: #eff6ff; color: var(--primary); font-weight: 600; }}
        .model-icon {{
            display: inline-flex; align-items: center; justify-content: center;
            width: 28px; height: 28px; border-radius: 6px;
            background: #e2e8f0; color: var(--text-secondary);
            font-size: 0.9rem; font-weight: 600; flex-shrink: 0;
        }}
        .sidebar-toggle {{ display: none; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-secondary); }}

        /* Main */
        .main {{ flex: 1; margin-left: 260px; padding: 1.5rem 2rem; transition: margin-left 0.3s ease; }}
        .topbar {{ margin-bottom: 1.5rem; }}
        .topbar h1 {{ font-size: 1.8rem; font-weight: 700; letter-spacing: -0.025em; }}

        /* Cards */
        .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1rem; margin-top: 1.5rem; }}
        .card {{
            background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
            padding: 1.5rem; box-shadow: var(--shadow-sm); transition: var(--transition); cursor: pointer;
        }}
        .card:hover {{ box-shadow: var(--shadow-lg); transform: translateY(-4px); border-color: #cbd5e1; }}
        .card a {{ display: block; color: var(--text); font-weight: 600; font-size: 1.1rem; }}
        .card .model-icon {{ width: 40px; height: 40px; font-size: 1.2rem; margin-bottom: 0.75rem; background: #e0e7ff; color: var(--primary); }}

        /* Buttons */
        .btn {{
            display: inline-flex; align-items: center; gap: 0.5rem;
            padding: 0.5rem 1rem; border-radius: 6px; font-weight: 500;
            border: 1px solid transparent; cursor: pointer; transition: var(--transition);
            text-align: center; font-size: 0.9rem; background: none; color: var(--text);
        }}
        .btn-primary {{ background: var(--primary); color: white; }}
        .btn-primary:hover {{ background: var(--primary-hover); color: white; }}
        .btn-danger {{ background: var(--danger); color: white; }}
        .btn-danger:hover {{ background: var(--danger-hover); color: white; }}
        .btn-outline {{ background: transparent; border-color: var(--border); color: var(--text); }}
        .btn-outline:hover {{ background: #f1f5f9; border-color: #cbd5e1; }}
        .btn-sm {{ padding: 0.25rem 0.5rem; font-size: 0.8rem; }}

        /* Forms */
        form {{ margin: 1rem 0; }}
        .form-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }}
        label {{ display: block; margin-bottom: 1rem; font-weight: 500; color: var(--text-secondary); }}
        input, textarea, select {{
            width: 100%; padding: 0.5rem 0.75rem; margin-top: 0.25rem;
            border: 1px solid var(--border); border-radius: 6px;
            background: var(--surface); color: var(--text); font-size: 0.9rem;
            transition: var(--transition);
        }}
        input:focus, textarea:focus, select:focus {{
            outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }}
        input[type="checkbox"] {{ width: auto; margin-right: 0.5rem; }}
        .form-actions {{ display: flex; gap: 0.5rem; margin-top: 1.5rem; }}

        /* Tables */
        .table-container {{
            background: var(--surface); border: 1px solid var(--border);
            border-radius: var(--radius); box-shadow: var(--shadow-sm);
            overflow: auto; margin-top: 1rem;
        }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
        th, td {{ padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid var(--border); }}
        th {{
            background: #f8fafc; font-weight: 600; color: var(--text-secondary);
            text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em;
            position: sticky; top: 0; user-select: none; cursor: pointer;
            transition: var(--transition);
        }}
        th:hover {{ background: #f1f5f9; }}
        th.sortable::after {{ content: '↕'; margin-left: 0.5rem; opacity: 0.5; }}
        th.sort-asc::after {{ content: '↑'; opacity: 1; }}
        th.sort-desc::after {{ content: '↓'; opacity: 1; }}
        tr:hover td {{ background: #f8fafc; }}
        .actions-cell {{ white-space: nowrap; }}
        .actions-cell a, .actions-cell form {{ display: inline-block; margin-right: 0.25rem; }}
        .bulk-actions {{ display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }}

        /* Pagination */
        .pagination {{ display: flex; justify-content: center; gap: 0.5rem; margin: 1rem 0; }}
        .pagination button {{
            padding: 0.5rem 0.75rem; border: 1px solid var(--border); border-radius: 6px;
            background: var(--surface); cursor: pointer; transition: var(--transition);
        }}
        .pagination button:hover {{ background: #f1f5f9; }}
        .pagination button.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
        .pagination button:disabled {{ opacity: 0.5; cursor: not-allowed; }}

        /* Modal */
        .modal-overlay {{
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.4); backdrop-filter: blur(2px);
            display: flex; align-items: center; justify-content: center;
            z-index: 1000; opacity: 0; pointer-events: none; transition: opacity 0.2s ease;
        }}
        .modal-overlay.active {{ opacity: 1; pointer-events: all; }}
        .modal {{
            background: white; padding: 2rem; border-radius: 8px; box-shadow: var(--shadow-lg);
            max-width: 400px; width: 90%; text-align: center; transform: scale(0.95);
            transition: transform 0.2s ease;
        }}
        .modal-overlay.active .modal {{ transform: scale(1); }}
        .modal h2 {{ margin-bottom: 1rem; }}
        .modal .form-actions {{ justify-content: center; }}

        /* Success banner */
        .success-banner {{
            background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534;
            padding: 0.75rem 1rem; border-radius: 6px; margin-bottom: 1rem;
            display: flex; align-items: center; gap: 0.5rem;
        }}
        .success-banner svg {{ width: 20px; height: 20px; flex-shrink: 0; }}

        /* Responsive */
        @media (max-width: 768px) {{
            .sidebar {{ transform: translateX(-100%); }}
            .sidebar.open {{ transform: translateX(0); }}
            .sidebar-toggle {{ display: block; }}
            .main {{ margin-left: 0; padding: 1rem; }}
            .card-grid {{ grid-template-columns: 1fr; }}
            .form-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    {self._sidebar_html(active_model)}
    <div class="main">
        {self._topbar_html(heading)}
        <div class="content">
            {body}
        </div>
    </div>

    <!-- Modal -->
    <div class="modal-overlay" id="confirm-modal">
        <div class="modal">
            <h2>Confirm Deletion</h2>
            <p>Are you sure you want to delete this record? This action cannot be undone.</p>
            <div class="form-actions">
                <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
                <button class="btn btn-danger" id="confirm-delete-btn">Delete</button>
            </div>
        </div>
    </div>

    <script>
        // Sidebar toggle
        function toggleSidebar() {{ document.getElementById('sidebar').classList.toggle('open'); }}

        // Modal for delete
        let deleteForm = null;
        function confirmDelete(event, form) {{
            event.preventDefault();
            deleteForm = form;
            document.getElementById('confirm-modal').classList.add('active');
        }}
        document.getElementById('confirm-delete-btn').addEventListener('click', function() {{
            if (deleteForm) deleteForm.submit();
            closeModal();
        }});
        function closeModal() {{ document.getElementById('confirm-modal').classList.remove('active'); }}
        document.getElementById('confirm-modal').addEventListener('click', function(e) {{
            if (e.target === this) closeModal();
        }});

        // Bulk select all
        document.addEventListener('change', function(e) {{
            if (e.target.id === 'select-all') {{
                document.querySelectorAll('input[name="selected_ids"]').forEach(cb => cb.checked = e.target.checked);
            }}
        }});
    </script>
</body>
</html>"""

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------
    def _dashboard(self) -> str:
        cards = []
        for name in sorted(self.models):
            icon = name[0].upper()
            cards.append(
                f'<div class="card">'
                f'<a href="/admin/{escape(name)}">'
                f'<span class="model-icon">{escape(icon)}</span>'
                f'{escape(name)}'
                f'</a>'
                f'</div>'
            )
        body = f"""
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">Manage your website's data and users</p>
        <div class="card-grid">
            {''.join(cards) if cards else '<p>No models registered yet.</p>'}
        </div>
        """
        return self._page("Dashboard", body)

    # ------------------------------------------------------------------
    # Router and Handlers
    # ------------------------------------------------------------------
    def router(self, prefix: str = "/admin") -> APIRouter:
        router = APIRouter(prefix=prefix)
        auth = Depends(self.security)

        @router.get("", response_class=HTMLResponse)
        @router.get("/", response_class=HTMLResponse)
        async def dashboard(credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            return self._dashboard()

        # --------------------------------
        # List view with pagination, filtering, searching, sorting, bulk actions
        # --------------------------------
        @router.get("/{model_name}", response_class=HTMLResponse)
        async def model_list(
            model_name: str,
            request: Request,
            credentials: Optional[HTTPBasicCredentials] = auth,
        ):
            self._authenticate(credentials)
            model = self._model(model_name)
            options = self.model_options.get(model_name, {})
            columns = options.get("list_display", self._columns(model))
            search_fields = options.get("search_fields", [])
            filter_fields = options.get("list_filter", [])
            actions = options.get("actions", [])

            # Query parameters
            page = self._query_int(request, "page", 1, 1, 10_000_000)
            per_page = self._query_int(request, "per_page", 25, 1, 100)
            q = request.query_params.get("q", "").strip()
            sort = request.query_params.get("sort", "")
            order = request.query_params.get("order", "asc")

            with get_session() as session:
                query = select(model)

                # Search
                if q and search_fields:
                    conditions = []
                    for field in search_fields:
                        column = getattr(model, field, None)
                        if column is not None:
                            conditions.append(column.ilike(f"%{q}%"))
                    if conditions:
                        from sqlalchemy import or_
                        query = query.where(or_(*conditions))

                # Filtering
                for field in filter_fields:
                    value = request.query_params.get(field)
                    if value:
                        column = getattr(model, field)
                        if column is not None:
                            query = query.where(column == value)

                # Sorting
                if sort and sort in columns:
                    column = getattr(model, sort)
                    if order == "desc":
                        query = query.order_by(column.desc())
                    else:
                        query = query.order_by(column.asc())

                # Count total for pagination
                total = int(session.execute(select(func.count()).select_from(query.subquery())).scalar() or 0)

                # Paginate
                query = query.offset((page - 1) * per_page).limit(per_page)
                objects = list(session.scalars(query))

            # Build table
            header = "".join(
                f'<th class="sortable" onclick="window.location.href=\'?sort={escape(col)}&order=' + ('asc' if order == 'desc' else 'desc') + f'&page={page}&q={escape(q)}\';">{escape(col)}</th>'
                for col in columns
            )

            # Add checkbox column for bulk actions
            header = f'<th><input type="checkbox" id="select-all"></th>' + header
            header += '<th>Actions</th>'

            body_rows = ""
            for row in objects:
                row_id = getattr(row, "id", None)
                checkbox = f'<td><input type="checkbox" name="selected_ids" value="{row_id}"></td>'
                cells = ""
                for col in columns:
                    cells += f'<td>{escape(str(self._serialize(getattr(row, col))))}</td>'
                actions_cell = f'''<td class="actions-cell">
                    <a href="/admin/{escape(model_name)}/{row_id}" class="btn btn-outline btn-sm">  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg></a>
                    <a href="/admin/{escape(model_name)}/{row_id}/edit" class="btn btn-outline btn-sm"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg></a>
                    <form method="post" action="/admin/{escape(model_name)}/{row_id}/delete" style="display:inline;" onsubmit="confirmDelete(event, this)">
                        <button type="submit" class="btn btn-danger btn-sm"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg></button>
                    </form>
                </td>'''
                body_rows += f'<tr>{checkbox}{cells}{actions_cell}</tr>'

            if not body_rows:
                body_rows = f'<tr><td colspan="{len(columns)+2}">No records found</td></tr>'

            # Bulk actions form
            bulk_actions_html = ""
            if actions:
                action_options = "".join(f'<option value="{escape(action.__name__)}">{escape(action.__name__)}</option>' for action in actions)
                bulk_actions_html = f"""
                <form method="post" action="/admin/{escape(model_name)}/bulk-action" class="bulk-actions">
                    <select name="action">
                        <option value="">---</option>
                        {action_options}
                    </select>
                    <button type="submit" class="btn btn-outline">Go</button>
                </form>
                """
            # Add default delete action if no custom actions
            if not bulk_actions_html:
                bulk_actions_html = """
                <form method="post" action="/admin/{}/bulk-delete" class="bulk-actions" onsubmit="return confirm('Delete selected items?');">
                    <button type="submit" class="btn btn-danger">Delete selected</button>
                </form>
                """.format(escape(model_name))

            # Pagination
            total_pages = (total + per_page - 1) // per_page
            pagination = ""
            if total_pages > 1:
                pagination = '<div class="pagination">'
                if page > 1:
                    pagination += f'<a href="?page={page-1}&q={escape(q)}&sort={escape(sort)}&order={escape(order)}">‹</a>'
                for p in range(max(1, page-2), min(total_pages, page+2)+1):
                    active = ' active' if p == page else ''
                    pagination += f'<a href="?page={p}&q={escape(q)}&sort={escape(sort)}&order={escape(order)}" class="btn{active}">{p}</a>'
                if page < total_pages:
                    pagination += f'<a href="?page={page+1}&q={escape(q)}&sort={escape(sort)}&order={escape(order)}">›</a>'
                pagination += '</div>'

            # Success banner
            success_msg = request.query_params.get("success", "")
            success_html = ""
            if success_msg:
                success_html = f"""
                <div class="success-banner">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                    {escape(success_msg)}
                </div>
                """

            body = f"""
            {success_html}
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:1rem;">
                <a href="/admin/{escape(model_name)}/new" class="btn btn-primary">+ Add {escape(model_name)}</a>
                <form method="get" class="search-form" style="display:flex; gap:0.5rem; margin:0;">
                    <input type="text" name="q" placeholder="Search..." value="{escape(q)}">
                    <button type="submit" class="btn btn-outline">Search</button>
                </form>
            </div>
            {bulk_actions_html}
            <div class="table-container">
                <table>
                    <thead><tr>{header}</tr></thead>
                    <tbody>{body_rows}</tbody>
                </table>
            </div>
            {pagination}
            """
            return self._page(model_name, body, active_model=model_name)

        # --------------------------------
        # Bulk delete
        # --------------------------------
        @router.post("/{model_name}/bulk-delete")
        async def bulk_delete(model_name: str, request: Request, credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            model = self._model(model_name)
            form_data = await request.form()
            ids = form_data.getlist("selected_ids")
            if not ids:
                return RedirectResponse(url=f"/admin/{model_name}?error=No items selected", status_code=303)
            with get_session() as session:
                session.query(model).filter(model.id.in_(ids)).delete(synchronize_session=False)
                session.commit()
            return RedirectResponse(url=f"/admin/{model_name}?success=Deleted {len(ids)} item(s)", status_code=303)

        # --------------------------------
        # Custom bulk actions
        # --------------------------------
        @router.post("/{model_name}/bulk-action")
        async def bulk_action(model_name: str, request: Request, credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            model = self._model(model_name)
            options = self.model_options.get(model_name, {})
            actions = options.get("actions", [])
            form_data = await request.form()
            action_name = form_data.get("action")
            ids = form_data.getlist("selected_ids")
            if not ids:
                return RedirectResponse(url=f"/admin/{model_name}?error=No items selected", status_code=303)
            action_func = None
            for a in actions:
                if a.__name__ == action_name:
                    action_func = a
                    break
            if not action_func:
                return RedirectResponse(url=f"/admin/{model_name}?error=Invalid action", status_code=303)
            with get_session() as session:
                objects = session.query(model).filter(model.id.in_(ids)).all()
                result = action_func(session, objects)
                session.commit()
            return RedirectResponse(url=f"/admin/{model_name}?success={result or 'Action completed'}", status_code=303)

        # --------------------------------
        # CRUD routes (unchanged from before, but updated with logging)
        # --------------------------------
        @router.get("/{model_name}/new", response_class=HTMLResponse)
        async def new_record_form(model_name: str, credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            model = self._model(model_name)
            fields = []
            editable = self._editable_columns(model)
            for column in editable:
                field_options = self.model_options.get(model_name, {}).get("form_fields", {}).get(column.key, {})
                required = " required" if not column.nullable else ""
                column_type = column.type
                if isinstance(column_type, Boolean):
                    control = f'<input type="checkbox" name="{escape(column.key)}" value="true">'
                elif isinstance(column_type, Text):
                    control = f'<textarea name="{escape(column.key)}"{required}></textarea>'
                elif isinstance(column_type, Integer):
                    control = f'<input type="number" name="{escape(column.key)}"{required}>'
                elif isinstance(column_type, (Float, Numeric)):
                    control = f'<input type="number" step="any" name="{escape(column.key)}"{required}>'
                elif isinstance(column_type, DateTime):
                    control = f'<input type="datetime-local" name="{escape(column.key)}"{required}>'
                elif isinstance(column_type, Date):
                    control = f'<input type="date" name="{escape(column.key)}"{required}>'
                else:
                    control = f'<input type="text" name="{escape(column.key)}"{required}>'
                if "widget" in field_options:
                    # simple widget override: e.g., "textarea"
                    widget = field_options["widget"]
                    if widget == "textarea":
                        control = f'<textarea name="{escape(column.key)}"{required}></textarea>'
                    elif widget == "checkbox":
                        control = f'<input type="checkbox" name="{escape(column.key)}" value="true">'
                fields.append(f'<label>{escape(column.key)}{control}</label>')
            form = "".join(fields) or "<p>This model has no editable fields.</p>"
            body = f"""
            <div style="max-width:800px;">
                <form method="post">
                    <div class="form-grid">
                        {form}
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary">Create</button>
                        <a href="/admin/{escape(model_name)}" class="btn btn-outline">Cancel</a>
                    </div>
                </form>
            </div>
            """
            return self._page(f"Add {model_name}", body, active_model=model_name)

        @router.post("/{model_name}/new", response_class=HTMLResponse)
        async def submit_new_record(model_name: str, request: Request, credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            model = self._model(model_name)
            form_data = await request.form()
            columns = {column.key: column for column in inspect(model).columns if not column.primary_key}
            values = {}
            try:
                for key, column in columns.items():
                    raw_value = form_data.get(key)
                    if isinstance(column.type, Boolean) and raw_value is None:
                        raw_value = False
                    if raw_value is not None:
                        values[key] = self._coerce_value(column, raw_value)
                with get_session() as session:
                    obj = model(**values)
                    session.add(obj)
                    session.flush()
                    if self.log_model:
                        self._log_action(session, None, "created", model_name, obj.id, str(obj), "Created")
                    session.commit()
            except (ValueError, TypeError) as error:
                raise HTTPException(status_code=400, detail=f"Invalid value: {error}") from error
            except SQLAlchemyError as error:
                raise HTTPException(status_code=400, detail=f"Could not save record: {error}") from error
            return RedirectResponse(url=f"/admin/{model_name}?success=Record created", status_code=303)

        # Register the JSON collection route before the integer record route.
        # Otherwise /admin/user/records can be interpreted as record_id="records".
        @router.get("/{model_name}/records")
        async def records(model_name: str, request: Request, credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            model = self._model(model_name)
            columns = self._columns(model)
            limit = self._query_int(request, "limit", 100, 1, 500)
            with get_session() as session:
                rows = list(session.scalars(select(model).limit(limit)))
            return [self._serialize_row(row, columns) for row in rows]

        @router.post("/{model_name}/records")
        async def create_record(model_name: str, request: Request, credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            model = self._model(model_name)
            data = await request.json()
            columns = {column.key: column for column in inspect(model).columns if not column.primary_key}
            try:
                values = {
                    key: self._coerce_value(column, data[key])
                    for key, column in columns.items()
                    if key in data and column.default is None and column.server_default is None
                }
                with get_session() as session:
                    row = model(**values)
                    session.add(row)
                    session.commit()
                    session.refresh(row)
                    return self._serialize_row(row, self._columns(model))
            except (ValueError, TypeError) as error:
                raise HTTPException(status_code=400, detail=f"Invalid value: {error}") from error
            except SQLAlchemyError as error:
                raise HTTPException(status_code=400, detail=f"Could not save record: {error}") from error

        @router.get("/{model_name}/{record_id}", response_class=HTMLResponse)
        async def record_detail(model_name: str, record_id: int, credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            model = self._model(model_name)
            columns = self._columns(model)
            with get_session() as session:
                row = session.get(model, record_id)
            if row is None:
                raise HTTPException(status_code=404, detail="Record not found")
            values = "".join(
                f"<tr><th>{escape(column)}</th><td>{escape(str(self._serialize(getattr(row, column))))}</td></tr>"
                for column in columns
            )
            # History
            history_html = ""
            if self.log_model:
                with get_session() as session:
                    logs = session.query(self.log_model).filter_by(model=model_name, object_id=str(record_id)).order_by(self.log_model.timestamp.desc()).limit(10).all()
                    if logs:
                        history_rows = "".join(
                            f"<tr><td>{escape(log.timestamp)}</td><td>{escape(log.action)}</td><td>{escape(log.change_message)}</td></tr>"
                            for log in logs
                        )
                        history_html = f"""
                        <h2 style="margin-top:2rem;">History</h2>
                        <div class="table-container">
                            <table>
                                <thead><tr><th>Date</th><th>Action</th><th>Change</th></tr></thead>
                                <tbody>{history_rows}</tbody>
                            </table>
                        </div>
                        """
            body = f"""
            <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1rem;">
                <a href="/admin/{escape(model_name)}/{record_id}/edit" class="btn btn-primary">Edit</a>
                <form method="post" action="/admin/{escape(model_name)}/{record_id}/delete" style="display:inline;" onsubmit="confirmDelete(event, this)">
                    <button type="submit" class="btn btn-danger">Delete</button>
                </form>
                <a href="/admin/{escape(model_name)}" class="btn btn-outline">Back to list</a>
            </div>
            <div class="table-container">
                <table>{values}</table>
            </div>
            {history_html}
            """
            return self._page(f"{model_name} #{record_id}", body, active_model=model_name)

        @router.get("/{model_name}/{record_id}/edit", response_class=HTMLResponse)
        async def edit_record_form(model_name: str, record_id: int, credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            model = self._model(model_name)
            with get_session() as session:
                row = session.get(model, record_id)
            if row is None:
                raise HTTPException(status_code=404, detail="Record not found")
            fields = []
            for column in self._editable_columns(model):
                value = getattr(row, column.key)
                required = " required" if not column.nullable else ""
                field_options = self.model_options.get(model_name, {}).get("form_fields", {}).get(column.key, {})
                if isinstance(column.type, Boolean):
                    checked = " checked" if value else ""
                    control = f'<input type="checkbox" name="{escape(column.key)}" value="true"{checked}>'
                elif isinstance(column.type, Text):
                    control = f'<textarea name="{escape(column.key)}"{required}>{escape(str(value or ""))}</textarea>'
                else:
                    input_type = "number" if isinstance(column.type, (Integer, Float, Numeric)) else "text"
                    control = f'<input type="{input_type}" name="{escape(column.key)}" value="{escape(str(value or ""))}"{required}>'
                if "widget" in field_options:
                    widget = field_options["widget"]
                    if widget == "textarea":
                        control = f'<textarea name="{escape(column.key)}"{required}>{escape(str(value or ""))}</textarea>'
                    elif widget == "checkbox":
                        checked = " checked" if value else ""
                        control = f'<input type="checkbox" name="{escape(column.key)}" value="true"{checked}>'
                fields.append(f'<label>{escape(column.key)}{control}</label>')
            body = f"""
            <div style="max-width:800px;">
                <form method="post">
                    <div class="form-grid">
                        {''.join(fields)}
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                        <a href="/admin/{escape(model_name)}/{record_id}" class="btn btn-outline">Cancel</a>
                    </div>
                </form>
            </div>
            """
            return self._page(f"Edit {model_name} #{record_id}", body, active_model=model_name)

        @router.post("/{model_name}/{record_id}/edit", response_class=HTMLResponse)
        async def submit_edit_record(model_name: str, record_id: int, request: Request, credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            model = self._model(model_name)
            form_data = await request.form()
            columns = {column.key: column for column in self._editable_columns(model)}
            try:
                with get_session() as session:
                    row = session.get(model, record_id)
                    if row is None:
                        raise HTTPException(status_code=404, detail="Record not found")
                    changes = []
                    for key, column in columns.items():
                        raw_value = form_data.get(key)
                        if isinstance(column.type, Boolean) and raw_value is None:
                            raw_value = False
                        if raw_value is not None:
                            new_value = self._coerce_value(column, raw_value)
                            old_value = getattr(row, key)
                            if old_value != new_value:
                                setattr(row, key, new_value)
                                changes.append(f"{key}: {old_value} -> {new_value}")
                    if self.log_model and changes:
                        self._log_action(session, None, "changed", model_name, record_id, str(row), ", ".join(changes))
                    session.commit()
            except (ValueError, TypeError) as error:
                raise HTTPException(status_code=400, detail=f"Invalid value: {error}") from error
            except SQLAlchemyError as error:
                raise HTTPException(status_code=400, detail=f"Could not save record: {error}") from error
            return RedirectResponse(url=f"/admin/{model_name}/{record_id}?success=Record updated", status_code=303)

        @router.post("/{model_name}/{record_id}/delete")
        async def delete_record_form(model_name: str, record_id: int, credentials: Optional[HTTPBasicCredentials] = auth):
            self._authenticate(credentials)
            model = self._model(model_name)
            with get_session() as session:
                row = session.get(model, record_id)
                if row is None:
                    raise HTTPException(status_code=404, detail="Record not found")
                if self.log_model:
                    self._log_action(session, None, "deleted", model_name, record_id, str(row), "Deleted")
                session.delete(row)
                session.commit()
            return RedirectResponse(url=f"/admin/{model_name}?success=Record deleted", status_code=303)

        return router

    def mount(self, app: Any, prefix: str = "/admin") -> Any:
        normalized_prefix = "/" + prefix.strip("/")
        app.include_router(self.router(normalized_prefix))

        # Explicit dashboard route (for compatibility)
        registered_paths = {getattr(route, "path", "") for route in app.routes}
        if normalized_prefix not in registered_paths:
            auth = Depends(self.security)

            async def explicit_dashboard(credentials: Optional[HTTPBasicCredentials] = auth):
                self._authenticate(credentials)
                return HTMLResponse(self._dashboard())

            app.add_api_route(
                normalized_prefix,
                explicit_dashboard,
                methods=["GET"],
                response_class=HTMLResponse,
                name="nextpy_admin_dashboard",
            )
        return app


# Default instance
admin = AdminSite()


def register(model: Type[Any], name: Optional[str] = None, **kwargs) -> Type[Any]:
    """Register a model on the default admin site with optional configuration."""
    return admin.register(model, name, **kwargs)