"""Pipeline route tests."""
from pytest import fixture

from app.routes import pipelines
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(pipelines, "pipelines_crud", crud)


def test_list_pipelines(client, mock_crud):
    """Test GET /api/v1/pipelines endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/pipelines")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_pipelines_for_team(client, mock_crud):
    """Test GET /api/v1/pipelines/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/pipelines/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_pipelines_for_team_404(client, mock_crud):
    """Test GET /api/v1/pipelines/team/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/pipelines/team/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_pipeline(client, mock_crud):
    """Test GET /api/v1/pipelines/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/pipelines/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_pipeline_404(client, mock_crud):
    """Test GET /api/v1/pipelines/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/pipelines/-1")

    assert resp.text == expected
    assert resp.status_code == 404
