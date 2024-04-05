"""Test text validation middleware."""

from app.middleware import validate_text


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
