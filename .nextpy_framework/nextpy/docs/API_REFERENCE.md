# NextPy API Reference

Complete API reference for NextPy v5.0.0.

## Table of Contents
1. [Core Components](#core-components)
2. [PSX Module](#psx-module)
3. [Hydration Engine](#hydration-engine)
4. [Server Actions](#server-actions)
5. [Database Integration](#database-integration)
6. [Authentication](#authentication)
7. [Router](#router)
8. [Utilities](#utilities)

---

## Core Components

### `@component` Decorator

Mark a function as a PSX component.

```python
from nextpy.psx import component

@component
def MyComponent(props=None):
    props = props or {}
    return psx("<div>Hello</div>")
```

**Parameters:**
- `props` (dict, optional): Component properties

**Returns:**
- Component render function

---

### `psx()` Function

Create PSX elements from template strings.

```python
from nextpy.psx import psx

html = psx("<div class='container'>Hello</div>")
```

**Parameters:**
- `template` (str): PSX template string

**Returns:**
- PSX element

---

## PSX Module

### Hooks

#### `useState(initialValue)`

Create reactive state in components.

```python
from nextpy.psx import useState

[count, setCount] = useState(0)
[name, setName] = useState("John")
```

**Parameters:**
- `initialValue` (any): Initial state value

**Returns:**
- `[state, setState]` tuple
  - `state`: Current state value
  - `setState`: Function to update state

**Example:**
```python
@component
def Counter(props=None):
    [count, setCount] = useState(0)
    
    def increment(e):
        setCount(count + 1)
    
    return psx(f"""
        <button onclick={increment}>
            Count: {count}
        </button>
    """)
```

---

#### `useEffect(callback, dependencies)`

Run side effects in components.

```python
from nextpy.psx import useEffect

def on_mount():
    print("Component mounted")

useEffect(on_mount, [])
```

**Parameters:**
- `callback` (function): Effect callback function
- `dependencies` (list): Dependency array

**Example:**
```python
@component
def DataFetcher(props=None):
    [data, setData] = useState(None)
    
    async def fetch_data():
        response = await fetch('/api/data')
        result = await response.json()
        setData(result)
    
    useEffect(fetch_data, [])
    
    return psx("<div>Loading...</div>")
```

---

#### `useMemo(callback, dependencies)`

Memoize expensive computations.

```python
from nextpy.psx import useMemo

computed = useMemo(lambda: expensive_calculation(), [input])
```

**Parameters:**
- `callback` (function): Computation callback
- `dependencies` (list): Dependency array

**Returns:**
- Memoized value

---

#### `useCallback(callback, dependencies)`

Memoize callback functions.

```python
from nextpy.psx import useCallback

handle_click = useCallback(lambda e: console.log("clicked"), [])
```

**Parameters:**
- `callback` (function): Callback to memoize
- `dependencies` (list): Dependency array

**Returns:**
- Memoized callback

---

#### `useRef(initialValue)`

Create a mutable ref object.

```python
from nextpy.psx import useRef

input_ref = useRef(null)
```

**Parameters:**
- `initialValue` (any): Initial ref value

**Returns:**
- Ref object with `current` property

---

### Component Functions

#### `Link(to, children, **kwargs)`

Create navigation links.

```python
from nextpy.psx import Link

return psx(f"""
    {Link("/about", "About Us")}
""")
```

**Parameters:**
- `to` (str): Destination path
- `children` (any): Link content
- `**kwargs`: Additional HTML attributes

---

#### `Image(src, alt, **kwargs)`

Create image elements.

```python
from nextpy.psx import Image

return psx(f"""
    {Image("/logo.png", "Logo", class="w-10 h-10")}
""")
```

**Parameters:**
- `src` (str): Image source
- `alt` (str): Alt text
- `**kwargs`: Additional HTML attributes

---

## Hydration Engine

### `@interactive_component` Decorator

Mark a component as interactive with client-side hydration.

```python
from nextpy.psx.hydration import interactive_component

@interactive_component
def Counter(props=None):
    [count, setCount] = useState(0)
    
    def increment(e):
        setCount(count + 1)
    
    return psx(f"""
        <button onclick={increment}>
            Count: {count}
        </button>
    """)
```

**Features:**
- Automatic state extraction
- Event handler conversion to JavaScript
- Client-side interactivity
- No page reloads needed

---

### `enable_hydration_globally()`

Enable hydration for all components.

```python
from nextpy.psx.hydration import enable_hydration_globally

enable_hydration_globally()

# Now all @component decorated functions are interactive
@component
def MyComponent(props=None):
    [count, setCount] = useState(0)
    # ... automatically hydrated!
```

---

### `create_interactive_page(html, script, title)`

Create a complete HTML page with hydration.

```python
from nextpy.psx.hydration import create_interactive_page

page = create_interactive_page(
    component_html,
    hydration_script,
    "My App"
)
```

**Parameters:**
- `html` (str): Component HTML
- `script` (str): Hydration script
- `title` (str): Page title

**Returns:**
- Complete HTML page string

---

## Server Actions

### `@server_action` Decorator

Mark a function as a server action.

```python
from nextpy.server_actions import server_action

@server_action
async def create_todo(title: str):
    # Server-side code
    todo = Todo(title=title)
    session.add(todo)
    session.commit()
    return todo
```

**Features:**
- Server-side execution
- Type safety with Pydantic
- Automatic serialization
- Error handling

---

### `fetch_api(url, options)`

Fetch data from API routes.

```python
from nextpy import fetch_api

data = await fetch_api('/api/todos')
```

**Parameters:**
- `url` (str): API endpoint
- `options` (dict): Fetch options

**Returns:**
- Parsed JSON response

---

## Database Integration

### `get_session()`

Get a database session.

```python
from nextpy.db import get_session

session = get_session()
users = session.query(User).all()
session.close()
```

**Returns:**
- SQLAlchemy session

---

### Model Definition

```python
from nextpy.db import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
```

---

## Authentication

### `AuthManager.create_token(user_id, expires_in)`

Create JWT token.

```python
from nextpy.auth import AuthManager

token = AuthManager.create_token(
    user_id=123,
    expires_in=3600
)
```

**Parameters:**
- `user_id` (int): User ID
- `expires_in` (int): Expiration time in seconds

**Returns:**
- JWT token string

---

### `AuthManager.verify_token(token)`

Verify JWT token.

```python
from nextpy.auth import AuthManager

user_id = AuthManager.verify_token(token)
```

**Parameters:**
- `token` (str): JWT token

**Returns:**
- User ID if valid

**Raises:**
- Exception if token is invalid

---

### `@require_auth` Decorator

Protect routes with authentication.

```python
from nextpy.auth import require_auth

@require_auth
async def protected_page(request):
    return {"message": "Protected content"}
```

---

## Router

### Router Class

```python
from nextpy.core.router import Router

router = Router(pages_dir="pages", templates_dir="templates")
router.scan_pages()
```

**Methods:**

#### `scan_pages()`
Scan pages directory and register routes.

#### `match(url_path)`
Find matching route for URL path.

```python
route, params = router.match("/users/123")
```

**Returns:**
- `(route, params)` tuple or `None`

#### `get_all_routes()`
Get all registered routes.

```python
routes = router.get_all_routes()
```

**Returns:**
- List of Route objects

---

### Route Parameters

```python
# pages/users/[id].py
async def get_server_side_props(context):
    user_id = context["params"]["id"]
    user = await fetch_user(user_id)
    return {"props": {"user": user}}
```

---

## Utilities

### Cache

```python
from nextpy.utils.cache import cache_result

@cache_result(ttl=3600)
async def expensive_operation():
    return await fetch_data()
```

---

### Email

```python
from nextpy.utils.email import send_email

await send_email(
    to=["user@example.com"],
    subject="Welcome!",
    html_content="<h1>Welcome</h1>"
)
```

---

### File Upload

```python
from nextpy.utils.file_upload import upload_file

async def post(request):
    form = await request.form()
    file = form["file"]
    
    file_path = await upload_file(file, directory="uploads")
    return {"file_path": file_path}
```

---

### Search

```python
from nextpy.utils.search import simple_search, fuzzy_search

results = simple_search("query", items, ["title"])
fuzzy_results = fuzzy_search("qury", items, "title")
```

---

### Validation

```python
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Name cannot be empty')
        return v
```

---

## Client-Side Router

### NextPyRouter Class

```javascript
const router = new NextPyRouter({
    mode: 'history',  // or 'hash'
    basePath: '/'
});

// Add routes
router.addRoute('/users/:id', (params, query) => {
    console.log('User ID:', params.id);
});

// Navigate
router.push('/users/123');

// Start router
router.start();
```

**Methods:**

#### `addRoute(path, handler, options)`
Register a route.

#### `push(path, options)`
Navigate to a path.

#### `replace(path, options)`
Replace current route.

#### `back()`
Go back in history.

#### `forward()`
Go forward in history.

#### `use(middleware)`
Add global middleware.

#### `setNotFound(handler)`
Set 404 handler.

---

## Type Definitions

### Route

```python
@dataclass
class Route:
    path: str
    file_path: Path
    handler: Optional[Callable]
    is_dynamic: bool
    is_api: bool
    is_catch_all: bool
    param_names: List[str]
    pattern: Optional[re.Pattern]
    layout_chain: List[Path]
```

### RouteParams

```python
class RouteParams(BaseModel):
    params: Dict[str, str] = {}
    query: Dict[str, str] = {}
```

---

## Constants

### HTTP Methods

- `GET`
- `POST`
- `PUT`
- `DELETE`
- `PATCH`

### Status Codes

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

---

**NextPy API Reference v5.0.0**
Last Updated: October 22, 2026
