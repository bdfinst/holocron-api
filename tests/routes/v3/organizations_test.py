"""Organization route tests."""

from unittest.mock import MagicMock

from pytest import fixture

from app.exceptions import HolocronIntegrityError
from app.middleware import auth
from app.routes.v3 import organizations
from tests.mocks import MockCRUD


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    crud = MockCRUD()
    monkeypatch.setattr(organizations, "organizations_crud", crud)
    monkeypatch.setattr(auth, "organizations_crud", crud)
    yield crud


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


def test_list_organizations(client, mock_crud, mock_request):
    """Test GET /api/v3/organizations endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v3/organizations")

    assert resp.json == expected
    assert resp.status_code == 200


# def test_list_organizations_team_views(
#     client, mock_crud, mock_request
# ):
#     """Test GET /api/v3/organizations endpoint team views feature."""
#     expected = {"result": []}
#     get_entities_without_team_views = MagicMock(return_value=[])
#     mock_crud.get_entities_without_team_views_paginated = (
#         get_entities_without_team_views
#     )

#     resp = client.get("/api/v3/organizations")

#     assert resp.json == expected
#     assert resp.status_code == 200
#     get_entities_without_team_views.assert_called_once()


def test_get_organization(client, mock_crud, mock_request):
    """Test GET /api/v3/organizations/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v3/organizations/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_organization_404(client, mock_crud, mock_request):
    """Test GET /api/v3/organizations/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v3/organizations/-1")

    assert resp.text == expected
    assert resp.status_code == 404


# def test_get_organization_feature_team_views(
#     client,
#     mock_request,
#     mock_crud,
# ):
#     """Test GET /api/v3/organizations/:id endpoint team views feature."""
#     expected = {"id": 1}
#     get_entity_without_team_views = MagicMock(return_value=expected)
#     mock_crud.get_entity_without_team_views = get_entity_without_team_views

#     resp = client.get("/api/v3/organizations/1")

#     assert resp.json == expected
#     assert resp.status_code == 200
#     get_entity_without_team_views.assert_called_once()


# def test_get_organization_feature_team_views_404(
#     client,
#     mock_request,
#     mock_crud,
# ):
#     """Test GET /api/v3/organizations/:id endpoint team views feature."""
#     expected = "Resource not found"
#     get_entity_without_team_views = MagicMock(
#         side_effect=HolocronIntegrityError("foo", "bar")
#     )
#     mock_crud.get_entity_without_team_views = get_entity_without_team_views

#     resp = client.get("/api/v3/organizations/1")

#     assert resp.text == expected
#     assert resp.status_code == 404
#     get_entity_without_team_views.assert_called_once()


def test_create_organization(client, mock_crud, mock_admin):
    """Test POST /api/v3/organizations endpoint."""
    json = {"name": "test", "userIds": [1]}
    expected = {"name": "test"}

    resp = client.post("/api/v3/organizations", json=json)

    assert resp.json == expected
    assert resp.status_code == 201


def test_create_organization_validation_error(client, mock_crud, mock_admin):
    """Test POST /api/v3/organizations endpoint."""
    json = {"extra": "field", "userIds": [1]}
    expected = {
        "name": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.post("/api/v3/organizations", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_create_organization_database_error(client, mock_crud, mock_admin):
    """Test POST /api/v3/organizations endpoint."""
    json = {"name": "error", "userIds": [1]}
    expected = {"error": "error"}

    resp = client.post("/api/v3/organizations", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_organization(client, mock_crud, mock_admin):
    """Test PUT /api/v3/organizations/1 endpoint."""
    json = {"name": "test", "userIds": [1]}
    expected = {"id": 1, "name": "test"}

    resp = client.put("/api/v3/organizations/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_organization_validation_error(client, mock_crud, mock_admin):
    """Test PUT /api/v3/organizations/1 endpoint."""
    json = {"extra": "field", "userIds": [1]}
    expected = {
        "name": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.put("/api/v3/organizations/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_organization_database_error(client, mock_crud, mock_admin):
    """Test PUT /api/v3/organizations/1 endpoint."""
    json = {"name": "error", "userIds": [1]}
    expected = {"error": "error"}

    resp = client.put("/api/v3/organizations/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_delete_organization(client, mock_crud, mock_admin):
    """Test DELETE /api/v3/organizations/1/endpoint."""
    resp = client.delete("/api/v3/organizations/1")

    assert resp.text == ""
    assert resp.status_code == 204
