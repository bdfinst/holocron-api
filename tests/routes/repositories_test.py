"""Repository route tests."""
from pytest import fixture

from app.middleware import auth
from app.routes import repositories
from tests.mocks import crud, request


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(repositories, "repositories_crud", crud)


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(auth, "request", request)
    yield request
    request.reset()


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


def test_list_repositories(client, mock_crud):
    """Test GET /api/v1/repositories endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/repositories")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_repositories_for_team(client, mock_crud, mock_admin):
    """Test GET /api/v1/repositories/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/repositories/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_repositories_for_team_404(client, mock_crud):
    """Test GET /api/v1/repositories/team/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/repositories/team/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_repository(client, mock_crud):
    """Test GET /api/v1/repositories/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/repositories/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_repository_404(client, mock_crud):
    """Test GET /api/v1/repositories/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/repositories/-1")

    assert resp.text == expected
    assert resp.status_code == 404
