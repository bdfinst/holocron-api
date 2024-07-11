"""FeatureFlags route tests."""

from setuptools_scm import get_version

from app.config import FEATURE_FLAGS, SSO_ENABLED


def test_get_system_config(client, mock_request):
    """Test GET /api/v3/system-config."""
    expected = {
        "version": get_version(),
        "featureFlags": FEATURE_FLAGS,
        "ssoEnabled": SSO_ENABLED,
    }

    resp = client.get("/api/v3/system-config")

    assert resp.json == expected
    assert resp.status_code == 200
