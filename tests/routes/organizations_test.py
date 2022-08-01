"""Organization route tests."""
from pytest import fixture

from app.routes import organizations
from tests.mocks import cache, crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(organizations, "organizations_crud", crud)


@fixture
def mock_cache(monkeypatch):
    """Patch cache."""
    monkeypatch.setattr(organizations, "organizations_cache", cache)


def test_list_organizations(client, mock_crud):
    """Test GET /api/v1/organizations endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/organizations")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_organization(client, mock_cache):
    """Test GET /api/v1/teams/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/organizations/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_organization_404(client, mock_cache):
    """Test GET /api/v1/teams/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/organizations/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_create_organization(client, mock_crud):
    """Test POST /api/v1/organizations endpoint."""
    json = {"name": "test"}

    resp = client.post("/api/v1/organizations", json=json)

    assert resp.json == json
    assert resp.status_code == 201


def test_create_organization_validation_error(client, mock_crud):
    """Test POST /api/v1/organizations endpoint."""
    json = {"extra": "field"}
    expected = {
        "name": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.post("/api/v1/organizations", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_create_organization_database_error(client, mock_crud):
    """Test POST /api/v1/organizations endpoint."""
    json = {"name": "error"}
    expected = {"error": "error"}

    resp = client.post("/api/v1/organizations", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_organization(client, mock_crud):
    """Test PUT /api/v1/organizations/1 endpoint."""
    json = {"name": "test"}
    expected = dict(id=1, **json)

    resp = client.put("/api/v1/organizations/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_organization_validation_error(client, mock_crud):
    """Test PUT /api/v1/organizations/1 endpoint."""
    json = {"extra": "field"}
    expected = {
        "name": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.put("/api/v1/organizations/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_organization_database_error(client, mock_crud):
    """Test PUT /api/v1/organizations/1 endpoint."""
    json = {"name": "error"}
    expected = {"error": "error"}

    resp = client.put("/api/v1/organizations/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_delete_organization(client, mock_crud):
    """Test DELETE /api/v1/organizations/1/endpoint."""
    resp = client.delete("/api/v1/organizations/1")

    assert resp.text == ""
    assert resp.status_code == 204
