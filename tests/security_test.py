"""Security Middlewares test."""

from unittest.mock import MagicMock

from pytest import raises

from app import security
from app.security import SQL_INJECTION, get_sanitized_id, on_unexpected_http_methods
from tests.utils.utils import first_argument


def test_on_unexpected_http_methods(mock_request, monkeypatch):
    """Test log on unexpected http method."""
    log_critical_mock = MagicMock()
    monkeypatch.setattr(security.logging, "critical", log_critical_mock)

    resp, code = on_unexpected_http_methods("dontcare")

    assert first_argument(log_critical_mock) == "0.0.0.0 - /test - METHOD NOT ALLOWED"
    assert resp == "Method Not Allowed"
    assert code == 405


def test_get_sanitized_id(mock_request):
    """Test get_sanitized_id valid id."""
    input_value, expected_value = "1", 1
    assert get_sanitized_id(input_value) == expected_value


def test_get_sanitized_id_error(mock_request, monkeypatch):
    """Test get_sanitized_id invalid id."""
    log_critical_mock = MagicMock()
    monkeypatch.setattr(security.logging, "critical", log_critical_mock)

    input_value = "1=1"

    with raises(Exception) as _:
        get_sanitized_id(input_value)
    assert first_argument(log_critical_mock) == f"0.0.0.0 - /test - {SQL_INJECTION}"
