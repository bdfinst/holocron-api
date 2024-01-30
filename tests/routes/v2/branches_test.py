"""Branch route tests."""

from pytest import fixture

from app.middleware import auth
from app.routes.v2 import branches
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(branches, "branches_crud", crud)


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


def test_list_branches_for_team(client, mock_crud, mock_admin):
    """Test GET /api/v2/branches/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v2/branches/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_branches_for_team_404(client, mock_crud, mock_request):
    """Test GET /api/v2/branches/team/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v2/branches/team/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_branch(client, mock_crud, mock_admin):
    """Test GET /api/v2/branches/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v2/branches/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_branch_404(client, mock_crud, mock_admin):
    """Test GET /api/v2/branches/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v2/branches/-1")

    assert resp.text == expected
    assert resp.status_code == 404
