"""FeatureFlags route tests."""
from pytest import fixture

from app.config import FEATURE_FLAGS
from app.middleware import log
from tests.mocks import request


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(log, "request", request)
    yield request
    request.reset()


def test_list_feature_flags(client, mock_request):
    """Test GET /api/v2/featureflags."""
    expected = FEATURE_FLAGS

    resp = client.get("/api/v2/featureflags")

    assert resp.json == expected
    assert resp.status_code == 200
