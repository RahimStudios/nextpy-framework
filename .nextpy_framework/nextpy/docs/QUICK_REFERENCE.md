# NextPy Quick Reference

## Project Creation
```bash
pip install nextpy-framework
nextpy create my-app
cd my-app
nextpy dev
```

## File Structure
```
pages/
  index.py          # Routes automatically
  blog/
    [slug].py       # Dynamic routes
  api/
    posts.py        # API endpoints
templates/
  index.html        # Templates
  components/       # Reusable components
public/
  css/, js/, images/
main.py             # Entry point
```

## Core Concepts

### Pages (Server-Side Rendering)
```python
async def get_server_side_props(context):
    data = await fetch_data()
    return {"props": {"data": data}}
```

### API Routes
```python
async def get(request):
    return {"message": "hello"}

async def post(request):
    data = await request.json()
    return {"created": data}
```

### Database
```python
from nextpy.db import get_session, User
session = get_session()
users = session.query(User).all()
```

### Authentication
```python
from nextpy.auth import AuthManager
token = AuthManager.create_token(user_id=123)
user_id = AuthManager.verify_token(token)
```

### Caching
```python
from nextpy.utils.cache import cache_result
@cache_result(ttl=3600)
async def expensive_function():
    pass
```

### Components
```html
{% from "components/button.html" import button %}
{{ button("Click", "/action", "primary") }}
```

## CLI Commands
- `nextpy dev` - Development server
- `nextpy build` - Static build
- `nextpy start` - Production server
- `nextpy create app_name` - New project
- `nextpy routes` - List routes

## Configuration
```bash
# .env
DATABASE_URL=sqlite:///./app.db
DEBUG=true
SECRET_KEY=your-secret
JWT_SECRET=your-jwt-secret
```

## Testing
```bash
pip install pytest pytest-asyncio
pytest tests/ -v
```

## Common Tasks

### Add Database Model
```python
from nextpy.db import Base
from sqlalchemy import Column, String, Integer

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
```

### Create Login
```python
# pages/api/login.py
async def post(request):
    data = await request.json()
    token = AuthManager.create_token(user_id=user.id)
    return {"token": token}
```

### Send Email
```python
from nextpy.utils.email import send_email
await send_email(
    to=["user@example.com"],
    subject="Hello",
    html_content="<h1>Hi</h1>"
)
```

### Validate Forms
```python
from pydantic import BaseModel, EmailStr

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str
```

## Resources
- Full Docs: `DOCUMENTATION.md`
- Auth Guide: `AUTHENTICATION.md`
- Testing: `TESTING.md`
- Performance: `PERFORMANCE.md`
- GitHub: https://github.com/IBRAHIMFONYUY/nextpy-framework
