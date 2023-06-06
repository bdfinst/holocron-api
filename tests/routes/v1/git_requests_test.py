"""Git Request route tests."""
from pytest import fixture

from app.middleware import auth, log
from app.routes.v1 import git_requests
from tests.mocks import crud, request


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(git_requests, "git_requests_crud", crud)


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(auth, "request", request)
    monkeypatch.setattr(log, "request", request)
    yield request
    request.reset()


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


def test_list_git_requests_for_team(client, mock_crud, mock_admin):
    """Test GET /api/v1/gitrequests/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/gitrequests/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_get_requests_for_team_404(client, mock_crud, mock_request):
    """Test GET /api/v1/gitrequests/team/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/gitrequests/team/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_git_request(client, mock_crud, mock_admin):
    """Test GET /api/v1/gitrequests/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/gitrequests/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_git_request_404(client, mock_crud, mock_admin):
    """Test GET /api/v1/gitrequests/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/gitrequests/-1")

    assert resp.text == expected
    assert resp.status_code == 404
