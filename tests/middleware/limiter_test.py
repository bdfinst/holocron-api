"""Rate Limiter tests."""
from pytest import fixture

from app import security
from app.middleware import log
from app.routes.v1 import organizations
from app.security import DEFAULT_LIMITS
from tests.mocks import crud, request


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(organizations, "organizations_crud", crud)


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(log, "request", request)
    monkeypatch.setattr(security, "request", request)


def test_rate_limiter(client, mock_crud, mock_request):
    """Test rate limiter using /api/v1/organizations as example."""
    max_requests_in_hour = int(DEFAULT_LIMITS[1].split("/")[0])
    for _ in range(max_requests_in_hour):
        resp = client.get("/api/v1/organizations")

        assert resp.status_code == 200, "should fetch fine until limit exceeds"

    exceed_resp = client.get("/api/v1/organizations")
    assert exceed_resp.status_code == 429, "should fail fetch on limit exceed"
    assert "Too Many Requests" in exceed_resp.text, "should fail fetch on limit exceed"
