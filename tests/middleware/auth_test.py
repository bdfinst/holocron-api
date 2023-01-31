"""Authentication middleware tests."""
from typing import List
from unittest.mock import MagicMock

from flask import Response
from pytest import fixture

from app import security
from app.crud import organizations_crud, teams_crud, valuestreams_crud
from app.middleware import (
    auth,
    requires_admin,
    requires_org_access,
    requires_org_leadership,
    requires_security,
    requires_team_access,
    requires_vs_access,
    return_user,
    set_user,
)
from app.models import Organization, Team, User, Valuestream
from tests.mocks import crud, request
from tests.utils.utils import first_argument, second_argument


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(auth, "request", request)
    monkeypatch.setattr(security, "request", request)
    yield request
    request.reset()


def test_set_user(mock_request, monkeypatch):
    """Test set_user function."""
    monkeypatch.setattr(auth, "users_crud", crud)

    set_user()

    assert mock_request.user == {"username": "1"}


def test_strip_returns():
    """Test strip_returns function."""
    cases = {
        "Test%0A": "Test",
        "Test%0D": "Test",
        "%0A%0DTest": "Test",
        "%0A": "",
        "%%0A0ATest": "Test",
        "Test": "Test",
    }

    for string, result in cases.items():
        assert auth.strip_returns(string) == result


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
    """Test requires admin function."""
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})
    monkeypatch.setattr(auth, "SSO_ENABLED", True)

    result = requires_security([requires_admin])(wrapped_test_func)()

    assert result == "success"


def test_requires_admin_403(mock_request, monkeypatch):
    """Test requires admin function with 403 error."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    result = requires_security([requires_admin])(wrapped_test_func)()

    assert result == ("Invalid permissions", 403)


def test_requires_org_leadership(mock_request, monkeypatch):
    """Test requires org leadership function with org leadership user."""
    setattr(
        mock_request,
        "user",
        {"isOrgLeadership": True, "isAdmin": False, "id": 1, "username": "t"},
    )

    result = requires_security([requires_org_leadership])(wrapped_test_func)()

    assert result == "success"


def test_requires_org_leadership_403(mock_request, monkeypatch):
    """Test requires org leadership function with 403 error."""
    setattr(
        mock_request,
        "user",
        {"isOrgLeadership": False, "isAdmin": False, "id": 1, "username": "t"},
    )

    result = requires_security([requires_org_leadership])(wrapped_test_func)()

    assert result == ("Invalid permissions", 403)


def test_requires_vs_access_vs_admin(mock_request, monkeypatch):
    """Test requires vs access function with vs admin user."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    valuestream = get_test_valuestream()
    valuestream.users = [get_test_user()]
    valuestream_mock = MagicMock(
        return_value=valuestream,
    )
    monkeypatch.setattr(
        valuestreams_crud,
        "get_entity",
        valuestream_mock,
    )

    result = requires_security([requires_vs_access])(wrapped_test_func)(
        valuestream_id=1
    )

    assert second_argument(valuestream_mock) == 1
    assert result == "success"


def test_requires_vs_access_org_admin(mock_request, monkeypatch):
    """Test requires vs access function with org admin user."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    organization = get_test_organization()
    organization.users = [get_test_user()]
    organization_mock = MagicMock(
        return_value=organization,
    )
    valuestream_mock = MagicMock(
        return_value=get_test_valuestream(),
    )
    monkeypatch.setattr(
        organizations_crud,
        "get_entity",
        organization_mock,
    )
    monkeypatch.setattr(
        valuestreams_crud,
        "get_entity",
        valuestream_mock,
    )

    result = requires_security([requires_vs_access])(wrapped_test_func)(
        valuestream_id=1
    )

    assert second_argument(organization_mock) == 1
    assert second_argument(valuestream_mock) == 1
    assert result == "success"


def test_requires_vs_access_403(mock_request, monkeypatch):
    """Test requires vs access function with 403 error."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})

    organization_mock = MagicMock(
        return_value=get_test_organization(),
    )
    valuestream_mock = MagicMock(
        return_value=get_test_valuestream(),
    )
    monkeypatch.setattr(
        organizations_crud,
        "get_entity",
        organization_mock,
    )
    monkeypatch.setattr(
        valuestreams_crud,
        "get_entity",
        valuestream_mock,
    )

    result = requires_security([requires_vs_access])(wrapped_test_func)(
        valuestream_id=1
    )

    assert second_argument(organization_mock) == 1
    assert second_argument(valuestream_mock) == 1
    assert result == ("Invalid permissions", 403)


def test_requires_vs_access_no_id(mock_request, monkeypatch):
    """Test requires vs access function with no valuestream id."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    mock_request.json = {"valuestreamId": "1"}

    valuestream = get_test_valuestream()
    valuestream.users = [get_test_user()]
    valuestream_mock = MagicMock(
        return_value=valuestream,
    )
    monkeypatch.setattr(
        valuestreams_crud,
        "get_entity",
        valuestream_mock,
    )

    result = requires_security([requires_vs_access])(wrapped_test_func)()

    assert second_argument(valuestream_mock) == 1
    assert result == "success"


def test_requires_org_access_org_admin(mock_request, monkeypatch):
    """Test requires org access function with org admin user."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    organization = get_test_organization()
    organization.users = [get_test_user()]
    organization_mock = MagicMock(
        return_value=organization,
    )
    monkeypatch.setattr(
        organizations_crud,
        "get_entity",
        organization_mock,
    )

    result = requires_security([requires_org_access])(wrapped_test_func)(org_id=1)

    assert second_argument(organization_mock) == 1
    assert result == "success"


def test_requires_org_access_no_id(mock_request, monkeypatch):
    """Test requires org access function with no org id input."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    mock_request.json = {"organizationId": "1"}
    organization = get_test_organization()
    organization.users = [get_test_user()]
    organization_mock = MagicMock(return_value=organization)
    monkeypatch.setattr(organizations_crud, "get_entity", organization_mock)

    result = requires_security([requires_org_access])(wrapped_test_func)()

    assert second_argument(organization_mock) == 1
    assert result == "success"


def test_requires_org_access_403(mock_request, monkeypatch):
    """Test requires org access function with 403 error."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    mock_request.json = {"organizationId": "1"}
    organization_mock = MagicMock(return_value=get_test_organization())
    monkeypatch.setattr(organizations_crud, "get_entity", organization_mock)

    result = requires_security([requires_org_access])(wrapped_test_func)(org_id=1)

    assert second_argument(organization_mock) == 1
    assert result == ("Invalid permissions", 403)


def test_requires_team_access_org_admin(mock_request, monkeypatch):
    """Test requires team access function with org admin user."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    organization = get_test_organization()
    organization.users = [get_test_user()]
    organizations_mock = MagicMock(return_value=organization)
    valuestreams_mock = MagicMock(return_value=get_test_valuestream())
    teams_mock = MagicMock(return_value=get_test_team())
    monkeypatch.setattr(
        organizations_crud,
        "get_entity",
        organizations_mock,
    )
    monkeypatch.setattr(valuestreams_crud, "get_entity", valuestreams_mock)
    monkeypatch.setattr(
        teams_crud,
        "get_entity",
        teams_mock,
    )

    result = requires_security([requires_team_access])(wrapped_test_func)(team_id=1)

    assert second_argument(organizations_mock) == 1
    assert second_argument(valuestreams_mock) == 1
    assert second_argument(teams_mock) == 1
    assert result == "success"


def test_requires_team_access_valuestream_admin(mock_request, monkeypatch):
    """Test requires team access function with valuestream admin user."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    valuestream = get_test_valuestream()
    valuestream.users = [get_test_user()]
    valuestream_mock = MagicMock(return_value=valuestream)
    team_mock = MagicMock(return_value=get_test_team())
    monkeypatch.setattr(
        valuestreams_crud,
        "get_entity",
        valuestream_mock,
    )
    monkeypatch.setattr(
        teams_crud,
        "get_entity",
        team_mock,
    )

    result = requires_security([requires_team_access])(wrapped_test_func)(team_id=1)

    assert second_argument(valuestream_mock) == 1
    assert second_argument(team_mock) == 1
    assert result == "success"


def test_requires_team_access_team_admin(mock_request, monkeypatch):
    """Test requires team access function with team admin user."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    team = get_test_team()
    team.users = [get_test_user()]
    team_mock = MagicMock(return_value=team)
    monkeypatch.setattr(
        teams_crud,
        "get_entity",
        team_mock,
    )
    result = requires_security([requires_team_access])(wrapped_test_func)(team_id=1)

    assert second_argument(team_mock) == 1
    assert result == "success"


def test_requires_team_access_403(mock_request, monkeypatch):
    """Test requires team access function with 403 error."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})

    organizations_mock = MagicMock(return_value=get_test_organization())
    valuestreams_mock = MagicMock(return_value=get_test_valuestream())
    teams_mock = MagicMock(return_value=get_test_team())

    monkeypatch.setattr(
        organizations_crud,
        "get_entity",
        organizations_mock,
    )
    monkeypatch.setattr(valuestreams_crud, "get_entity", valuestreams_mock)
    monkeypatch.setattr(
        teams_crud,
        "get_entity",
        teams_mock,
    )

    result = requires_security([requires_team_access])(wrapped_test_func)(team_id=1)
    assert second_argument(organizations_mock) == 1
    assert second_argument(valuestreams_mock) == 1
    assert second_argument(teams_mock) == 1
    assert result == ("Invalid permissions", 403)


def get_test_user() -> User:
    """Create test user."""
    return User(id=1)


def get_test_team() -> Team:
    """Create test team."""
    return Team(id=1, name="team", valuestream_id=1, users=[])


def get_test_valuestream() -> Valuestream:
    """Create test valuesteam."""
    return Valuestream(id=1, name="value", organization_id=1, users=[])


def get_test_organization() -> Organization:
    """Create test organization."""
    return Organization(id=1, name="org", users=[])
