"""Rate Limiter tests."""

from pytest import fixture

from app import security
from app.middleware import log, rate_limiter
from app.routes.v2 import organizations
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
    monkeypatch.setattr(rate_limiter, "request", request)
    monkeypatch.setattr(security, "request", request)


def test_rate_limiter(client, mock_crud, mock_request):
    """Test rate limiter using /api/v2/organizations as example."""
    max_requests_in_hour = int(DEFAULT_LIMITS[1].split("/")[0])

    for _ in range(max_requests_in_hour):
        resp = client.get("/api/v2/organizations")

        assert resp.status_code == 200, "should fetch fine until limit exceeds"

    exceed_resp = client.get("/api/v2/organizations")

    assert exceed_resp.status_code == 429, "should fail fetch on limit exceed"
    assert "Too Many Requests" in exceed_resp.text, "should fail fetch on limit exceed"


def test_ip_whitelist(client, mock_crud, mock_request, monkeypatch):
    """Test ip_whitelist decorator."""
    monkeypatch.setattr(rate_limiter, "RATE_LIMITING_IP_WHITELIST", ["0.0.0.0"])
    excess_requests = int(DEFAULT_LIMITS[1].split("/")[0]) + 1

    for _ in range(excess_requests):
        resp = client.get("/api/v2/organizations")

        assert resp.status_code == 200, "should allow all requests"
