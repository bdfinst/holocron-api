"""Builds route tests."""
from pytest import fixture

from app.routes import builds
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(builds, "builds_crud", crud)


def test_list_builds_for_team(client, mock_crud):
    """Test GET /api/v1/builds/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/builds/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_builds_for_team_404(client, mock_crud):
    """Test GET /api/v1/builds/team/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/builds/team/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_build(client, mock_crud):
    """Test GET /api/v1/builds/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/builds/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_build_404(client, mock_crud):
    """Test GET /api/v1/builds/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/builds/-1")

    assert resp.text == expected
    assert resp.status_code == 404
