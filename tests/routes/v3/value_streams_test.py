"""Value stream route tests."""

from unittest.mock import MagicMock

from pytest import fixture

from app.exceptions import HolocronIntegrityError
from app.middleware import auth
from app.routes.v3 import value_streams
from tests.mocks import MockCRUD


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    crud = MockCRUD()
    monkeypatch.setattr(value_streams, "value_streams_crud", crud)
    monkeypatch.setattr(auth, "value_streams_crud", crud)
    yield crud


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


@fixture
def mock_feature_team_views_true(monkeypatch):
    """Mock FEATURE_TEAM_VIEWS as true."""
    monkeypatch.setattr(value_streams, "FEATURE_FLAGS", {"FEATURE_TEAM_VIEWS": True})


@fixture
def mock_feature_team_views_false(monkeypatch):
    """Mock FEATURE_TEAM_VIEWS as false."""
    monkeypatch.setattr(value_streams, "FEATURE_FLAGS", {"FEATURE_TEAM_VIEWS": False})


def test_list_value_streams(
    client, mock_crud, mock_request, mock_feature_team_views_false
):
    """Test GET /api/v3/value-streams endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v3/value-streams")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_value_streams_team_views(
    client, mock_request, mock_crud, mock_feature_team_views_true
):
    """Test GET /api/v3/value-streams endpoint team view feature."""
    expected = {"result": []}
    get_entities_without_team_views = MagicMock(return_value=[])
    mock_crud.get_entities_without_team_views_paginated = (
        get_entities_without_team_views
    )

    resp = client.get("/api/v3/value-streams")

    assert resp.json == expected
    assert resp.status_code == 200
    get_entities_without_team_views.assert_called_once()


def test_get_value_stream(
    client, mock_crud, mock_request, mock_feature_team_views_false
):
    """Test GET /api/v3/value-streams/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v3/value-streams/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_value_stream_404(
    client, mock_crud, mock_request, mock_feature_team_views_false
):
    """Test GET /api/v3/value-streams/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v3/value-streams/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_value_stream_feature_team_views(
    client, mock_request, mock_crud, mock_feature_team_views_true
):
    """Test GET /api/v3/value-streams/:id endpoint feature team views."""
    expected = {"id": 1}
    get_entity_without_team_views = MagicMock(return_value=expected)
    mock_crud.get_entity_without_team_views = get_entity_without_team_views

    resp = client.get("/api/v3/value-streams/1")

    assert resp.json == expected
    assert resp.status_code == 200
    get_entity_without_team_views.assert_called_once()


def test_get_value_stream_404_feature_team_views(
    client, mock_request, mock_crud, mock_feature_team_views_true
):
    """Test GET /api/v3/value-streams/:id endpoint feature team views."""
    expected = "Resource not found"
    get_entity_without_team_views = MagicMock(
        side_effect=HolocronIntegrityError("foo", "bar")
    )
    mock_crud.get_entity_without_team_views = get_entity_without_team_views

    resp = client.get("/api/v3/value-streams/-1")

    assert resp.text == expected
    assert resp.status_code == 404
    get_entity_without_team_views.assert_called_once()


def test_create_value_stream(client, mock_crud, mock_admin):
    """Test POST /api/v3/value-streams endpoint."""
    json = {"name": "test", "organizationId": 1, "userIds": [1]}
    expected = {"name": "test", "organizationId": 1}

    resp = client.post("/api/v3/value-streams", json=json)

    assert resp.json == expected
    assert resp.status_code == 201


def test_create_value_stream_validation_error(client, mock_crud, mock_admin):
    """Test POST /api/v3/value-streams endpoint."""
    json = {"name": "test", "extra": "field", "userIds": [1]}
    expected = {
        "organizationId": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.post("/api/v3/value-streams", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_create_value_stream_database_error(client, mock_crud, mock_admin):
    """Test POST /api/v3/value-streams endpoint."""
    json = {"name": "error", "organizationId": 1, "userIds": [1]}
    expected = {"error": "error"}

    resp = client.post("/api/v3/value-streams", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_value_stream(client, mock_crud, mock_admin):
    """Test PUT /api/v3/value-streams/1 endpoint."""
    json = {"name": "test", "organizationId": 1, "userIds": [1]}
    expected = {"id": 1, "name": "test", "organizationId": 1}

    resp = client.put("/api/v3/value-streams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_value_stream_validation_error(client, mock_crud, mock_admin):
    """Test PUT /api/v3/value-streams/1 endpoint."""
    json = {"name": "test", "extra": "field", "userIds": [1]}
    expected = {
        "organizationId": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.put("/api/v3/value-streams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_value_stream_database_error(client, mock_crud, mock_admin):
    """Test PUT /api/v3/value-streams/1 endpoint."""
    json = {"name": "error", "organizationId": 1, "userIds": [1]}
    expected = {"error": "error"}

    resp = client.put("/api/v3/value-streams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_delete_value_stream(client, mock_crud, mock_admin):
    """Test DELETE /api/v3/value-streams/1/endpoint."""
    resp = client.delete("/api/v3/value-streams/1")

    assert resp.text == ""
    assert resp.status_code == 204
