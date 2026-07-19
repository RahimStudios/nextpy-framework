# NextPy Database Integration

NextPy supports multiple databases with SQLAlchemy ORM, environment variable configuration, and both sync/async pages.

## Quick Setup

### 1. Configure Environment

Create `.env` file:

```bash
# SQLite (default)
DATABASE_URL=sqlite:///./nextpy.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/nextpy_db

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/nextpy_db
```

### 2. Initialize Database

Update `main.py`:

```python
from nextpy.server.app import create_app
from nextpy.db import init_db

# Initialize database
init_db()

app = create_app(...)
```

### 3. Define Models

```python
# models.py
from nextpy.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    slug = Column(String(255), unique=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 4. Use in Pages

**Async (recommended):**
```python
# pages/posts.py
from nextpy.db import get_session
from models import Post

async def get_server_side_props(context):
    session = get_session()
    try:
        posts = session.query(Post).all()
        return {"props": {"posts": posts}}
    finally:
        session.close()
```

**Sync (also supported):**
```python
# pages/posts.py
from nextpy.db import get_session
from models import Post

def get_server_side_props(context):  # No async needed!
    session = get_session()
    try:
        posts = session.query(Post).all()
        return {"props": {"posts": posts}}
    finally:
        session.close()
```

### 5. API Routes with Database

```python
# pages/api/posts.py
from fastapi import HTTPException
from nextpy.db import get_session, Post
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str

async def get(request):
    """GET /api/posts"""
    session = get_session()
    try:
        posts = session.query(Post).all()
        return {"posts": [{"id": p.id, "title": p.title} for p in posts]}
    finally:
        session.close()

async def post(request):
    """POST /api/posts"""
    session = get_session()
    try:
        data = await request.json()
        post_data = PostCreate(**data)
        post = Post(title=post_data.title, content=post_data.content)
        session.add(post)
        session.commit()
        return {"created": True, "id": post.id}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
```

## Environment Variables

All environment variables from `.env` are automatically loaded:

```python
from nextpy.config import settings, get_env

# Access settings
print(settings.database_url)
print(settings.debug)
print(settings.secret_key)

# Or individual variables
db_url = get_env("DATABASE_URL", "sqlite:///./nextpy.db")
```

## Supported Databases

| Database | URL Format |
|----------|-----------|
| SQLite | `sqlite:///./nextpy.db` |
| PostgreSQL | `postgresql://user:password@host:5432/db` |
| MySQL | `mysql+pymysql://user:password@host:3306/db` |
| MariaDB | `mysql+pymysql://user:password@host:3306/db` |

## Built-in Models

NextPy includes pre-built models:

```python
from nextpy.db import User, Post

# User model
user = User(email="user@example.com", username="john", full_name="John Doe")

# Post model  
post = Post(title="Hello", slug="hello", content="...", author_id=1)
```

## Advanced Configuration

### Connection Pooling

```bash
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

### Query Logging

```bash
DB_ECHO=true  # Log all SQL queries
```

### Custom Configuration

```python
from nextpy.db import Database

# Initialize with custom settings
db = Database(database_url="postgresql://...")
session = db.get_session()
```

## Sync vs Async

NextPy supports both sync and async page functions:

```python
# Async (modern, recommended)
async def get_server_side_props(context):
    # ... async code ...
    return {"props": {...}}

# Sync (simpler, also works)
def get_server_side_props(context):
    # ... regular sync code ...
    return {"props": {...}}
```

NextPy automatically handles the conversion!

## Examples

Visit `/db_example` to see a working example with users and posts.

API example: `GET /api/users_db`

## Best Practices

1. **Always close sessions**: Use try/finally or context managers
2. **Use async for production**: Better performance under load
3. **Index frequently queried fields**: Add `index=True` to columns
4. **Use connection pooling**: Enabled by default for PostgreSQL/MySQL
5. **Validate input**: Use Pydantic models for all API inputs

## Troubleshooting

**"DatabaseNotInitializedError"**
```python
# Make sure to call this in main.py
from nextpy.db import init_db
init_db()
```

**"No such table"**
```python
# Create tables
from nextpy.db import get_db
db = get_db()
db.create_tables()
```

**Port connection error**
- Check DATABASE_URL is correct
- Ensure database server is running
- Verify firewall allows connection
