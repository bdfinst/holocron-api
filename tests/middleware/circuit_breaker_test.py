"""Circuit breaker middleware tests."""

from datetime import datetime
from unittest.mock import MagicMock

from flask import Response
from pytest import fixture

from app.middleware import (
    circuit_breaker,
    circuit_breaker_check,
    circuit_breaker_validation,
)
from tests.mocks import request
from tests.utils import first_argument


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(circuit_breaker, "request", request)
    yield request
    request.reset()


def test_circuit_breaker_check_good(mock_request):
    """Test circuit_breaker_check function with passing request."""
    mock_request.headers["X-Forwarded-For"] = "no match"

    result = circuit_breaker_check()

    assert result is None


def test_circuit_breaker_check_bad(mock_request, monkeypatch):
    """Test circuit_breaker_check function with failing request."""
    mock_request.headers["X-Forwarded-For"] = "match"
    monkeypatch.setattr(
        circuit_breaker.breaker, "break_times", {"match": datetime.now()}
    )

    result = circuit_breaker_check()

    assert result == ("Too many requests", 429)


def test_circuit_breaker_validation_200(monkeypatch):
    """Test circuit_breaker_validation_function with 200 status code."""
    mock_time = MagicMock()
    monkeypatch.setattr(circuit_breaker, "time", mock_time)
    resp = Response()
    resp.status_code = 200

    circuit_breaker_validation(resp)

    assert not mock_time.sleep.called


def test_circuit_breaker_validation_500(mock_request, monkeypatch):
    """Test circuit_breaker_validation_function with 500 status code."""
    mock_time = MagicMock()
    monkeypatch.setattr(circuit_breaker, "time", mock_time)
    resp = Response()
    resp.status_code = 500

    circuit_breaker_validation(resp)

    assert first_argument(mock_time.sleep) == 60
