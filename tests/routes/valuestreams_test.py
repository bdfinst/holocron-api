"""Valuestream route tests."""
from pytest import fixture

from app.middleware import auth
from app.routes import valuestreams
from tests.mocks import crud, request


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(auth, "request", request)
    yield request
    request.reset()


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(valuestreams, "valuestreams_crud", crud)
    monkeypatch.setattr(auth, "valuestreams_crud", crud)


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


@fixture
def mock_non_admin(monkeypatch, mock_request):
    """Mock a non admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})


def test_list_valuestreams(client, mock_crud):
    """Test GET /api/v1/valuestreams endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/valuestreams")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_valuestream(client, mock_crud, mock_admin):
    """Test GET /api/v1/valuestreams/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/valuestreams/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_valuestream_404(client, mock_crud, mock_non_admin):
    """Test GET /api/v1/valuestreams/:id endpoint."""
    expected = "Resource not found"

    # did not mock admin, we want requires_vs_access to catch this error
    resp = client.get("/api/v1/valuestreams/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_create_valuestream(client, mock_crud, mock_admin):
    """Test POST /api/v1/valuestreams endpoint."""
    json = {"name": "test", "organizationId": 1, "userIds": [1]}
    expected = {"name": "test", "organizationId": 1}

    resp = client.post("/api/v1/valuestreams", json=json)

    assert resp.json == expected
    assert resp.status_code == 201


def test_create_valuestream_validation_error(client, mock_crud, mock_admin):
    """Test POST /api/v1/valuestreams endpoint."""
    json = {"name": "test", "extra": "field", "userIds": [1]}
    expected = {
        "organizationId": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.post("/api/v1/valuestreams", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_create_valuestream_database_error(client, mock_crud, mock_admin):
    """Test POST /api/v1/valuestreams endpoint."""
    json = {"name": "error", "organizationId": 1, "userIds": [1]}
    expected = {"error": "error"}

    resp = client.post("/api/v1/valuestreams", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_valuestream(client, mock_crud, mock_admin):
    """Test PUT /api/v1/valuestreams/1 endpoint."""
    json = {"name": "test", "organizationId": 1, "userIds": [1]}
    expected = {"id": 1, "name": "test", "organizationId": 1}

    resp = client.put("/api/v1/valuestreams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_valuestream_validation_error(client, mock_crud, mock_admin):
    """Test PUT /api/v1/valuestreams/1 endpoint."""
    json = {"name": "test", "extra": "field", "userIds": [1]}
    expected = {
        "organizationId": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.put("/api/v1/valuestreams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_valuestream_database_error(client, mock_crud, mock_admin):
    """Test PUT /api/v1/valuestreams/1 endpoint."""
    json = {"name": "error", "organizationId": 1, "userIds": [1]}
    expected = {"error": "error"}

    resp = client.put("/api/v1/valuestreams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_delete_valuestream(client, mock_crud, mock_admin):
    """Test DELETE /api/v1/valuestreams/1/endpoint."""
    resp = client.delete("/api/v1/valuestreams/1")

    assert resp.text == ""
    assert resp.status_code == 204
