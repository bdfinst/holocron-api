"""Team route tests."""
from unittest.mock import MagicMock

from pytest import fixture

from app.models import Team
from app.routes import teams
from tests.mocks import crud, team_history_crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(teams, "teams_crud", crud)
    monkeypatch.setattr(teams, "team_history_crud", team_history_crud)


def test_list_teams(client, mock_crud):
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

    resp = client.get("/api/v1/teams/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_create_team(client, mock_crud, monkeypatch):
    """Test POST /api/v1/teams endpoint."""
    json = {"name": "test", "valuestreamId": 1, "teamSize": 1}

    monkeypatch.setattr(
        teams.teams_crud,
        "create_entity",
        MagicMock(return_value=Team(id=1, team_size=1, name="test", valuestream_id=1)),
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
        "users": [],
    }

    assert resp.json == expected
    assert resp.status_code == 201


def test_create_team_validation_error(client, mock_crud):
    """Test POST /api/v1/teams endpoint."""
    json = {"name": "test", "valuestreamId": 1, "extra": "field"}
    expected = {
        "teamSize": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.post("/api/v1/teams", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_create_team_database_error(client, mock_crud):
    """Test POST /api/v1/teams endpoint."""
    json = {"name": "error", "valuestreamId": 1, "teamSize": 1}
    expected = {"error": "error"}

    resp = client.post("/api/v1/teams", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_team(client, mock_crud, monkeypatch):
    """Test PUT /api/v1/teams/1 endpoint."""
    json = {"name": "test2", "valuestreamId": 1, "teamSize": 1}
    expected = dict(
        id=1, collectorTargets=[], createdAt=None, updatedAt=None, users=[], **json
    )

    monkeypatch.setattr(
        teams.teams_crud,
        "get_entity",
        MagicMock(return_value=Team(id=1, team_size=1, name="test", valuestream_id=1)),
    )
    monkeypatch.setattr(
        teams.teams_crud,
        "update_entity",
        MagicMock(return_value=Team(id=1, team_size=1, name="test2", valuestream_id=1)),
    )

    resp = client.put("/api/v1/teams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_team_validation_error(client, mock_crud):
    """Test PUT /api/v1/teams/1 endpoint."""
    expected = {
        "teamSize": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }
    json = {"name": "test", "valuestreamId": 1, "extra": "field"}

    resp = client.put("/api/v1/teams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_team_database_error(client, mock_crud):
    """Test PUT /api/v1/teams/1 endpoint."""
    json = {"name": "error", "valuestreamId": 1, "teamSize": 1}
    expected = {"error": "error"}

    resp = client.put("/api/v1/teams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_delete_team(client, mock_crud):
    """Test DELETE /api/v1/teams/1 endpoint."""
    resp = client.delete("/api/v1/teams/1")

    assert resp.text == ""
    assert resp.status_code == 204
