"""Metrics route tests."""
from pytest import fixture

from app.routes import metrics
from tests.mocks import cache


@fixture
def mock_cache(monkeypatch):
    """Patch cache."""
    monkeypatch.setattr(metrics, "organizations_cache", cache)


def test_get_metrics(client, mock_cache):
    """Test GET /api/v1/metrics/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/metrics/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_metrics_404(client, mock_cache):
    """Test GET /api/v1/metrics/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/metrics/-1")

    assert resp.text == expected
