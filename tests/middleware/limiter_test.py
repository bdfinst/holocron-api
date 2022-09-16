"""Rate Limiter tests."""
from pytest import fixture

from app.routes import organizations
from app.security import DEFAULT_LIMITS
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(organizations, "organizations_crud", crud)


def test_rate_limiter(client, mock_crud):
    """Test rate limiter using /api/v1/organizations as example."""
    max_requests_in_hour = int(DEFAULT_LIMITS[1].split("/")[0])
    for _ in range(max_requests_in_hour):
        resp = client.get("/api/v1/organizations")

        assert resp.status_code == 200, "should fetch fine until limit exceeds"

    exceed_resp = client.get("/api/v1/organizations")
    assert exceed_resp.status_code == 429, "should fail fetch on limit exceed"
    assert "Too Many Requests" in exceed_resp.text, "should fail fetch on limit exceed"
