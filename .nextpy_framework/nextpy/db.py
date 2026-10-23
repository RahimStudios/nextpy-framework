"""
NextPy Database Layer
Support for SQLite, PostgreSQL, MySQL with SQLAlchemy ORM
"""

import os
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Type

from sqlalchemy import create_engine, func, or_, ForeignKey
from sqlalchemy.orm import (
    Session,
    declarative_base,
    joinedload,
    relationship,
    selectinload,
    sessionmaker,
)

Base = declarative_base()
Model = Base


class DatabaseConfig:
    """Database configuration manager"""
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv("DATABASE_URL", "sqlite:///./nextpy.db")
        self.echo = os.getenv("DB_ECHO", "false").lower() == "true"
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "5"))
        self.max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "10"))
        
    def get_engine(self):
        """Get SQLAlchemy engine"""
        if self.database_url.startswith("sqlite"):
            return create_engine(
                self.database_url,
                echo=self.echo,
                connect_args={"check_same_thread": False}
            )
        else:
            return create_engine(
                self.database_url,
                echo=self.echo,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_pre_ping=True
            )


class Database:
    """Database manager with connection pooling"""
    
    def __init__(self, database_url: Optional[str] = None):
        self.config = DatabaseConfig(database_url)
        self.engine = self.config.get_engine()
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)
    
    def drop_tables(self):
        """Drop all tables (development only)"""
        Base.metadata.drop_all(self.engine)
    
    def close(self):
        """Close connection pool"""
        self.engine.dispose() 


# Global database instance
_db: Optional[Database] = None


def init_db(database_url: Optional[str] = None) -> Database:
    """Initialize global database instance"""
    global _db
    _db = Database(database_url)
    _db.create_tables()
    return _db


def get_db() -> Database:
    """Get global database instance"""
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db


def get_session() -> Session:
    """Get database session"""
    return get_db().get_session()


def session() -> Session:
    """Return a database session using the native NextPy API name."""
    return get_session()


# Models example
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    full_name = Column(String(255))
    hashed_password = Column(String(255))
    role = Column(String(50), default="job_seeker")  # job_seeker | employer
    bio = Column(Text, default="")
    company_name = Column(String(255), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSession(Base):
    """Persistent server-side login session.

    Stored in the database (instead of process memory) so sessions survive
    server restarts and work across multiple workers.
    """
    __tablename__ = "user_sessions"

    id = Column(String(64), primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)


class Post(Base):
    """Blog post model"""
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    slug = Column(String(255), unique=True, index=True)
    content = Column(Text)
    excerpt = Column(String(500))
    author_id = Column(Integer, index=True)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Todo(Base):
    """Persistent todo item shared by the API, PSX pages, and admin."""
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)




class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    location = Column(String(200))
    description = Column(Text, nullable=False)
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    job_type = Column(String(50), default="full_time")  # full_time | part_time | contract | internship
    experience_level = Column(String(50), default="mid")  # entry | mid | senior | lead
    employer_id = Column(Integer, ForeignKey("users.id"), index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    applications = relationship(
        "Application", back_populates="job", cascade="all, delete-orphan"
    )
    employer = relationship("User", foreign_keys=[employer_id])


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
    applicant_id = Column(Integer, ForeignKey("users.id"), index=True)
    cover_letter = Column(Text, default="")
    resume_url = Column(String(500), default="")
    status = Column(String(50), default="pending", index=True)  # pending | accepted | rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="applications", foreign_keys=[job_id], lazy="joined")
    applicant = relationship("User", foreign_keys=[applicant_id], lazy="joined")


# ---------------------------------------------------------------------------
# Generic query / CRUD helpers
# ---------------------------------------------------------------------------

@dataclass
class Page:
    """Serializable pagination envelope."""

    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool

    def to_dict(self, include_items: bool = False) -> Dict[str, Any]:
        data = {
            "total": self.total,
            "page": self.page,
            "per_page": self.per_page,
            "pages": self.pages,
            "has_next": self.has_next,
            "has_prev": self.has_prev,
        }
        if include_items:
            data["items"] = self.items
        return data


def transaction() -> Session:
    """Context manager that commits on success and rolls back on error.

    Usage::

        with transaction() as db:
            db.add(record)
    """
    @contextmanager
    def _transaction():
        db = get_session()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    return _transaction()


def paginate(
    query: Any,
    page: int = 1,
    per_page: int = 20,
    max_per_page: int = 100,
) -> Page:
    """Paginate a SQLAlchemy query without loading the full result set."""
    page = max(1, int(page or 1))
    per_page = max(1, min(int(per_page or 20), max_per_page))
    total = int(query.order_by(None).count())
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    pages = (total + per_page - 1) // per_page if total else 0
    return Page(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )


def get_or_none(db: Session, model: Type[Any], ident: Any) -> Optional[Any]:
    """Fetch a row by primary key or return ``None``."""
    return db.get(model, ident)


def get_or_404(db: Session, model: Type[Any], ident: Any, name: str = "Record") -> Any:
    """Fetch a row by primary key or raise ``LookupError``."""
    obj = db.get(model, ident)
    if obj is None:
        raise LookupError(f"{name} not found")
    return obj


def batch_get(
    db: Session,
    model: Type[Any],
    ids: Iterable[Any],
    key: str = "id",
) -> Dict[Any, Any]:
    """Load many rows in one query and return a mapping keyed by ``key``."""
    values = [value for value in dict.fromkeys(ids) if value is not None]
    if not values:
        return {}
    column = getattr(model, key)
    rows = db.query(model).filter(column.in_(values)).all()
    return {getattr(row, key): row for row in rows}


def apply_filters(
    query: Any,
    model: Type[Any],
    filters: Optional[Dict[str, Any]] = None,
    *,
    allowed: Optional[Sequence[str]] = None,
    search: Optional[str] = None,
    search_fields: Sequence[str] = (),
) -> Any:
    """Apply whitelisted equality/IN filters and a safe ILIKE search."""
    filters = filters or {}
    allowed_set = set(allowed) if allowed is not None else None
    for field, value in filters.items():
        if value in (None, "", []):
            continue
        if allowed_set is not None and field not in allowed_set:
            continue
        if not hasattr(model, field):
            continue
        column = getattr(model, field)
        if isinstance(value, (list, tuple, set)):
            query = query.filter(column.in_(list(value)))
        else:
            query = query.filter(column == value)

    if search and search_fields:
        term = f"%{search.strip()}%"
        clauses = [getattr(model, field).ilike(term) for field in search_fields if hasattr(model, field)]
        if clauses:
            query = query.filter(or_(*clauses))
    return query


def eager_load(query: Any, *paths: Any) -> Any:
    """Eager-load relationships using ``selectinload``."""
    if paths:
        query = query.options(*(selectinload(path) for path in paths))
    return query


def serialize_model(
    obj: Any,
    fields: Optional[Sequence[str]] = None,
    exclude: Sequence[str] = (),
) -> Dict[str, Any]:
    """Serialize a SQLAlchemy model's columns to plain Python values."""
    exclude_set = set(exclude)
    columns = obj.__table__.columns
    result: Dict[str, Any] = {}
    for column in columns:
        name = column.name
        if fields is not None and name not in fields:
            continue
        if name in exclude_set:
            continue
        value = getattr(obj, name, None)
        if hasattr(value, "isoformat"):
            value = value.isoformat()
        result[name] = value
    return result


def count_by(
    db: Session,
    model: Type[Any],
    group_field: str,
    filters: Optional[Dict[str, Any]] = None,
) -> Dict[Any, int]:
    """Return counts grouped by one column, avoiding per-row count queries."""
    column = getattr(model, group_field)
    query = db.query(column, func.count()).group_by(column)
    query = apply_filters(query, model, filters)
    return {key: int(count) for key, count in query.all()}
