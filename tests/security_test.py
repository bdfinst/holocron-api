"""Security Middlewares test."""
from unittest.mock import MagicMock

from pytest import fixture

from app import security
from app.security import on_unexpected_http_methods
from tests.mocks import request
from tests.utils import first_argument


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(security, "request", request)
    yield request
    request.reset()


def test_on_unexpected_http_methods(mock_request, monkeypatch):
    """Test log on unexpected http method."""
    log_critical_mock = MagicMock()
    monkeypatch.setattr(security.logging, "critical", log_critical_mock)

    resp, code = on_unexpected_http_methods("dontcare")

    assert first_argument(log_critical_mock) == "0.0.0.0 - /test - METHOD NOT ALLOWED"
    assert resp == "Method Not Allowed"
    assert code == 405
