"""Team route tests."""

from unittest.mock import MagicMock

from pytest import fixture

from app.exceptions import HolocronIntegrityError
from app.middleware import auth, business_logic_teams
from app.routes.v3 import teams
from tests.mocks import MockCRUD, team_history_crud
from tests.testdata import create_team, create_team_view


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    crud = MockCRUD()
    monkeypatch.setattr(teams, "teams_crud", crud)
    monkeypatch.setattr(teams, "team_views_crud", crud)
    monkeypatch.setattr(auth, "teams_crud", crud)
    monkeypatch.setattr(teams, "team_history_crud", team_history_crud)
    yield crud


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


@fixture
def mock_requires_valid_team_data(monkeypatch):
    """Mock requires_valid_team_data decorator."""
    monkeypatch.setattr(
        business_logic_teams,
        "is_valid_team_data_for_create",
        lambda *_, **__: (True, ""),
    )
    monkeypatch.setattr(
        business_logic_teams,
        "is_valid_team_data_for_update",
        lambda *_, **__: (True, ""),
    )


@fixture
def mock_requires_valid_team_view_data(monkeypatch):
    """Mock requires_valid_team_view_data decorator."""
    monkeypatch.setattr(
        business_logic_teams,
        "is_valid_team_view_data_for_create",
        lambda *_, **__: (True, ""),
    )
    monkeypatch.setattr(
        business_logic_teams,
        "is_valid_team_view_data_for_update",
        lambda *_, **__: (True, ""),
    )


def test_list_teams(client, mock_request, mock_crud):
    """Test GET /api/v3/teams endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v3/teams")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_teams_feature_team_views(client, mock_crud, mock_request):
    """Test GET /api/v3/teams endpoint feature team views."""
    expected = {"result": []}
    get_entities_without_team_views = MagicMock(return_value=[])
    mock_crud.get_entities_without_team_views_paginated = (
        get_entities_without_team_views
    )

    resp = client.get("/api/v3/teams")

    assert resp.json == expected
    assert resp.status_code == 200
    get_entities_without_team_views.assert_called_once()


def test_get_team(client, mock_crud, mock_request, monkeypatch):
    """Test GET /api/v3/teams/:id endpoint."""
    expected = {"id": 1}
    monkeypatch.setattr(teams, "FEATURE_FLAGS", {"FEATURE_TEAM_VIEWS": False})

    resp = client.get("/api/v3/teams/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_team_404(client, mock_crud, mock_request, monkeypatch):
    """Test GET /api/v3/teams/:id endpoint."""
    expected = "Resource not found"
    monkeypatch.setattr(teams, "FEATURE_FLAGS", {"FEATURE_TEAM_VIEWS": False})

    resp = client.get("/api/v3/teams/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_team_feature_team_views(client, mock_crud, mock_request):
    """Test GET /api/v3/teams/:id endpoint."""
    expected = {"id": 1}
    get_entity_no_team_view = MagicMock(return_value=expected)
    mock_crud.get_entity_no_team_view = get_entity_no_team_view

    resp = client.get("/api/v3/teams/1")

    assert resp.json == expected
    assert resp.status_code == 200
    get_entity_no_team_view.assert_called_once()


def test_get_team_404_feature_team_views(client, mock_crud, mock_request):
    """Test GET /api/v3/teams/:id endpoint."""
    expected = "Resource not found"
    get_entity_no_team_view = MagicMock(
        side_effect=HolocronIntegrityError("foo", "bar")
    )
    mock_crud.get_entity_no_team_view = get_entity_no_team_view

    resp = client.get("/api/v3/teams/-1")

    assert resp.text == expected
    assert resp.status_code == 404
    get_entity_no_team_view.assert_called_once()


def test_create_team(client, mock_crud, mock_admin, mock_requires_valid_team_data):
    """Test POST /api/v3/teams endpoint."""
    json = {
        "name": "test",
        "valueStreamId": 1,
        "teamSize": 1,
        "userIds": [1],
        "collectorTargetIds": [1],
    }
    mock_crud.create_entity = MagicMock(
        return_value=create_team(
            name="test",
            team_size=1,
            users=[],
            pipelines=[],
            repositories=[],
            ticket_boards=[],
        )
    )

    resp = client.post("/api/v3/teams", json=json)

    expected = {
        "id": 1,
        "name": "test",
        "valueStreamId": 1,
        "teamSize": 1,
        "collectorTargets": [],
        "createdAt": None,
        "updatedAt": None,
        "teamHistory": [],
        "users": [],
        "isWorkflowOnly": False,
        "members": [],
    }

    assert resp.json == expected
    assert resp.status_code == 201


def test_create_team_validation_error(
    client, mock_crud, mock_admin, mock_requires_valid_team_data
):
    """Test POST /api/v3/teams endpoint."""
    MISSING_DATA_MSG = "Missing data for required field."
    UNKNOWN_FIELD_MSG = "Unknown field."
    test_cases = [
        (
            """should show missing and extra fields.""",
            {
                "extra": "field",
            },
            {
                "name": [MISSING_DATA_MSG],
                "userIds": [MISSING_DATA_MSG],
                "teamSize": [MISSING_DATA_MSG],
                "extra": [UNKNOWN_FIELD_MSG],
                "valueStreamId": [MISSING_DATA_MSG],
            },
        ),
        (
            """should show invalid fields.""",
            {
                "name": "",
                "userIds": [],
                "collectorTargetIds": [],
                "teamSize": -1,
            },
            {
                "name": ["String does not match expected pattern."],
                "userIds": ["Shorter than minimum length 1."],
                "teamSize": ["Must be greater than or equal to 1."],
                "valueStreamId": [MISSING_DATA_MSG],
            },
        ),
    ]
    for test_case in test_cases:
        description, input_json, expected_json = test_case

        resp = client.post("/api/v3/teams", json=input_json)

        assert resp.json == expected_json, description
        assert resp.status_code == 400, description


def test_create_team_database_error(
    client, mock_crud, mock_admin, mock_requires_valid_team_data
):
    """Test POST /api/v3/teams endpoint."""
    json = {
        "name": "error",
        "valueStreamId": 1,
        "teamSize": 1,
        "userIds": [1],
        "collectorTargetIds": [1],
    }
    expected = {"error": "error"}

    resp = client.post("/api/v3/teams", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_team(client, mock_crud, mock_admin, mock_requires_valid_team_data):
    """Test PUT /api/v3/teams/1 endpoint."""
    json = {
        "name": "test2",
        "valueStreamId": 1,
        "teamSize": 1,
        "userIds": [1],
        "collectorTargetIds": [1],
    }
    expected = dict(
        id=1,
        collectorTargets=[],
        createdAt=None,
        updatedAt=None,
        users=[],
        isWorkflowOnly=False,
        teamHistory=[],
        name="test2",
        teamSize=1,
        valueStreamId=1,
        members=[],
    )
    mock_crud.get_entity = MagicMock(return_value=create_team(team_size=1))
    mock_crud.update_entity = MagicMock(
        return_value=create_team(
            team_size=1,
            name="test2",
            pipelines=[],
            repositories=[],
            ticket_boards=[],
            users=[],
        )
    )

    resp = client.put("/api/v3/teams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_team_validation_error(
    client, mock_crud, mock_admin, mock_requires_valid_team_data
):
    """Test PUT /api/v3/teams/1 endpoint."""
    MISSING_DATA_MSG = "Missing data for required field."
    UNKNOWN_FIELD_MSG = "Unknown field."
    test_cases = [
        (
            """should show missing and extra fields.""",
            {
                "extra": "field",
            },
            {
                "name": [MISSING_DATA_MSG],
                "userIds": [MISSING_DATA_MSG],
                "teamSize": [MISSING_DATA_MSG],
                "extra": [UNKNOWN_FIELD_MSG],
                "valueStreamId": [MISSING_DATA_MSG],
            },
        ),
        (
            """should show invalid fields.""",
            {
                "name": "",
                "userIds": [],
                "collectorTargetIds": [],
                "teamSize": -1,
            },
            {
                "name": ["String does not match expected pattern."],
                "userIds": ["Shorter than minimum length 1."],
                "teamSize": ["Must be greater than or equal to 1."],
                "valueStreamId": [MISSING_DATA_MSG],
            },
        ),
    ]
    for test_case in test_cases:
        description, input_json, expected_json = test_case

        resp = client.put("/api/v3/teams/1", json=input_json)

        assert resp.json == expected_json, description
        assert resp.status_code == 400, description


def test_update_team_database_error(
    client, mock_crud, mock_admin, mock_requires_valid_team_data
):
    """Test PUT /api/v3/teams/1 endpoint."""
    json = {
        "name": "error",
        "valueStreamId": 1,
        "teamSize": 1,
        "userIds": [1],
        "collectorTargetIds": [1],
    }
    expected = {"error": "error"}

    mock_crud.get_entity = MagicMock(return_value=create_team(name="error"))

    resp = client.put("/api/v3/teams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_delete_team(client, mock_crud, mock_admin):
    """Test DELETE /api/v3/teams/1 endpoint."""
    resp = client.delete("/api/v3/teams/1")

    assert resp.text == ""
    assert resp.status_code == 204


def test_list_team_views(
    client,
    mock_request,
    mock_crud,
):
    """Test GET /api/v3/teams/views endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v3/teams/views")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_team_view(
    client,
    mock_crud,
    mock_request,
):
    """Test GET /api/v3/teams/views/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v3/teams/views/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_team_view_404(
    client,
    mock_crud,
    mock_request,
):
    """Test GET /api/v3/teams/views/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v3/teams/views/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_create_team_view(
    client,
    mock_crud,
    mock_admin,
    mock_request,
    mock_requires_valid_team_view_data,
):
    """Test POST /api/v3/teams/views endpoint."""
    json = {"name": "test_view", "collectorTargetIds": [1], "viewOwnerId": 1}

    mock_crud.create_entity = MagicMock(
        return_value=create_team(
            id=2,
            name="test_view",
            team_size=1,
            users=[],
            pipelines=[],
            projects=[],
            repositories=[],
            ticket_boards=[],
            view_owner_id=1,
            value_stream_id=1,
        )
    )

    resp = client.post("/api/v3/teams/views", json=json)

    expected = {
        "id": 2,
        "name": "test_view",
        "collectorTargets": [],
        "createdAt": None,
        "updatedAt": None,
        "isWorkflowOnly": False,
        "viewOwnerId": 1,
    }

    assert resp.json == expected
    assert resp.status_code == 201


def test_create_team_view_database_error(
    client, mock_crud, mock_admin, mock_request, mock_requires_valid_team_view_data
):
    """Test POST /api/v3/teams/views endpoint."""
    json = {
        "name": "error",
        "viewOwnerId": 1,
        "collectorTargetIds": [1],
    }
    expected = {"error": "error"}

    resp = client.post("/api/v3/teams/views", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_team_view(
    client, mock_crud, mock_admin, mock_requires_valid_team_view_data
):
    """Test PUT /api/v3/teams/1 endpoint."""
    json = {"name": "test_view2", "collectorTargetIds": [1], "viewOwnerId": 1}
    expected = dict(
        id=2,
        collectorTargets=[],
        createdAt=None,
        updatedAt=None,
        isWorkflowOnly=False,
        name="test_view2",
        viewOwnerId=1,
    )

    mock_crud.update_entity = MagicMock(
        return_value=create_team_view(
            name="test_view2",
            pipelines=[],
            projects=[],
            repositories=[],
            ticket_boards=[],
            view_owner_id=1,
        )
    )

    resp = client.put("/api/v3/teams/views/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_team_view_validation_error(
    client, mock_crud, mock_admin, mock_requires_valid_team_view_data
):
    """Test PUT /api/v3/teams/views/1 endpoint."""
    MISSING_DATA_MSG = "Missing data for required field."
    UNKNOWN_FIELD_MSG = "Unknown field."
    test_cases = [
        (
            """should show missing and extra fields.""",
            {
                "extra": "field",
            },
            {
                "name": [MISSING_DATA_MSG],
                "viewOwnerId": [MISSING_DATA_MSG],
                "extra": [UNKNOWN_FIELD_MSG],
            },
        ),
        (
            """should show invalid fields.""",
            {
                "name": "",
                "collectorTargetIds": [],
                "viewOwnerId": "invalid",
            },
            {
                "name": ["String does not match expected pattern."],
                "viewOwnerId": ["Not a valid integer."],
            },
        ),
    ]
    for test_case in test_cases:
        description, input_json, expected_json = test_case

        resp = client.put("/api/v3/teams/views/1", json=input_json)

        assert resp.json == expected_json, description
        assert resp.status_code == 400, description


def test_update_team_view_database_error(
    client, mock_crud, monkeypatch, mock_admin, mock_requires_valid_team_view_data
):
    """Test PUT /api/v3/teams/views/1 endpoint."""
    json = {"name": "error", "collectorTargetIds": [1], "viewOwnerId": 1}
    expected = {"error": "error"}

    resp = client.put("/api/v3/teams/views/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_delete_team_view(
    client,
    mock_crud,
    mock_admin,
):
    """Test DELETE /api/v3/teams/views/1 endpoint."""
    resp = client.delete("/api/v3/teams/1")

    assert resp.text == ""
    assert resp.status_code == 204
