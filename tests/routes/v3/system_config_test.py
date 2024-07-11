"""FeatureFlags route tests."""

from app.config import FEATURE_FLAGS, SSO_ENABLED
from app.routes.v3 import system_config


def test_get_system_config(client, mock_request, monkeypatch):
    """Test GET /api/v3/system-config."""
    monkeypatch.setattr(system_config, "VERSION", "test")
    expected = {
        "version": "test",
        "featureFlags": FEATURE_FLAGS,
        "ssoEnabled": SSO_ENABLED,
    }

    resp = client.get("/api/v3/system-config")

    assert resp.json == expected
    assert resp.status_code == 200
