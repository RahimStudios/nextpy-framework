# NextPy Full-Stack Guide

Complete guide to building full-stack applications with NextPy's enhanced client-server communication system.

## Overview

NextPy v5.0 introduces powerful full-stack capabilities that bridge the gap between client-side interactivity and server-side logic. This guide covers:

- **Server Actions**: Call Python functions directly from client code
- **State Synchronization**: Real-time state sync between client and server
- **Enhanced API Routes**: Type-safe, validated API endpoints
- **Database Integration**: Seamless database operations from both client and server
- **Real-time Updates**: WebSocket-based live updates

## Architecture

NextPy uses a **hybrid routing system**:

- **Server-side routing** (primary): File-based routing with FastAPI backend
- **Client-side navigation** (enhanced): Smooth transitions without page reloads
- **API routes**: Server-side endpoints in `pages/api/` directory
- **Server actions**: Direct client-to-server function calls

### Client-Server Communication Flow

```
Client Component → Server Action → FastAPI Backend → Database → Response → Client Update
                    ↓
              WebSocket Broadcast → Real-time Sync
```

## Server Actions

Server actions allow you to define Python functions that can be called directly from client-side JavaScript, with automatic serialization, validation, and error handling.

### Defining Server Actions

```python
import nextpy as nx
from nextpy.server_actions import server_action, ValidationError
from nextpy.db import get_session, Todo

@server_action(name="create_todo")
async def create_todo(title: str, session=None):
    """Create a new todo item"""
    if not title or not title.strip():
        raise ValidationError("title", "Title cannot be empty")
    
    with session if session else get_session() as db:
        todo = Todo(title=title.strip(), completed=False)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        
        return {
            "id": todo.id,
            "title": todo.title,
            "completed": todo.completed
        }
```

### Calling Server Actions from Client

```javascript
// Using the enhanced client runtime
const result = await window.nextpy.executeAction("create_todo", {
    title: "Learn NextPy"
});

console.log("Created todo:", result);
```

### Validation

Server actions support built-in validation:

```python
from nextpy.server_actions import FormValidator, ActionSchema

# Schema-based validation
todo_schema = ActionSchema(
    title={
        'type': str,
        'required': True,
        'validator': lambda x: (len(x.strip()) > 0, "Title cannot be empty")
    }
)

@server_action(validate=lambda data: todo_schema.validate(data)[0])
async def create_todo_validated(title: str):
    # Validation runs automatically
    pass
```

### Built-in Validators

```python
from nextpy.server_actions import FormValidator

# Email validation
is_valid = FormValidator.validate_email("user@example.com")

# Password validation
is_valid, message = FormValidator.validate_password("MyPass123")

# Required fields
is_valid, message = FormValidator.validate_required_fields(
    {"name": "John", "email": "john@example.com"},
    ["name", "email"]
)
```

## State Synchronization

NextPy provides a powerful state management system with real-time synchronization.

### Server-Side State

```python
from nextpy.state_sync import get_state, set_state, update_state

# Set state
await set_state("user_theme", "dark")

# Get state
theme = await get_state("user_theme", "light")

# Update state with function
await update_state("counter", lambda x: x + 1)
```

### Client-Side State Subscription

```javascript
// Subscribe to state changes
const unsubscribe = window.nextpy.subscribe("user_theme", (newValue, oldValue, message) => {
    console.log("Theme changed from", oldValue, "to", newValue);
    document.body.className = newValue;
});

// Unsubscribe when done
unsubscribe();
```

### Declaring Models and the Database

A new NextPy app puts SQLAlchemy models in `models/` and initializes the
database in `main.py`. Import the shared `Base` from `nextpy.db` so every model
is registered before tables are created.

```python
# models/User.py
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from nextpy.db import Base


class User(Base):
    # The framework owns the "users" table; use a distinct table name for
    # application-specific models.
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
```

```python
# models/__init__.py
from models.User import User

__all__ = ["User"]
```

```python
# main.py
from nextpy.config import settings
from nextpy.db import init_db

import models  # registers every model on Base

init_db(settings["database_url"])

app = nx.create_app(...)
```

Set the connection string in the project `.env`:

```bash
DATABASE_URL=sqlite:///./app.db
# PostgreSQL: postgresql+psycopg://user:password@host:5432/dbname
# MySQL:      mysql+pymysql://user:password@host:3306/dbname
```

Query through ORM sessions (never concatenate user input into SQL):

```python
from nextpy.db import get_session

with get_session() as session:
    user = session.query(User).filter(User.email == email).first()
```

### Database-Backed State

For persistent state that survives server restarts:

```python
from nextpy.state_sync import DatabaseState

# Initialize database state storage
db_state = DatabaseState("app_state")
await db_state.initialize()

# Use like regular state
await db_state.set("user_preferences", {"theme": "dark"})
preferences = await db_state.get("user_preferences")
```

## Enhanced API Routes

API routes in NextPy are automatically integrated with the server actions system.

### File-Based API Routes

Create API endpoints in `pages/api/`:

```python
# pages/api/users.py
import nextpy as nx
from nextpy.db import get_session, User

@nx.api.get("/users")
async def list_users():
    with get_session() as db:
        users = db.query(User).all()
        return [{"id": u.id, "email": u.email} for u in users]

@nx.api.post("/users")
async def create_user(data: dict):
    with get_session() as db:
        user = User(email=data["email"], username=data["username"])
        db.add(user)
        db.commit()
        return {"id": user.id}
```

### Server Action API Endpoints

Server actions are automatically exposed via API:

```bash
# List all available actions
GET /__nextpy/actions

# Execute a server action
POST /__nextpy/actions/execute
{
    "action": "create_todo",
    "params": {"title": "Learn NextPy"}
}

# Get action schema
GET /__nextpy/actions/create_todo/schema
```

## Real-Time Updates

NextPy includes WebSocket support for real-time data synchronization.

### Server-Side Broadcasting

```python
from nextpy.websocket import manager

# Broadcast to all subscribers
await manager.broadcast("todos", {
    "type": "TODO_CHANGED",
    "action": "created",
    "todo": {"id": 1, "title": "New Todo"}
})
```

### Client-Side WebSocket Handling

The enhanced client runtime automatically handles WebSocket connections:

```javascript
// Listen for WebSocket messages
window.addEventListener('nextpy:todo:changed', (event) => {
    console.log("Todo updated:", event.detail);
    // Update UI accordingly
});

// WebSocket status events
window.addEventListener('nextpy:websocket:connected', () => {
    console.log("Real-time connection established");
});

window.addEventListener('nextpy:websocket:disconnected', () => {
    console.log("Real-time connection lost");
});
```

## Complete Example: Full-Stack Todo App

Here's a complete example combining all features:

### Server Actions (`pages/api/todos_actions.py`)

```python
import nextpy as nx
from nextpy.server_actions import server_action, ValidationError
from nextpy.db import get_session, Todo

@server_action()
async def get_todos(session=None):
    """Get all todos"""
    with session if session else get_session() as db:
        todos = db.query(Todo).order_by(Todo.created_at.desc()).all()
        return [
            {
                "id": todo.id,
                "title": todo.title,
                "completed": todo.completed
            }
            for todo in todos
        ]

@server_action()
async def create_todo(title: str, session=None):
    """Create a new todo"""
    if not title or not title.strip():
        raise ValidationError("title", "Title cannot be empty")
    
    with session if session else get_session() as db:
        todo = Todo(title=title.strip(), completed=False)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        
        # Broadcast to WebSocket subscribers
        from nextpy.websocket import manager
        await manager.broadcast("todos", {
            "type": "TODO_CHANGED",
            "action": "created",
            "todo": {"id": todo.id, "title": todo.title, "completed": False}
        })
        
        return {"id": todo.id, "title": todo.title, "completed": False}
```

### Client Component (`pages/todos.py`)

```python
from nextpy.psx import component, useState, useEffect
import nextpy as nx

@component
def TodoApp(props=None):
    """Full-stack todo application"""
    props = props or {}
    
    # Initial server-side data
    initial_todos = props.get("todos", [])
    
    return (
        <div class="max-w-2xl mx-auto p-6">
            <h1 class="text-3xl font-bold mb-6">Todos</h1>
            
            <div class="mb-4">
                <input 
                    type="text" 
                    id="new-todo"
                    placeholder="Add a new todo..."
                    class="w-full p-3 border rounded-lg"
                />
                <button 
                    onclick="createTodoFromClient()"
                    class="mt-2 px-4 py-2 bg-blue-600 text-white rounded-lg"
                >
                    Add Todo
                </button>
            </div>
            
            <ul id="todo-list" class="space-y-2">
                {initial_todos.map(todo => (
                    <li key={todo["id"]} class="p-3 bg-gray-100 rounded-lg">
                        {todo["title"]}
                    </li>
                ))}
            </ul>
            
            <script src="/static/js/todo-client.js"></script>
        </div>
    )

def get_server_side_props(context):
    """Fetch initial todos"""
    from nextpy.db import get_session, Todo
    
    with get_session() as db:
        todos = db.query(Todo).order_by(Todo.created_at.desc()).limit(10).all()
        
        return {
            "props": {
                "todos": [
                    {"id": t.id, "title": t.title, "completed": t.completed}
                    for t in todos
                ]
            }
        }

default = TodoApp
```

### Client JavaScript (`public/js/todo-client.js`)

```javascript
async function createTodoFromClient() {
    const input = document.getElementById('new-todo');
    const title = input.value.trim();
    
    if (!title) return;
    
    try {
        const result = await window.nextpy.executeAction("create_todo", {title});
        
        // Add to UI
        const list = document.getElementById('todo-list');
        const li = document.createElement('li');
        li.className = 'p-3 bg-gray-100 rounded-lg';
        li.textContent = result.title;
        li.dataset.id = result.id;
        list.prepend(li);
        
        input.value = '';
    } catch (error) {
        console.error('Failed to create todo:', error);
        alert('Failed to create todo');
    }
}

// Listen for real-time updates
window.addEventListener('nextpy:todo:changed', (event) => {
    const {action, todo} = event.detail;
    console.log('Todo update received:', action, todo);
    
    if (action === 'created') {
        // Add new todo to UI
        const list = document.getElementById('todo-list');
        const existing = document.querySelector(`[data-id="${todo.id}"]`);
        if (!existing) {
            const li = document.createElement('li');
            li.className = 'p-3 bg-gray-100 rounded-lg';
            li.textContent = todo.title;
            li.dataset.id = todo.id;
            list.prepend(li);
        }
    }
});
```

## Best Practices

### 1. Keep Server Actions Focused
Each server action should do one thing well:

```python
# Good: Single responsibility
@server_action()
async def create_user(email: str, username: str):
    # Only creates user
    pass

# Avoid: Multiple responsibilities
@server_action()
async def create_user_and_send_email(email: str, username: str):
    # Creates user AND sends email - better as separate actions
    pass
```

### 2. Use Validation Always
Validate inputs on the server side:

```python
@server_action()
async def update_profile(user_id: int, email: str):
    # Validate email format
    if not FormValidator.validate_email(email):
        raise ValidationError("email", "Invalid email format")
    
    # Update user
    pass
```

### 3. Handle Errors Gracefully
Server actions automatically handle errors, but provide meaningful messages:

```python
@server_action()
async def delete_item(item_id: int):
    item = db.get(Item, item_id)
    if not item:
        raise ServerActionError("Item not found", "NOT_FOUND")
    
    db.delete(item)
    db.commit()
```

### 4. Use WebSocket for Real-Time Features
Broadcast important state changes:

```python
@server_action()
async def update_status(status_id: int, new_status: str):
    # Update database
    status = db.get(Status, status_id)
    status.status = new_status
    db.commit()
    
    # Broadcast to all connected clients
    await manager.broadcast("status_updates", {
        "type": "STATUS_CHANGED",
        "status_id": status_id,
        "new_status": new_status
    })
```

### 5. Leverage Server-Side Rendering
Use `get_server_side_props` for initial data:

```python
def get_server_side_props(context):
    # Fetch initial data server-side for fast initial load
    with get_session() as db:
        data = db.query(Model).all()
    
    return {
        "props": {"initial_data": data}
    }
```

## Migration Guide

### From Traditional API Routes

**Before:**
```python
# pages/api/todos.py
async def post(request, params):
    data = await request.json()
    # Manual validation and error handling
    # Manual database session management
    return {"result": "created"}
```

**After:**
```python
# Automatic server actions
@server_action()
async def create_todo(title: str, session=None):
    # Automatic validation, error handling, session management
    with session if session else get_session() as db:
        todo = Todo(title=title)
        db.add(todo)
        db.commit()
        return {"id": todo.id, "title": title}
```

### From Client-Side Fetch

**Before:**
```javascript
const response = await fetch('/api/todos', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({title: 'New Todo'})
});
const result = await response.json();
```

**After:**
```javascript
const result = await window.nextpy.executeAction("create_todo", {
    title: "New Todo"
});
```

## Performance Considerations

1. **Server Actions are Fast**: Direct function calls are faster than HTTP requests
2. **WebSocket for Real-Time**: Use WebSocket subscriptions instead of polling
3. **State Caching**: The state manager includes built-in caching
4. **Database Connection Pooling**: Automatic connection pooling via SQLAlchemy
5. **Lazy Loading**: Load data only when needed using server actions

## Security

### Authentication in Server Actions

```python
@server_action()
async def get_user_profile(request, user_id: int):
    # Check authentication
    from nextpy.auth import AuthManager
    token = AuthManager.get_token_from_request(request)
    user = AuthManager.verify_token(token)
    
    # Only allow users to access their own profile
    if user["id"] != user_id:
        raise ServerActionError("Access denied", "FORBIDDEN")
    
    return get_user_data(user_id)
```

### Input Validation
Always validate and sanitize inputs:

```python
@server_action()
async def search_users(query: str):
    # Sanitize query to prevent SQL injection
    if not query or len(query) > 100:
        raise ValidationError("query", "Invalid search query")
    
    # Use parameterized queries (SQLAlchemy does this automatically)
    users = db.query(User).filter(User.username.ilike(f"%{query}%")).all()
    return users
```

## Troubleshooting

### Server Actions Not Working
1. Check that the server action is properly decorated with `@server_action()`
2. Verify the action name matches what you're calling from the client
3. Check browser console for JavaScript errors
4. Ensure the enhanced client runtime is loaded

### WebSocket Connection Issues
1. Check that WebSocket support is enabled in your hosting environment
2. Verify the WebSocket endpoint is accessible
3. Check browser console for WebSocket connection errors
4. Ensure your firewall/proxy allows WebSocket connections

### State Not Syncing
1. Verify that state changes are using `await set_state()` with `broadcast=True`
2. Check that WebSocket connection is established
3. Ensure client subscriptions are properly set up
4. Check browser console for state change events

## Conclusion

NextPy's enhanced full-stack capabilities provide a seamless development experience where you can:

- Write server-side logic in Python
- Call it directly from client-side JavaScript
- Keep everything synchronized in real-time
- Maintain type safety and validation
- Scale effortlessly with the power of FastAPI

This eliminates the traditional boundary between frontend and backend, letting you focus on building great applications rather than managing API integrations.