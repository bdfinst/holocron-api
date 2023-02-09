"""Team route tests."""
from unittest.mock import MagicMock

from pytest import fixture

from app.middleware import auth
from app.routes import teams
from tests.mocks import crud, request, team_history_crud
from tests.testdata import create_team


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(teams, "teams_crud", crud)
    monkeypatch.setattr(auth, "teams_crud", crud)
    monkeypatch.setattr(teams, "team_history_crud", team_history_crud)


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


def test_list_teams(client, mock_request, mock_crud):
    """Test GET /api/v1/teams endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/teams")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_team(client, mock_crud):
    """Test GET /api/v1/teams/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/teams/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_team_404(client, mock_crud):
    """Test GET /api/v1/teams/:id endpoint."""
    expected = "Resource not found"

    # did not mock admin, we want requires_team_access to catch the error
    resp = client.get("/api/v1/teams/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_create_team(client, mock_crud, monkeypatch, mock_admin):
    """Test POST /api/v1/teams endpoint."""
    json = {
        "name": "test",
        "valuestreamId": 1,
        "teamSize": 1,
        "userIds": [1],
        "collectorTargetIds": [1],
    }

    monkeypatch.setattr(
        teams.teams_crud,
        "create_entity",
        MagicMock(
            return_value=create_team(
                name="test",
                team_size=1,
                users=[],
                pipelines=[],
                repositories=[],
                ticket_boards=[],
            )
        ),
    )

    resp = client.post("/api/v1/teams", json=json)

    expected = {
        "id": 1,
        "name": "test",
        "valuestreamId": 1,
        "teamSize": 1,
        "collectorTargets": [],
        "createdAt": None,
        "updatedAt": None,
        "teamHistory": [],
        "users": [],
        "isWorkflowOnly": False,
    }

    assert resp.json == expected
    assert resp.status_code == 201


def test_create_team_validation_error(client, mock_crud, mock_admin):
    """Test POST /api/v1/teams endpoint."""
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
                "collectorTargetIds": [MISSING_DATA_MSG],
                "teamSize": [MISSING_DATA_MSG],
                "extra": [UNKNOWN_FIELD_MSG],
                "valuestreamId": [MISSING_DATA_MSG],
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
                "collectorTargetIds": ["Shorter than minimum length 1."],
                "teamSize": ["Must be greater than or equal to 1."],
                "valuestreamId": [MISSING_DATA_MSG],
            },
        ),
    ]
    for test_case in test_cases:
        description, input_json, expected_json = test_case

        resp = client.post("/api/v1/teams", json=input_json)

        assert resp.json == expected_json, description
        assert resp.status_code == 400, description


def test_create_team_database_error(client, mock_crud, mock_admin):
    """Test POST /api/v1/teams endpoint."""
    json = {
        "name": "error",
        "valuestreamId": 1,
        "teamSize": 1,
        "userIds": [1],
        "collectorTargetIds": [1],
    }
    expected = {"error": "error"}

    resp = client.post("/api/v1/teams", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_team(client, mock_crud, monkeypatch, mock_admin):
    """Test PUT /api/v1/teams/1 endpoint."""
    json = {
        "name": "test2",
        "valuestreamId": 1,
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
        valuestreamId=1,
    )

    monkeypatch.setattr(
        teams.teams_crud,
        "get_entity",
        MagicMock(return_value=create_team(team_size=1)),
    )
    monkeypatch.setattr(
        teams.teams_crud,
        "update_entity",
        MagicMock(
            return_value=create_team(
                team_size=1,
                name="test2",
                pipelines=[],
                repositories=[],
                ticket_boards=[],
                users=[],
            )
        ),
    )

    resp = client.put("/api/v1/teams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_team_validation_error(client, mock_crud, mock_admin):
    """Test PUT /api/v1/teams/1 endpoint."""
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
                "collectorTargetIds": [MISSING_DATA_MSG],
                "teamSize": [MISSING_DATA_MSG],
                "extra": [UNKNOWN_FIELD_MSG],
                "valuestreamId": [MISSING_DATA_MSG],
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
                "collectorTargetIds": ["Shorter than minimum length 1."],
                "teamSize": ["Must be greater than or equal to 1."],
                "valuestreamId": [MISSING_DATA_MSG],
            },
        ),
    ]
    for test_case in test_cases:
        description, input_json, expected_json = test_case

        resp = client.put("/api/v1/teams/1", json=input_json)

        assert resp.json == expected_json, description
        assert resp.status_code == 400, description


def test_update_team_database_error(client, mock_crud, monkeypatch, mock_admin):
    """Test PUT /api/v1/teams/1 endpoint."""
    json = {
        "name": "error",
        "valuestreamId": 1,
        "teamSize": 1,
        "userIds": [1],
        "collectorTargetIds": [1],
    }
    expected = {"error": "error"}

    monkeypatch.setattr(
        teams.teams_crud,
        "get_entity",
        MagicMock(
            return_value=create_team(
                name="error",
            )
        ),
    )

    resp = client.put("/api/v1/teams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_delete_team(client, mock_crud, mock_admin):
    """Test DELETE /api/v1/teams/1 endpoint."""
    resp = client.delete("/api/v1/teams/1")

    assert resp.text == ""
    assert resp.status_code == 204
