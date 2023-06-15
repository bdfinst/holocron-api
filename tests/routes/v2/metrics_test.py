"""Metrics route tests."""
from unittest.mock import MagicMock

from pytest import fixture

from app.middleware import auth, log
from app.routes.v2 import metrics
from tests.mocks import cache_v2, crud, request
from tests.testdata import create_team, create_valuestream


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(auth, "request", request)
    monkeypatch.setattr(log, "request", request)
    yield request
    request.reset()


@fixture
def mock_cache(monkeypatch):
    """Patch cache."""
    monkeypatch.setattr(metrics, "organizations_cache_v2", cache_v2)


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


def test_get_organization_metrics(client, mock_cache, mock_admin):
    """Test GET /api/v1/metrics/organization/:id endpoint."""
    resp = client.get("/api/v2/metrics/organization/1")

    assert resp.json["result"][0]["organization_name"] == "org_name_test"
    assert resp.status_code == 200


def test_get_organization_metrics_404(monkeypatch, client, mock_cache, mock_non_admin):
    """Test GET /api/v1/metrics/organization/:id endpoint."""
    expected = "Resource not found"
    monkeypatch.setattr(auth, "organizations_crud", crud)

    resp = client.get("/api/v2/metrics/organization/-1")

    assert resp.text == expected


def test_get_organization_metrics_202(client, mock_cache, mock_admin):
    """Test GET /api/v1/metrics:id endpoint."""
    expected = "Processing not completed"

    resp = client.get("/api/v2/metrics/organization/42")

    assert resp.text == expected
    assert resp.status_code == 202


def test_get_valuestream_metrics(monkeypatch, client, mock_cache, mock_admin):
    """Test GET /api/v1/metrics/valuestream/:id endpoint."""
    monkeypatch.setattr(
        metrics.valuestreams_crud,
        "get_entity",
        MagicMock(return_value=create_valuestream(name="vs_name_test")),
    )
    resp = client.get("/api/v2/metrics/valuestream/1")

    assert resp.json["result"][0]["value_stream_name"] == "vs_name_test"
    assert resp.status_code == 200


def test_get_valuestream_metrics_404(monkeypatch, client, mock_cache, mock_non_admin):
    """Test GET /api/v1/metrics/valuestream/:id endpoint."""
    expected = "Resource not found"
    monkeypatch.setattr(auth, "valuestreams_crud", crud)
    resp = client.get("/api/v2/metrics/valuestream/-1")

    assert resp.text == expected


def test_get_valuestream_metrics_202(monkeypatch, client, mock_cache, mock_admin):
    """Test GET /api/v1/metrics/valuestream/:id endpoint."""
    expected = "Processing not completed"
    monkeypatch.setattr(
        metrics.valuestreams_crud,
        "get_entity",
        MagicMock(return_value=create_valuestream(organization_id=42)),
    )
    resp = client.get("/api/v2/metrics/valuestream/1")
    assert resp.text == expected
    assert resp.status_code == 202


def test_get_team_metrics(monkeypatch, client, mock_cache, mock_admin):
    """Test GET /api/v1/metrics/team/:id endpoint."""
    monkeypatch.setattr(
        metrics.teams_crud,
        "get_entity",
        MagicMock(return_value=create_team(name="team_name_test")),
    )
    monkeypatch.setattr(
        metrics.valuestreams_crud,
        "get_entity",
        MagicMock(return_value=create_valuestream(name="vs_name_test")),
    )
    resp = client.get("/api/v2/metrics/team/1")

    assert resp.json["name"] == "team_name_test"
    assert resp.status_code == 200


def test_get_team_metrics_404(monkeypatch, client, mock_cache, mock_non_admin):
    """Test GET /api/v1/metrics/team/:id endpoint."""
    expected = "Resource not found"
    monkeypatch.setattr(auth, "teams_crud", crud)
    resp = client.get("/api/v2/metrics/team/-1")

    assert resp.text == expected


def test_get_team_metrics_202(monkeypatch, client, mock_cache, mock_admin):
    """Test GET /api/v1/metrics/team/:id endpoint."""
    expected = "Processing not completed"
    monkeypatch.setattr(
        metrics.teams_crud,
        "get_entity",
        MagicMock(return_value=create_team()),
    )
    monkeypatch.setattr(
        metrics.valuestreams_crud,
        "get_entity",
        MagicMock(return_value=create_valuestream(organization_id=42)),
    )
    resp = client.get("/api/v2/metrics/team/1")
    assert resp.text == expected
    assert resp.status_code == 202
