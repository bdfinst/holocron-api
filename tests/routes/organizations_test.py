"""Organization route tests."""
from pytest import fixture

from app import security
from app.middleware import auth, log
from app.routes import organizations
from tests.mocks import crud, request


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(auth, "request", request)
    monkeypatch.setattr(log, "request", request)
    monkeypatch.setattr(security, "request", request)
    yield request
    request.reset()


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(organizations, "organizations_crud", crud)
    monkeypatch.setattr(auth, "organizations_crud", crud)


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


def test_list_organizations(client, mock_crud, mock_request):
    """Test GET /api/v1/organizations endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/organizations")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_organization(client, mock_crud, mock_request):
    """Test GET /api/v1/teams/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/organizations/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_organization_404(client, mock_crud, mock_request):
    """Test GET /api/v1/teams/:id endpoint."""
    expected = "Resource not found"

    # did not mock admin, we want requires_org_access to catch the error
    resp = client.get("/api/v1/organizations/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_create_organization(client, mock_crud, mock_admin):
    """Test POST /api/v1/organizations endpoint."""
    json = {"name": "test", "userIds": [1]}
    expected = {"name": "test"}

    resp = client.post("/api/v1/organizations", json=json)

    assert resp.json == expected
    assert resp.status_code == 201


def test_create_organization_validation_error(client, mock_crud, mock_admin):
    """Test POST /api/v1/organizations endpoint."""
    json = {"extra": "field", "userIds": [1]}
    expected = {
        "name": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.post("/api/v1/organizations", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_create_organization_database_error(client, mock_crud, mock_admin):
    """Test POST /api/v1/organizations endpoint."""
    json = {"name": "error", "userIds": [1]}
    expected = {"error": "error"}

    resp = client.post("/api/v1/organizations", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_organization(client, mock_crud, mock_admin):
    """Test PUT /api/v1/organizations/1 endpoint."""
    json = {"name": "test", "userIds": [1]}
    expected = {"id": 1, "name": "test"}

    resp = client.put("/api/v1/organizations/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_organization_validation_error(client, mock_crud, mock_admin):
    """Test PUT /api/v1/organizations/1 endpoint."""
    json = {"extra": "field", "userIds": [1]}
    expected = {
        "name": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.put("/api/v1/organizations/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_organization_database_error(client, mock_crud, mock_admin):
    """Test PUT /api/v1/organizations/1 endpoint."""
    json = {"name": "error", "userIds": [1]}
    expected = {"error": "error"}

    resp = client.put("/api/v1/organizations/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_delete_organization(client, mock_crud, mock_admin):
    """Test DELETE /api/v1/organizations/1/endpoint."""
    resp = client.delete("/api/v1/organizations/1")

    assert resp.text == ""
    assert resp.status_code == 204
