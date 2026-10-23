"""
NextPy Authentication - JWT, Session, and Password support
"""

import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Iterable
from functools import wraps
from fastapi import HTTPException, Request, Response
from nextpy.config import settings


# ---------------------------------------------------------------------------
# Password hashing (HMAC-SHA256 with random salt — no bcrypt dependency)
# ---------------------------------------------------------------------------
_HASH_ITERATIONS = 260_000


def hash_password(password: str) -> str:
    """Hash a password with a random salt.  Returns ``salt$hash``."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), _HASH_ITERATIONS)
    return f"{salt}${dk.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a ``salt$hash`` string."""
    try:
        salt, expected_hex = hashed.split("$", 1)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), _HASH_ITERATIONS)
        return secrets.compare_digest(dk.hex(), expected_hex)
    except Exception:
        return False


class AuthManager:
    """Handle JWT and session authentication"""
    
    @staticmethod
    def create_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT token"""
        if expires_delta is None:
            expires_delta = timedelta(hours=settings.jwt_expiration_hours)
        
        expire = datetime.utcnow() + expires_delta
        payload = {"user_id": user_id, "exp": expire}
        
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    
    @staticmethod
    def verify_token(token: str) -> Optional[int]:
        """Verify JWT token and return user_id"""
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            user_id = payload.get("user_id")
            if user_id is None:
                return None
            return user_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    @staticmethod
    def get_token_from_request(request: Request) -> Optional[str]:
        """Extract token from Authorization header"""
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:]
        return None


def require_auth(func):
    """Decorator to require a Bearer token."""
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        token = AuthManager.get_token_from_request(request)
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")

        user_id = AuthManager.verify_token(token)
        request.state.user_id = user_id
        return await func(request, *args, **kwargs)

    return wrapper


def get_user_from_request(request: Request, db=None):
    """Resolve the current user from a session cookie or Bearer token.

    Returns the ORM ``User`` instance or ``None``.  The database session is
    closed automatically unless the caller supplies one.
    """
    from nextpy.db import User, get_session as _db_session

    owns_session = db is None
    db = db or _db_session()
    try:
        user_id = get_user_id_from_request(request)
        if user_id is None:
            token = AuthManager.get_token_from_request(request)
            if token:
                user_id = AuthManager.verify_token(token)
        if user_id is None:
            return None
        return db.get(User, user_id)
    finally:
        if owns_session:
            db.close()


def current_user_id(request: Request) -> Optional[int]:
    """Return the authenticated user id from cookie or Bearer token."""
    user_id = get_user_id_from_request(request)
    if user_id is not None:
        return user_id
    token = AuthManager.get_token_from_request(request)
    if not token:
        return None
    return AuthManager.verify_token(token)


def require_user(func):
    """Decorator for server actions/API handlers that require a user.

    Injects ``request.state.user`` and ``request.state.user_id``.  Works with
    both sync and async functions.
    """
    if _is_async_callable(func):
        @wraps(func)
        async def async_wrapper(request: Request, *args, **kwargs):
            user = get_user_from_request(request)
            if user is None:
                raise HTTPException(status_code=401, detail="Authentication required")
            request.state.user = user
            request.state.user_id = user.id
            return await func(request, *args, **kwargs)
        return async_wrapper

    @wraps(func)
    def sync_wrapper(request: Request, *args, **kwargs):
        user = get_user_from_request(request)
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication required")
        request.state.user = user
        request.state.user_id = user.id
        return func(request, *args, **kwargs)
    return sync_wrapper


def require_role(*roles: str):
    """Require the authenticated user to have one of ``roles``."""
    allowed = {str(role) for role in roles}

    def decorator(func):
        if _is_async_callable(func):
            @wraps(func)
            async def async_wrapper(request: Request, *args, **kwargs):
                user = get_user_from_request(request)
                if user is None:
                    raise HTTPException(status_code=401, detail="Authentication required")
                if getattr(user, "role", None) not in allowed:
                    raise HTTPException(status_code=403, detail="Insufficient permissions")
                request.state.user = user
                request.state.user_id = user.id
                return await func(request, *args, **kwargs)
            return async_wrapper

        @wraps(func)
        def sync_wrapper(request: Request, *args, **kwargs):
            user = get_user_from_request(request)
            if user is None:
                raise HTTPException(status_code=401, detail="Authentication required")
            if getattr(user, "role", None) not in allowed:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            request.state.user = user
            request.state.user_id = user.id
            return func(request, *args, **kwargs)
        return sync_wrapper

    return decorator


def _is_async_callable(func) -> bool:
    import inspect
    return inspect.iscoroutinefunction(func)


# Sessions are persisted in the database so they survive process restarts
# and are shared by every worker.  In-memory sessions were convenient for a
# demo but log every user out whenever the server restarts.

def create_session(user_id: int) -> str:
    """Create a persistent server-side session and return its id."""
    import uuid
    from nextpy.db import get_session as _db_session, UserSession

    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    db = _db_session()
    try:
        # Opportunistic cleanup keeps the table from growing forever.
        db.query(UserSession).filter(UserSession.expires_at <= now).delete(
            synchronize_session=False
        )
        db.add(UserSession(
            id=session_id,
            user_id=user_id,
            created_at=now,
            expires_at=now + timedelta(hours=24),
        ))
        db.commit()
    finally:
        db.close()
    return session_id


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Look up a session, returning None when missing or expired."""
    if not session_id:
        return None

    from nextpy.db import get_session as _db_session, UserSession

    db = _db_session()
    try:
        row = db.query(UserSession).filter(UserSession.id == session_id).first()
        if row is None:
            return None
        if row.expires_at <= datetime.utcnow():
            db.delete(row)
            db.commit()
            return None
        return {
            "user_id": row.user_id,
            "created_at": row.created_at,
            "expires_at": row.expires_at,
        }
    finally:
        db.close()


def delete_session(session_id: str) -> bool:
    """Delete a session from persistent storage."""
    if not session_id:
        return False

    from nextpy.db import get_session as _db_session, UserSession

    db = _db_session()
    try:
        deleted = db.query(UserSession).filter(
            UserSession.id == session_id
        ).delete(synchronize_session=False)
        db.commit()
        return bool(deleted)
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Cookie-based session helpers (for server actions / API routes)
# ---------------------------------------------------------------------------

COOKIE_NAME = "nextpy_session"
COOKIE_MAX_AGE = 86400  # 24 hours


def set_session_cookie(response: Response, user_id: int, secure: bool = False) -> str:
    """Create a session and set it as an HTTP cookie on *response*."""
    session_id = create_session(user_id)
    response.set_cookie(
        COOKIE_NAME,
        session_id,
        max_age=COOKIE_MAX_AGE,
        path="/",
        httponly=True,
        secure=secure,
        samesite="lax",
    )
    return session_id


def get_user_id_from_request(request: Request) -> Optional[int]:
    """Extract the authenticated user-id from the session cookie.

    Returns ``None`` when not authenticated.
    """
    session_id = request.cookies.get(COOKIE_NAME)
    if not session_id:
        return None
    sess = get_session(session_id)
    if sess is None:
        return None
    return sess.get("user_id")


def clear_session_cookie(response: Response, session_id: str, secure: bool = False) -> None:
    """Delete the session cookie and the server-side session."""
    delete_session(session_id)
    response.delete_cookie(COOKIE_NAME, path="/", secure=secure, samesite="lax")
