# Authentication in NextPy

NextPy provides built-in JWT and session-based authentication.

## JWT Authentication

### Create Token

```python
from nextpy.auth import AuthManager

token = AuthManager.create_token(user_id=123)
```

### Verify Token

```python
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

## Session Authentication

```python
from nextpy.auth import create_session, get_session, delete_session

# Create session
session_id = create_session(user_id=123)

# Get session
session = get_session(session_id)

# Delete session
delete_session(session_id)
```

## Login Example

```python
# pages/api/login.py
from nextpy.auth import AuthManager

async def post(request):
    data = await request.json()
    # Verify credentials...
    token = AuthManager.create_token(user_id=user.id)
    return {"token": token}
```

## Frontend Usage

```html
<script>
// Store token
localStorage.setItem('token', response.token);

// Send with requests
fetch('/api/protected', {
    headers: {'Authorization': `Bearer ${localStorage.getItem('token')}`}
});
</script>
```

## Configuration

```bash
# .env
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
SESSION_SECRET=your-session-secret
```
