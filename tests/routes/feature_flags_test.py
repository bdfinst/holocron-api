"""FeatureFlags route tests."""
from app.config import FEATURE_FLAGS
from tests.mocks import request


def test_list_feature_flags(client):
    """Test GET /api/v1/featureflags."""
    expected = FEATURE_FLAGS

    resp = client.get("/api/v1/featureflags")

    assert resp.json == expected
    assert resp.status_code == 200
