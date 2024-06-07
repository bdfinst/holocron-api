"""FeatureFlags route tests."""

from app.config import FEATURE_FLAGS, SSO_ENABLED


def test_list_feature_flags(client, mock_request):
    """Test GET /api/v2/featureflags."""
    expected = {}
    expected.update(FEATURE_FLAGS)
    expected.update({"SSO_ENABLED": SSO_ENABLED})

    resp = client.get("/api/v2/featureflags")

    assert resp.json == expected
    assert resp.status_code == 200
