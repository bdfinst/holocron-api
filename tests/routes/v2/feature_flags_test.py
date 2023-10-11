"""FeatureFlags route tests."""
from app.config import FEATURE_FLAGS


def test_list_feature_flags(client, mock_request):
    """Test GET /api/v2/featureflags."""
    expected = FEATURE_FLAGS

    resp = client.get("/api/v2/featureflags")

    assert resp.json == expected
    assert resp.status_code == 200
