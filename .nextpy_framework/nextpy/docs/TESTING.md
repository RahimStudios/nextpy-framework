# Testing in NextPy

NextPy comes with pytest setup for testing your application.

## Setup

```bash
pip install pytest pytest-asyncio
```

## Writing Tests

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

@pytest.mark.asyncio
async def test_async_page(client):
    response = client.get("/about")
    assert response.status_code == 200
```

## Running Tests

```bash
pytest tests/ -v
pytest tests/test_pages.py::test_home_page
pytest --cov=nextpy  # With coverage
```

## Testing API Routes

```python
def test_api_endpoint(client):
    response = client.post("/api/users", json={
        "name": "John",
        "email": "john@example.com"
    })
    assert response.status_code == 200
    assert response.json()["success"] == True
```

## Testing with Database

```python
def test_create_user(client):
    from nextpy.db import get_session, User
    
    session = get_session()
    user = User(email="test@example.com", username="test")
    session.add(user)
    session.commit()
    
    assert user.id is not None
    session.close()
```
