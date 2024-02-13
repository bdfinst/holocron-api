"""Collector route tests."""

from unittest.mock import MagicMock

from pytest import fixture

from app.exceptions import HolocronIntegrityError
from app.middleware import auth
from app.routes.v2 import collectors
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(collectors, "collectors_crud", crud)


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


def test_list_collectors(client, mock_crud, mock_request):
    """Test GET /api/v2/collectors endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v2/collectors")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_collector(client, mock_crud, mock_request):
    """Test GET /api/v2/collectors/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v2/collectors/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_collector_404(client, mock_crud, mock_request):
    """Test GET /api/v2/collectors/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v2/collectors/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_update_collector(client, mock_crud, mock_admin):
    """Test PUT /api/v2/collectors/:id endpoint."""
    json = {
        "collectorIntervalSeconds": 0,
        "collectorTargetsIntrvlSecs": 0,
        "lookBackDays": 0,
        "maxRequestsPerMinute": 0,
        "name": "test",
        "target": "test",
    }
    expected = {
        "id": 1,
        "collectorIntervalSeconds": 0,
        "collectorTargetsIntrvlSecs": 0,
        "lookBackDays": 0,
        "maxRequestsPerMinute": 0,
        "name": "test",
        "target": "test",
    }

    resp = client.put("/api/v2/collectors/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_collector_validation_error(client, mock_crud, mock_admin):
    """Test PUT /api/v2/collectors/:id endpoint."""
    json = {
        "extra": "field",
        "collectorIntervalSeconds": 0,
        "collectorTargetsIntrvlSecs": 0,
        "lookBackDays": 0,
        "maxRequestsPerMinute": 0,
        "name": "test",
    }
    expected = {
        "target": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.put("/api/v2/collectors/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_collector_database_error(client, mock_crud, mock_admin):
    """Test PUT /api/v2/collectors/:id endpoint."""
    json = {
        "collectorIntervalSeconds": 0,
        "collectorTargetsIntrvlSecs": 0,
        "lookBackDays": 0,
        "maxRequestsPerMinute": 0,
        "name": "error",
        "target": "test",
    }
    expected = {"error": "error"}

    resp = client.put("/api/v2/collectors/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400
