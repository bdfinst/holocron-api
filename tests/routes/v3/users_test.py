"""User route tests."""

from pytest import fixture

from app.middleware import auth
from app.routes.v3 import users
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(users, "users_crud", crud)


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


def test_list_users(client, mock_crud, mock_request):
    """Test GET /api/v3/users endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v3/users")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_user(client, mock_crud, mock_request):
    """Test GET /api/v3/users/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v3/users/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_user_404(client, mock_crud, mock_request):
    """Test GET /api/v3/users/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v3/users/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_delete_user(client, mock_crud, mock_admin):
    """Test DELETE /api/v3/users/:id endpoint."""
    resp = client.delete("/api/v3/users/1")

    assert resp.text == ""
    assert resp.status_code == 204
