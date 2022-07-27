"""Authentication middleware tests."""
from unittest.mock import MagicMock

from flask import Response
from pytest import fixture

from app.middleware import (
    auth,
    requires_admin,
    requires_admin_or_member,
    requires_leadership,
    return_user,
    set_user,
)
from app.models import Team
from tests.mocks import crud, request


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(auth, "request", request)
    yield request
    request.reset()


def test_set_user(mock_request, monkeypatch):
    """Test set_user function."""
    monkeypatch.setattr(auth, "users_crud", crud)

    set_user()

    assert mock_request.user == {"username": "1"}


def test_return_user(mock_request):
    """Test return_user function."""
    setattr(mock_request, "user", {"username": "1"})
    response = Response()

    result = return_user(response)

    assert result.headers["X-User"] == '{"username": "1"}'


def wrapped_test_func(*args, **kwargs):
    """Mock function for wrapping decorators."""
    return "success"


def test_requires_admin(mock_request, monkeypatch):
    """Test requires_admin decorator."""
    setattr(mock_request, "user", {"isAdmin": True})
    monkeypatch.setattr(auth, "SSO_ENABLED", True)

    result = requires_admin(wrapped_test_func)()

    assert result == "success"


def test_requires_admin_403(mock_request, monkeypatch):
    """Test requires_admin decorator."""
    setattr(mock_request, "user", {"isAdmin": False})
    monkeypatch.setattr(auth, "SSO_ENABLED", True)

    result = requires_admin(wrapped_test_func)()

    assert result == ("Invalid permissions", 403)


def test_requires_leadership(mock_request, monkeypatch):
    """Test requires_leadership decorator."""
    setattr(mock_request, "user", {"isOrgLeadership": True})
    monkeypatch.setattr(auth, "SSO_ENABLED", True)

    result = requires_leadership(wrapped_test_func)()

    assert result == "success"


def test_requires_leadership_403(mock_request, monkeypatch):
    """Test requires_leadership decorator."""
    setattr(mock_request, "user", {"isOrgLeadership": False})
    monkeypatch.setattr(auth, "SSO_ENABLED", True)

    result = requires_leadership(wrapped_test_func)()

    assert result == ("Invalid permissions", 403)


def test_requires_admin_or_member_admin(mock_request, monkeypatch):
    """Test requires_admin_or_member decorator."""
    setattr(mock_request, "user", {"isAdmin": True})
    monkeypatch.setattr(auth, "SSO_ENABLED", True)

    result = requires_admin_or_member(wrapped_test_func)()

    assert result == "success"


def test_requires_admin_or_member_member(mock_request, monkeypatch):
    """Test requires_admin_or_member decorator."""
    setattr(mock_request, "user", {"id": 1, "isAdmin": False})
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    monkeypatch.setattr(
        auth.teams_crud, "get_entity", MagicMock(return_value=Team(users=[1]))
    )

    result = requires_admin_or_member(wrapped_test_func)(team_id=1)

    assert result == "success"


def test_requires_admin_or_member_403(mock_request, monkeypatch):
    """Test requires_admin_or_member decorator."""
    setattr(mock_request, "user", {"id": 1, "isAdmin": False})
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    monkeypatch.setattr(
        auth.teams_crud, "get_entity", MagicMock(return_value=Team(users=[]))
    )

    result = requires_admin_or_member(wrapped_test_func)(team_id=1)

    assert result == ("Invalid permissions", 403)
