"""Request logging middleware tests."""

from unittest.mock import MagicMock

from pytest import fixture, mark

from app.middleware import log, log_request
from tests.mocks import request
from tests.utils import first_argument


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(log, "request", request)
    yield request
    request.reset()


@mark.skip(reason="testing header logs")
def test_log_request(mock_request, monkeypatch):
    """Test log_request function."""
    log_mock = MagicMock()
    monkeypatch.setattr(log.logging, "info", log_mock)

    log_request()

    assert first_argument(log_mock) == "0.0.0.0 - /test"
