"""Authentication middleware tests."""
from app.middleware import set_user


def test_set_user(mock_request, mock_crud):
    """Test set_user function."""
    set_user()

    assert mock_request.user == {"username": "1"}
