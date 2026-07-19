# NextPy - Complete Documentation

## Table of Contents

1. [Getting Started](#getting-started)
2. [File-Based Routing](#file-based-routing)
3. [Pages & Data Fetching](#pages--data-fetching)
4. [API Routes](#api-routes)
5. [Database Integration](#database-integration)
6. [Authentication](#authentication)
7. [Components & Templates](#components--templates)
8. [Styling with Tailwind CSS](#styling-with-tailwind-css)
9. [Built-in Utilities](#built-in-utilities)
10. [Configuration](#configuration)
11. [Deployment](#deployment)
12. [API Reference](#api-reference)

---

## Getting Started

### Installation

```bash
pip install nextpy-framework
nextpy create my-app
cd my-app
nextpy dev
```

Visit `http://localhost:5000` - your app runs with hot reload!

### Project Structure

```
my-app/
├── pages/                      # File-based routes
│   ├── index.py               # Home (/)
│   ├── about.py               # About (/about)
│   ├── blog/
│   │   ├── index.py          # Blog listing (/blog)
│   │   └── [slug].py         # Dynamic posts (/blog/post-name)
│   └── api/
│       ├── posts.py          # GET /api/posts
│       ├── posts.py (POST)   # POST /api/posts
│       └── users/[id].py     # GET /api/users/123
├── templates/
│   ├── _base.html            # Root layout
│   ├── index.html            # Home template
│   └── components/
│       ├── button.html       # Reusable components
│       ├── card.html
│       └── modal.html
├── public/                     # Static files
│   └── tailwind.css            # Compiled Tailwind CSS
├── models/                    # Database models
│   └── user.py
├── nextpy.config.py          # Framework config
├── main.py                   # Entry point
├── .env                      # Secrets
├── package.json              # Node.js dependencies
├── tailwind.config.js        # Tailwind CSS configuration
├── postcss.config.js         # PostCSS configuration
└── styles.css                # Tailwind CSS directives
```

---

## File-Based Routing

### Basic Routes

Files in `pages/` automatically become HTTP routes:

| File | Route |
|------|-------|
| `pages/index.py` | `/` |
| `pages/about.py` | `/about` |
| `pages/blog/index.py` | `/blog` |
| `pages/contact.py` | `/contact` |

### Dynamic Routes

Use `[param]` for dynamic segments:

```python
# pages/blog/[slug].py
def get_template():
    return "blog/post.html"

async def get_server_side_props(context):
    slug = context["params"]["slug"]
    post = await fetch_post(slug)
    return {"props": {"post": post}}
```

Access: `/blog/hello-world` → `slug = "hello-world"`

### Catch-All Routes

Use `[...path]` to capture multiple segments:

```python
# pages/docs/[...path].py
async def get_server_side_props(context):
    path = context["params"]["path"]  # ["guides", "setup"]
    page = await get_docs(path)
    return {"props": {"page": page}}
```

Access: `/docs/guides/setup` → `path = ["guides", "setup"]`

---

## Pages & Data Fetching

### Basic Page

```python
# pages/hello.py
def get_template():
    return "hello.html"

async def get_server_side_props(context):
    return {
        "props": {
            "name": "NextPy",
            "year": 2025
        }
    }
```

Template (`templates/hello.html`):
```html
{% extends "_base.html" %}
{% block content %}
<h1 class="text-3xl font-bold underline">Hello {{ name }}!</h1>
<p>Year: {{ year }}</p>
{% endblock %}
```

### Server-Side Rendering (SSR)

Data fetched **per request**:

```python
async def get_server_side_props(context):
    # Fetch fresh data on every request
    data = await fetch_from_database()
    return {
        "props": {"data": data},
        "revalidate": 60  # Cache for 60 seconds
    }
```

### Static Generation (SSG)

Data fetched **at build time**:

```python
async def get_static_props():
    posts = await get_all_posts()
    return {
        "props": {"posts": posts},
        "revalidate": 3600  # Regenerate every hour
    }

async def get_static_paths():
    # Generate paths at build time
    posts = await get_all_posts()
    return ["/blog/" + post.slug for post in posts]
```

Build static site: `nextpy build`

---

## API Routes

### Basic GET Request

```python
# pages/api/posts.py
async def get(request):
    posts = await fetch_posts()
    return {"posts": posts}
```

Request: `GET /api/posts` → Returns JSON

### POST Request

```python
# pages/api/posts.py
from pydantic import BaseModel

class CreatePost(BaseModel):
    title: str
    content: str

async def post(request):
    body = await request.json()
    post = CreatePost(**body)
    
    # Save to database
    new_post = await save_post(post)
    return {"id": new_post.id, "title": new_post.title}, 201
```

Request:
```bash
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello", "content": "World"}'
```

### Dynamic API Routes

```python
# pages/api/posts/[id].py
async def get(request):
    post_id = request.path_params["id"]
    post = await fetch_post(post_id)
    if not post:
        return {"error": "Not found"}, 404
    return {"post": post}

async def put(request):
    post_id = request.path_params["id"]
    body = await request.json()
    updated = await update_post(post_id, body)
    return {"post": updated}

async def delete(request):
    post_id = request.path_params["id"]
    await delete_post(post_id)
    return {"message": "Deleted"}, 204
```

### All HTTP Methods

```python
# pages/api/resource.py

async def get(request):
    """GET request handler"""
    return {"method": "GET"}

async def post(request):
    """POST request handler"""
    body = await request.json()
    return {"method": "POST", "data": body}

async def put(request):
    """PUT request handler"""
    body = await request.json()
    return {"method": "PUT", "data": body}

async def delete(request):
    """DELETE request handler"""
    return {"method": "DELETE"}

async def patch(request):
    """PATCH request handler"""
    body = await request.json()
    return {"method": "PATCH", "data": body}
```

---

## Database Integration

### Setup

```python
# main.py or config
from nextpy.db import engine, Base, Session
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

# Define model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Configuration

```python
# nextpy.config.py or .env
DATABASE_URL=sqlite:///app.db
# or
DATABASE_URL=postgresql://user:pass@localhost/dbname
# or
DATABASE_URL=mysql://user:pass@localhost/dbname
```

### Query Data in Pages

```python
# pages/users.py
from nextpy.db import Session
from models.user import User

async def get_server_side_props(context):
    with Session() as session:
        users = session.query(User).all()
        return {
            "props": {"users": [{"id": u.id, "name": u.name} for u in users]}
        }
```

### Query in API Routes

```python
# pages/api/users.py
from nextpy.db import Session
from models.user import User
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

async def get(request):
    with Session() as session:
        users = session.query(User).all()
        return {"users": [{"id": u.id, "name": u.name} for u in users]}

async def post(request):
    body = await request.json()
    user_data = UserCreate(**body)
    
    with Session() as session:
        user = User(name=user_data.name, email=user_data.email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"id": user.id, "name": user.name}, 201
```

---

## Authentication

### JWT Authentication

```python
# pages/api/login.py
from nextpy.auth import AuthManager
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

async def post(request):
    body = await request.json()
    data = LoginRequest(**body)
    
    # Verify credentials
    user = await verify_user(data.username, data.password)
    if not user:
        return {"error": "Invalid credentials"}, 401
    
    # Create token
    token = AuthManager.create_token(
        user_id=user.id,
        expires_in=3600  # 1 hour
    )
    
    return {"token": token}
```

### Verify Token

```python
# pages/api/profile.py
from nextpy.auth import AuthManager

async def get(request):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    
    try:
        user_id = AuthManager.verify_token(token)
        user = await get_user(user_id)
        return {"user": {"id": user.id, "name": user.name}}
    except:
        return {"error": "Unauthorized"}, 401
```

### Protected Routes Middleware

```python
# middleware.py
from nextpy.auth import AuthManager

async def require_auth(request, call_next):
    auth = request.headers.get("Authorization")
    if not auth:
        return {"error": "Unauthorized"}, 401
    
    try:
        token = auth.replace("Bearer ", "")
        user_id = AuthManager.verify_token(token)
        request.user_id = user_id
    except:
        return {"error": "Invalid token"}, 401
    
    return await call_next(request)
```

---

## Components & Templates

### Built-in Components

#### Button

```html
{% from 'components/button.html' import button %}
{{ button('Click me', href='/page', disabled=False, variant='primary') }}
```

#### Card

```html
{% from 'components/card.html' import card %}
{{ card(title='Title', content='Content here', footer='Footer') }}
```

#### Modal

```html
{% from 'components/modal.html' import modal %}
{{ modal(id='myModal', title='Confirm', content='Are you sure?') }}
```

#### Form

```html
{% from 'components/form.html' import form_input %}
{{ form_input('email', type='email', placeholder='Enter email') }}
```

### Custom Components

Create `templates/components/custom.html`:

```html
{% macro custom_card(title, items=[]) %}
<div class="card">
    <h3>{{ title }}</h3>
    {% for item in items %}
    <p>{{ item }}</p>
    {% endfor %}
</div>
{% endmacro %}
```

Use in templates:

```html
{% from 'components/custom.html' import custom_card %}
{{ custom_card('My Title', items=['Item 1', 'Item 2']) }}
```

### Base Layout

`templates/_base.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My App{% endblock %}</title>
    <link href="/public/tailwind.css" rel="stylesheet">
</head>
<body>
    <nav>Navigation</nav>
    
    <div id="main-content">
        {% block content %}{% endblock %}
    </div>
    
    <footer>Footer</footer>
</body>
</html>
```

---

## Styling with Tailwind CSS

NextPy supports seamless integration with Tailwind CSS for rapid and utility-first styling. Follow these steps to set up Tailwind CSS in your NextPy project:

### 1. Install Node.js Dependencies

Navigate to your project root and install Tailwind CSS, PostCSS, and Autoprefixer using npm:

```bash
npm init -y
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
```

### 2. Configure Tailwind CSS

Create `tailwind.config.js` in your project root:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './templates/**/*.html', // Crucial for scanning Jinja2 templates
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

Create `postcss.config.js` in your project root:

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

Create `styles.css` in your project root (or `public/css/styles.css` for better organization) with the Tailwind directives:

```css
/* styles.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 3. Automatic CSS Compilation (`main.py`)

NextPy's `main.py` is configured to automatically compile your Tailwind CSS when the application starts. Ensure the following snippet is present (it's included by default in new projects):

```python
# main.py (excerpt)
import subprocess

# ... other imports and setup ...

try:
    print("Compiling Tailwind CSS...")
    # This command reads styles.css and outputs compiled CSS to public/tailwind.css
    subprocess.run(["npx", "tailwindcss", "-i", "./styles.css", "-o", "./public/tailwind.css"], check=True)
    print("Tailwind CSS compiled successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error compiling Tailwind CSS: {e}")
except FileNotFoundError:
    print("Error: npx or tailwindcss command not found. Make sure Node.js and Tailwind CSS are installed.")

# ... rest of your NextPy app creation ...
```

### 4. Link Compiled CSS in your Base Template

Include the compiled Tailwind CSS file in your main layout template, typically `templates/_base.html`:

```html
<!-- templates/_base.html (excerpt) -->
<head>
  <!-- ... other head elements ... -->
  <link href="/public/tailwind.css" rel="stylesheet">
</head>
<body>
  <!-- ... rest of your layout ... -->
</body>
```

### 5. Using Tailwind Classes

You can now use Tailwind CSS classes directly in your Jinja2 templates:

```html
<!-- templates/my_page.html -->
{% extends "_base.html" %}

{% block content %}
<h1 class="text-4xl font-bold text-blue-600 my-4">Welcome to My NextPy App</h1>
<button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
  Click Me
</button>
{% endblock %}
```

With these steps, your NextPy application will leverage Tailwind CSS for styling, with the compiled CSS available as a static asset for offline use.

---

## Built-in Utilities

### Caching

```python
from nextpy.utils.cache import Cache

# Simple cache
cache = Cache()
cache.set("key", "value", ttl=3600)  # 1 hour
value = cache.get("key")

# In pages
from nextpy.utils.cache import cached

@cached(ttl=600)
async def expensive_operation():
    return await fetch_data()
```

### Email

```python
from nextpy.utils.email import send_email

# Configure in .env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Send email
await send_email(
    to="user@example.com",
    subject="Welcome!",
    html="<h1>Hello</h1>"
)
```

### File Uploads

```python
# pages/api/upload.py
from nextpy.utils.uploads import handle_upload

async def post(request):
    form = await request.form()
    file = form["file"]
    
    filename = await handle_upload(
        file,
        upload_dir="public/uploads",
        max_size=5*1024*1024  # 5MB
    )
    
    return {"filename": filename}
```

### Search

```python
from nextpy.utils.search import SimpleSearch, FuzzySearch

# Simple search
search = SimpleSearch(["apple", "apricot", "banana"])
results = search.find("app")  # ["apple", "apricot"]

# Fuzzy search
fuzzy = FuzzySearch(data_list)
matches = fuzzy.search("appel", threshold=0.8)  # Matches "apple"
```

### Logging

```python
from nextpy.utils.logging import get_logger

logger = get_logger("myapp")
logger.info("Application started")
logger.error("An error occurred", exc_info=True)
```

### Validation

```python
from nextpy.utils.validators import (
    validate_email,
    validate_url,
    validate_phone
)

is_valid = validate_email("user@example.com")
is_valid = validate_url("https://example.com")
is_valid = validate_phone("+1234567890")
```

---

## Configuration

### Environment Variables

Create `.env`:

```
DATABASE_URL=sqlite:///app.db
DEBUG=True
SECRET_KEY=your-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

Load in code:

```python
from nextpy.config import settings

database_url = settings.database_url
debug = settings.debug
secret_key = settings.secret_key
```

### Custom Configuration

`nextpy.config.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Deployment

### Build for Production

```bash
nextpy build
```

Creates optimized static files in `out/` directory.

### Start Production Server

```bash
nextpy start
```

### Docker Deployment

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["nextpy", "start"]
```

### Environment Variables

Set in production:

```
DATABASE_URL=postgresql://...
DEBUG=False
SECRET_KEY=production-secret-key
```

---

## API Reference

### Core Functions

#### `get_template()`

Returns template filename for page rendering.

```python
def get_template():
    return "page.html"
```

#### `get_server_side_props(context)`

Fetches data per request (SSR).

```python
async def get_server_side_props(context):
    return {
        "props": {"key": "value"},
        "revalidate": 60
    }
```

#### `get_static_props()`

Fetches data at build time (SSG).

```python
async def get_static_props():
    return {
        "props": {"key": "value"},
        "revalidate": 3600
    }
```

#### `get_static_paths()`

Defines which paths to pre-generate.

```python
async def get_static_paths():
    return ["/", "/about", "/blog/post-1"]
```

### HTTP Handlers

```python
async def get(request):
    """Handle GET requests"""
    
async def post(request):
    """Handle POST requests"""
    
async def put(request):
    """Handle PUT requests"""
    
async def delete(request):
    """Handle DELETE requests"""
    
async def patch(request):
    """Handle PATCH requests"""
```

### Request Object

```python
request.method      # HTTP method
request.path        # Request path
request.headers     # Headers dict
request.query_params  # Query parameters
await request.json()  # Parse JSON body
await request.form()  # Parse form data
request.cookies     # Cookies dict
```

### Response

```python
return {
    "key": "value"
}  # Returns JSON (200)

return {"error": "message"}, 400  # Custom status code

return HTMLResponse("<h1>HTML</h1>")  # Return HTML
```

---

## CLI Commands

```bash
# Create new project
nextpy create my-app

# Development server with hot reload
nextpy dev

# Build static site
nextpy build

# Start production server
nextpy start

# Generate new page
nextpy create page my-page

# Generate new API
nextpy create api my-endpoint

# Generate new component
nextpy create component my-component

# Show all routes
nextpy routes
```

---

## Examples

### Blog Post Page

```python
# pages/blog/[slug].py
async def get_static_paths():
    posts = await get_all_posts()
    return [f"/blog/{p.slug}" for p in posts]

async def get_static_props():
    slug = context["params"]["slug"]
    post = await get_post(slug)
    return {
        "props": {"post": post},
        "revalidate": 3600
    }

def get_template():
    return "blog/post.html"
```

### Todo API

```python
# pages/api/todos.py
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    completed: bool = False

async def get(request):
    todos = await get_all_todos()
    return {"todos": todos}

async def post(request):
    body = await request.json()
    todo = TodoCreate(**body)
    new_todo = await create_todo(todo)
    return {"todo": new_todo.dict()}, 201
```

### Protected API Route

```python
# pages/api/user/profile.py
from nextpy.auth import AuthManager

async def get(request):
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "")
    
    try:
        user_id = AuthManager.verify_token(token)
        user = await get_user(user_id)
        return {"user": user.dict()}
    except:
        return {"error": "Unauthorized"}, 401
```

---

## Troubleshooting

### Hot Reload Not Working

- Check if watchdog is installed: `pip install watchdog`
- Ensure `nextpy dev` is running
- Try manual reload: `Ctrl+Shift+R` in development

### Database Connection Error

- Verify DATABASE_URL in .env
- Check database server is running
- For PostgreSQL: install `psycopg2` → `pip install psycopg2-binary`

### Import Errors

- Ensure package is installed: `pip install nextpy-framework`
- Check PYTHONPATH includes project directory
- Restart dev server after new installs

### Template Not Found

- Check template filename in `get_template()`
- Verify file exists in `templates/` directory
- Use relative paths: `"page.html"` not `"./page.html"`

### Tailwind CSS Not Applying / Compiling

- **Node.js and npm:** Ensure Node.js and npm are installed on your system. Run `node -v` and `npm -v` to verify.
- **Dependencies:** Make sure you have installed the necessary Node.js dependencies: `npm install -D tailwindcss@latest postcss@latest autoprefixer@latest`.
- **Configuration:** Double-check `tailwind.config.js` and `postcss.config.js` for correct syntax and content, especially the `content` array in `tailwind.config.js` including `'./templates/**/*.html'`.
- **`styles.css`:** Verify that `styles.css` exists in the project root (or the path specified in `main.py`) and contains the `@tailwind` directives.
- **`main.py` Compilation:** Confirm the `subprocess.run` command in `main.py` for Tailwind CSS compilation is present and executes without errors when you run `nextpy dev`.
- **Link in `_base.html`:** Ensure `<link href="/public/tailwind.css" rel="stylesheet">` is correctly placed in the `<head>` section of your `templates/_base.html`.
- **Clear Browser Cache:** Sometimes browser caching can prevent new styles from loading. Try a hard refresh (`Ctrl+Shift+R` or `Cmd+Shift+R`) or clear your browser's cache.

---

## Best Practices

1. **Organize routes logically** - Group related pages in directories
2. **Use SSG for static content** - Improves performance
3. **Cache expensive operations** - Use `@cached` decorator
4. **Validate all inputs** - Use Pydantic models in APIs
5. **Protect sensitive routes** - Use authentication middleware
6. **Use environment variables** - Don't hardcode secrets
7. **Write reusable components** - DRY principle
8. **Handle errors gracefully** - Always return proper status codes
9. **Optimize Tailwind CSS for Production** - When deploying to production, ensure you run `nextpy build` to generate optimized static files, which will include the purged and minified Tailwind CSS. This ensures the smallest possible CSS bundle size.

---

## Resources

- **Examples**: `/examples` page on the app
- **Components**: `/examples` for UI component showcase
- **Blog**: `/blog` for tutorials
- **GitHub**: [NextPy Framework](https://github.com/IBRAHIMFONYUY/nextpy-framework)
- **Community**: Join our Discord

---

**NextPy v1.0.0** - The Python web framework inspired by Next.js
Built with love ❤️ by the NextPy community.
