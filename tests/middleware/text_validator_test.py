"""Test text validation middleware."""
from pytest import fixture

from app.middleware import text_validator, validate_text
from tests.mocks import request


@fixture
def mock_request(monkeypatch):
    """Mock flask request object."""
    monkeypatch.setattr(text_validator, "request", request)
    yield request
    request.reset()


def test_validate_text_invalid(mock_request):
    """Test validate_text function."""
    mock_request.json = '{"key": "value©"}'

    result = validate_text()

    assert result[0] == "Invalid characters detected in request body"
    assert result[1] == 400


def test_validate_text_valid(mock_request):
    """Test validate_text function."""
    result = validate_text()

    assert result is None
