# NextPy - Comprehensive Developer Guide

## 📖 Table of Contents
1. [Getting Started](#getting-started)
2. [Core Concepts](#core-concepts)
3. [File-Based Routing](#file-based-routing)
4. [Server-Side Rendering](#server-side-rendering)
5. [Static Generation](#static-generation)
6. [API Routes](#api-routes)
7. [Database Integration](#database-integration)
8. [Authentication](#authentication)
9. [Components & Templates](#components--templates)
10. [Styling with Tailwind CSS](#styling-with-tailwind-css)
11. [Utilities & Tools](#utilities--tools)
12. [Development Tools](#development-tools)
13. [Performance Optimization](#performance-optimization)
14. [Testing](#testing)
15. [Deployment](#deployment)
16. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation

```bash
pip install nextpy-framework
```

### Create New Project

```bash
nextpy create my-app
cd my-app
```

### Project Structure

```
my-app/
├── pages/                  # Your app routes
│   ├── index.py           # Homepage (/)
│   ├── about.py           # About page (/about)
│   ├── blog/
│   │   ├── index.py       # Blog listing (/blog)
│   │   └── [slug].py      # Dynamic blog post (/blog/:slug)
│   └── api/
│       ├── users.py       # GET /api/users
│       └── posts.py       # GET /api/posts
├── templates/             # Jinja2 templates
│   ├── _base.html         # Base layout
│   ├── index.html         # Homepage template
│   ├── components/        # Reusable components
│   └── [page].html        # Page templates
├── public/                # Static files
│   └── tailwind.css       # Compiled Tailwind CSS
├── models/                # Database models
├── tests/                 # Test files
├── nextpy/                # Framework code
├── main.py               # Application entry
├── requirements.txt      # Dependencies
├── package.json          # Node.js dependencies
├── tailwind.config.js    # Tailwind CSS configuration
├── postcss.config.js     # PostCSS configuration
├── styles.css            # Tailwind CSS directives
└── .env                  # Configuration

```

### Development Server

```bash
nextpy dev
```

Starts server with hot reload at `http://localhost:5000`

---

## Core Concepts

### Pages vs Routes

- **Pages** = Python files in `pages/` that render HTML
- **Routes** = API endpoints or dynamic segments

```python
# pages/index.py → / (homepage)
# pages/about.py → /about
# pages/blog/index.py → /blog
# pages/blog/[slug].py → /blog/:slug
# pages/api/posts.py → /api/posts
```

### Lifecycle

1. Request comes in
2. Router matches to page/API
3. `get_server_side_props()` runs (optional)
4. Page renders with props
5. Response sent

---

## File-Based Routing

### Basic Pages

Create `pages/about.py`:

```python
def get_template():
    return "about.html"

async def get_server_side_props(context):
    return {
        "props": {
            "title": "About Us",
            "description": "Learn about our company"
        }
    }
```

Template `templates/about.html`:

```html
{% extends "_base.html" %}

{% block content %}
<h1 class="text-4xl font-bold">{{ title }}</h1>
<p class="text-lg">{{ description }}</p>
{% endblock %}
```

### Dynamic Routes

Create `pages/products/[id].py`:

```python
async def get_server_side_props(context):
    product_id = context["params"]["id"]
    product = await fetch_product(product_id)
    
    if not product:
        return {"notFound": True}
    
    return {"props": {"product": product}}
```

Access via: `/products/123`, `/products/456`, etc.

### Catch-All Routes

Create `pages/docs/[...slug].py`:

```python
async def get_server_side_props(context):
    slug_parts = context["params"]["slug"]  # ['guides', 'advanced', 'performance']
    path = "/".join(slug_parts)
    return {"props": {"path": path}}
```

Access via: `/docs/guides/advanced`, `/docs/guides/advanced`, etc.

---

## Server-Side Rendering

### get_server_side_props

Fetch data per request:

```python
async def get_server_side_props(context):
    # context contains: request, params, query
    
    posts = await fetch_posts()
    user = await fetch_user(context["query"].get("user_id"))
    
    return {
        "props": {
            "posts": posts,
            "user": user
        },
        "revalidate": 60  # Revalidate every 60 seconds (ISR)
    }
```

**When to use:**
- Content changes frequently
- Need access to request data
- User-specific data
- Real-time data

---

## Static Generation

### get_static_props

Pre-render at build time:

```python
async def get_static_props(context):
    all_posts = await fetch_all_posts()
    
    return {
        "props": {"posts": all_posts},
        "revalidate": 86400  # Revalidate daily
    }
```

### get_static_paths

Pre-generate paths:

```python
async def get_static_paths():
    posts = await fetch_all_posts()
    
    return {
        "paths": [{"params": {"slug": p.slug}} for p in posts],
        "fallback": "blocking"  # Generate on-demand
    }
```

**When to use:**
- Content rarely changes
- Need ultra-fast performance
- Can pre-generate all variations
- Marketing/landing pages

---

## API Routes

### GET Endpoint

`pages/api/users.py`:

```python
async def get(request):
    users = await fetch_all_users()
    return {"users": users}
```

Request: `GET /api/users`

### POST Endpoint

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

async def post(request):
    data = await request.json()
    user = UserCreate(**data)
    
    new_user = await create_user(user.name, user.email)
    return {"created": True, "user_id": new_user.id}
```

Request:
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'
```

### Query Parameters

```python
async def get(request):
    page = int(request.query_params.get("page", 1))
    limit = int(request.query_params.get("limit", 10))
    
    users = await fetch_users(page=page, limit=limit)
    return {"users": users}
```

Request: `GET /api/users?page=2&limit=20`

### Error Handling

```python
from fastapi import HTTPException

async def get(request):
    user_id = request.query_params.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing id")
    
    user = await fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"user": user}
```

---

## Database Integration

### Setup

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/nextpy
```

### Define Models

```python
# models/user.py
from nextpy.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Query Data

```python
from nextpy.db import get_session, User

async def get_server_side_props(context):
    session = get_session()
    
    # Fetch
    users = session.query(User).all()
    user = session.query(User).filter_by(email="john@example.com").first()
    
    session.close()
    return {"props": {"users": users}}
```

### Create/Update/Delete

```python
from nextpy.db import get_session, User

async def post(request):
    session = get_session()
    data = await request.json()
    
    # Create
    user = User(name=data["name"], email=data["email"])
    session.add(user)
    session.commit()
    
    # Update
    user.name = "New Name"
    session.commit()
    
    # Delete
    session.delete(user)
    session.commit()
    
    session.close()
    return {"success": True}
```

### Relationships

```python
from sqlalchemy import ForeignKey, relationship

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    posts = relationship("Post", back_populates="user")
```

---

## Authentication

### JWT Tokens

```python
from nextpy.auth import AuthManager

# Create token
token = AuthManager.create_token(user_id=123)

# Verify token
user_id = AuthManager.verify_token(token)
```

### Protected Routes

```python
from nextpy.auth import require_auth
from fastapi import Request

@require_auth
async def get(request: Request):
    user_id = request.state.user_id
    return {"user_id": user_id}
```

### Login Example

`pages/api/login.py`:

```python
from nextpy.auth import AuthManager
from nextpy.db import get_session, User

async def post(request):
    data = await request.json()
    
    session = get_session()
    user = session.query(User).filter_by(email=data["email"]).first()
    
    if not user or not verify_password(data["password"], user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = AuthManager.create_token(user_id=user.id)
    session.close()
    Link("/about", "About Us", prefetch=False)
    return {"token": token, "user_id": user.id}
```

### Frontend Usage

```html
<script>
// Login
const response = await fetch('/api/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email, password})
});

const {token} = await response.json();
localStorage.setItem('token', token);

// Protected request
const response = await fetch('/api/protected', {
    headers: {'Authorization': `Bearer ${localStorage.getItem('token')}`}
});
</script>
```

---

## Components & Templates

### Built-In Components

#### Button

```html
{% from "components/button.html" import button %}
{{ button("Click Me", "/action", "primary", "md") }}
```

#### Input Field

```html
{% from "components/form.html" import input %}
{{ input("email", "Email", "email", required=True) }}
```

#### Card

```html
{% from "components/card.html" import card %}
{{ card("Title", "Content here", "primary") }}
```

#### Pagination

```html
{% from "components/pagination.html" import pagination %}
{{ pagination(current_page, total_pages, "/posts") }}
```

#### Modal

```html
{% from "components/modal.html" import modal %}
{{ modal("modal_id", "Modal Title", "Modal content") }}
```

#### Toast Notification

```html
{% from "components/toast.html" import toast %}
{{ toast("Success!", "success", 3000) }}
```

#### Dropdown

```html
{% from "components/dropdown.html" import dropdown %}
{% set items = [
    {"label": "Profile", "href": "/profile"},
    {"label": "Settings", "href": "/settings"}
] %}
{{ dropdown("Menu", items, "user-menu") }}
```

#### Tabs

```html
{% from "components/tabs.html" import tabs %}
{% set tabs_content = [
    {"label": "Overview", "content": "<p>Overview content</p>"},
    {"label": "Details", "content": "<p>Details content</p>"}
] %}
{{ tabs(tabs_content, "main-tabs") }}
```

### Custom Components

Create `templates/components/custom.html`:

```html
{% macro custom_component(title, items) %}
<div class="custom-component">
    <h3>{{ title }}</h3>
    {% for item in items %}
        <div class="item">{{ item }}</div>
    {% endfor %}
</div>
{% endmacro %}
```

Use it:

```html
{% from "components/custom.html" import custom_component %}
{{ custom_component("My Title", ["item1", "item2"]) }}
```

---

## Styling with Tailwind CSS

NextPy provides a streamlined workflow for integrating Tailwind CSS into your projects, allowing you to build UIs rapidly with a utility-first approach.

### 1. Install Node.js Dependencies

Tailwind CSS is a PostCSS plugin, requiring Node.js and npm. Navigate to your project root and install the necessary packages:

```bash
npm init -y
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
```

### 2. Configure Tailwind CSS

Create `tailwind.config.js` in your project root to configure Tailwind's content paths, theme, and plugins. It's crucial to include your Jinja2 template files (`./templates/**/*.html`) in the `content` array so Tailwind can scan them for classes:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './templates/**/*.html', // Include this line for Jinja2 templates
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

Create `postcss.config.js` in your project root to enable PostCSS and its plugins, including Tailwind CSS and Autoprefixer:

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

Create a `styles.css` file (e.g., in your project root or `public/css/`) and include the Tailwind directives:

```css
/* styles.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 3. Automatic CSS Compilation with `main.py`

NextPy's `main.py` is pre-configured to automatically compile your Tailwind CSS into a static file (`public/tailwind.css`) whenever your application starts. This ensures that your styles are always up-to-date. The relevant section in `main.py` looks like this:

```python
# main.py (excerpt)
import subprocess

# ... other imports and setup ...

try:
    print("Compiling Tailwind CSS...")
    subprocess.run(["npx", "tailwindcss", "-i", "./styles.css", "-o", "./public/tailwind.css"], check=True)
    print("Tailwind CSS compiled successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error compiling Tailwind CSS: {e}")
except FileNotFoundError:
    print("Error: npx or tailwindcss command not found. Make sure Node.js and Tailwind CSS are installed.")

# ... rest of your NextPy app creation ...
```

### 4. Link Compiled CSS in your Base Template

To apply the Tailwind CSS styles to your application, link the compiled CSS file (`/public/tailwind.css`) in the `<head>` section of your base Jinja2 template (typically `templates/_base.html`):

```html
<!-- templates/_base.html (excerpt) -->
<!DOCTYPE html>
<html>
<head>
    <!-- ... other head elements ... -->
    <link href="/public/tailwind.css" rel="stylesheet">
</head>
<body>
    <!-- ... rest of your layout ... -->
</body>
</html>
```

### 5. Using Tailwind Classes in Templates

Once set up, you can use Tailwind CSS utility classes directly within your Jinja2 templates. Tailwind will automatically detect these classes and include them in the compiled `public/tailwind.css` file.

```html
<!-- templates/my_awesome_page.html -->
{% extends "_base.html" %}

{% block content %}
<div class="container p-4 mx-auto bg-white rounded-lg shadow-lg">
    <h1 class="mb-6 text-5xl font-extrabold text-indigo-800">Hello, Tailwind!</h1>
    <p class="mb-8 text-lg leading-relaxed text-gray-700">
        This is an example of a NextPy page styled with 
        <span class="font-semibold text-teal-600">Tailwind CSS</span>. 
        Enjoy rapid UI development!
    </p>
    <button class="px-6 py-3 font-bold text-white transition duration-300 ease-in-out transform bg-blue-600 rounded-full shadow-xl hover:bg-blue-700 hover:scale-105">
        Learn More
    </button>
</div>
{% endblock %}
```

This integration ensures that your NextPy applications can leverage the full power of Tailwind CSS for modern and responsive designs, with the compiled styles being available offline once the application is running.

---

## Utilities & Tools

### Caching

```python
from nextpy.utils.cache import cache_result

@cache_result(ttl=3600)  # Cache for 1 hour
async def expensive_operation():
    data = await fetch_from_api()
    return data
```

### Email

```python
from nextpy.utils.email import send_email

await send_email(
    to=["user@example.com"],
    subject="Welcome!",
    html_content="<h1>Welcome to NextPy</h1>"
)
```

### File Upload

```python
from nextpy.utils.file_upload import upload_file

async def post(request):
    form = await request.form()
    file = form["file"]
    
    file_path = await upload_file(file, directory="uploads")
    return {"file_path": file_path}
```

### Search

```python
from nextpy.utils.search import simple_search, fuzzy_search

items = [
    {"id": 1, "title": "Getting Started"},
    {"id": 2, "title": "Advanced Guide"}
]

results = simple_search("getting", items, ["title"])
fuzzy_results = fuzzy_search("advanc", items, "title")
```

### Logging

```python
from nextpy.utils.logging import get_logger

logger = get_logger("my_app")
logger.info("User logged in", user_id=123)
logger.error("Database connection failed", error="timeout")
```

### Validation

```python
from pydantic import BaseModel, EmailStr, validator

class SignupForm(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    @validator('password')
    def password_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password too short')
        return v
```

---

## Development Tools

### Generators

Generate pages quickly:

```bash
nextpy create:page products
nextpy create:api products
nextpy create:component product-card
nextpy create:model Product
```

### Development Server

Hot reload automatically detects changes and compiles Tailwind CSS:

```bash
nextpy dev
```

Features:
- Auto-restart on file changes
- Error display in browser
- Performance stats
- **Automatic Tailwind CSS compilation**

### Build Optimization

```bash
nextpy build
```

Optimizations:
- Static generation
- Code splitting
- Compression
- Cache busting
- **Tailwind CSS purging and minification**

---

## Performance Optimization

### Rate Limiting

```python
from nextpy.performance import rate_limiter

async def api_endpoint(request):
    if not rate_limiter.is_allowed(request.client.host):
        raise HTTPException(status_code=429, detail="Too many requests")
    # Process request...
```

### Batch Processing

```python
from nextpy.performance import batch_processor

@batch_processor(batch_size=50)
async def process_item(item):
    return item * 2

results = await process_item(list(range(1000)))
```

### Timing

```python
from nextpy.performance import timeit

@timeit
async def slow_function():
    await asyncio.sleep(1)
```

### Static Site Generation

For maximum performance, use SSG:

```python
async def get_static_props(context):
    posts = await fetch_all_posts()
    return {"props": {"posts": posts}}

async def get_static_paths():
    posts = await fetch_all_posts()
    return {"paths": [{"params": {"slug": p.slug}} for p in posts]}
```

---

## Testing

### Setup

```bash
pip install pytest pytest-asyncio
```

### Write Tests

```python
# tests/test_pages.py
import pytest
from fastapi.testclient import TestClient
from nextpy.server.app import create_app

@pytest.fixture
def client():
    app = create_app(debug=True)
    return TestClient(app)

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "NextPy" in response.text

def test_api_endpoint(client):
    response = client.get("/api/posts")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
```

### Run Tests

```bash
pytest tests/ -v
pytest tests/test_pages.py::test_home_page
pytest --cov=nextpy
```

---

## Deployment

### Docker

```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Node.js and npm for Tailwind CSS compilation
RUN apt-get update && apt-get install -y nodejs npm
COPY package.json tailwind.config.js postcss.config.js styles.css ./
RUN npm install

COPY . .

# Compile Tailwind CSS during build (or ensure main.py runs it)
RUN npx tailwindcss -i ./styles.css -o ./public/tailwind.css --minify

CMD ["nextpy", "start"]
```

### Environment

Production `.env`:

```
DEBUG=false
DATABASE_URL=postgresql://...
SECRET_KEY=your-production-secret
JWT_SECRET=your-jwt-secret
```

### Start Server

```bash
nextpy build
nextpy start
```

---

## Troubleshooting

### Hot Reload Not Working

1. Check file permissions
2. Restart dev server
3. Check `.env` for correct paths

### Database Connection Error

1. Verify `DATABASE_URL` in `.env`
2. Check database is running
3. Verify credentials

### Import Errors

1. Check `requirements.txt`
2. Run `pip install -r requirements.txt`
3. Check file paths

### Slow Build

1. Use SSG for static pages
2. Enable caching
3. Check for N+1 queries

### Tailwind CSS Not Applying / Compiling

- **Node.js and npm:** Ensure Node.js and npm are installed on your system. Run `node -v` and `npm -v` to verify.
- **Dependencies:** Make sure you have installed the necessary Node.js dependencies: `npm install -D tailwindcss@latest postcss@latest autoprefixer@latest`.
- **Configuration:** Double-check `tailwind.config.js` and `postcss.config.js` for correct syntax and content, especially the `content` array in `tailwind.config.js` including `'./templates/**/*.html'`.
- **`styles.css`:** Verify that `styles.css` exists in the project root (or the path specified in `main.py`) and contains the `@tailwind` directives.
- **`main.py` Compilation:** Confirm the `subprocess.run` command in `main.py` for Tailwind CSS compilation is present and executes without errors when you run `nextpy dev`.
- **Link in `_base.html`:** Ensure `<link href="/public/tailwind.css" rel="stylesheet">` is correctly placed in the `<head>` section of your `templates/_base.html`.
- **Clear Browser Cache:** Sometimes browser caching can prevent new styles from loading. Try a hard refresh (`Ctrl+Shift+R` or `Cmd+Shift+R`) or clear your browser's cache.

---

## Resources

- **GitHub**: https://github.com/IBRAHIMFONYUY/nextpy-framework
- **Documentation**: See `DOCUMENTATION.md`
- **Quick Reference**: See `QUICK_REFERENCE.md`
- **Authentication Guide**: See `AUTHENTICATION.md`
- **Testing**: See `TESTING.md`
- **Performance**: See `PERFORMANCE.md`
- **WebSockets**: See `WEBSOCKETS.md`

---

**NextPy - Build Modern Python Web Apps Fast** 🚀
