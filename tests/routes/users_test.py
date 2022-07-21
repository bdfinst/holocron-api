"""User route tests."""
from pytest import fixture

from app.routes import users
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(users, "users_crud", crud)


def test_list_users(client, mock_crud):
    """Test GET /api/v1/users endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/users")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_user(client, mock_crud):
    """Test GET /api/v1/users/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/users/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_user_404(client, mock_crud):
    """Test GET /api/v1/users/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/users/-1")

    assert resp.text == expected
    assert resp.status_code == 404
