"""
NextPy Routing Tests
"""

import pytest
from fastapi.testclient import TestClient
from nextpy.server.app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app(debug=True)
    return TestClient(app)


def test_home_page(client):
    """Test home page loads"""
    response = client.get("/")
    assert response.status_code == 200
    assert "NextPy" in response.text


def test_about_page(client):
    """Test about page loads"""
    response = client.get("/about")
    assert response.status_code == 200


def test_api_health(client):
    """Test health API endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_posts(client):
    """Test posts API endpoint"""
    response = client.get("/api/posts")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert isinstance(data["posts"], list)


def test_404_not_found(client):
    """Test 404 error handling"""
    response = client.get("/nonexistent")
    assert response.status_code == 404
