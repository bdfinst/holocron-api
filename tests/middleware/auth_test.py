"""Authentication middleware tests."""

from unittest.mock import MagicMock

from flask import Response
from pytest import fixture

from app import security
from app.crud import organizations_crud, team_views_crud, teams_crud, valuestreams_crud
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
from tests.mocks import config, crud, request
from tests.testdata import (
    create_organization,
    create_team,
    create_team_view,
    create_valuestream,
)
from tests.utils.utils import second_argument


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(auth, "request", request)
    monkeypatch.setattr(security, "request", request)
    yield request
    request.reset()


@fixture
def mock_config(monkeypatch):
    """Mock configuration."""
    monkeypatch.setattr(auth, "config", config)


@fixture
def mock_config_feature_team_views(monkeypatch):
    """Mock configuration feature flag FEATURE_TEAM_VIEWS."""
    monkeypatch.setattr(auth, "FEATURE_FLAGS", {"FEATURE_TEAM_VIEWS": True})


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


def test_return_user_sso_disabled(mock_request, monkeypatch):
    """Test return_user function."""
    monkeypatch.setattr(auth, "SSO_ENABLED", False)
    response = Response()

    result = return_user(response)

    assert (
        result.headers["X-User"]
        == '{"isOrgLeadership": true, "isAdmin": true, "ssoId": "-1", "username": "name"}'
    )


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
    valuestream_mock = MagicMock(
        return_value=create_valuestream(),
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
    organization_mock = MagicMock(
        return_value=create_organization(),
    )
    valuestream_mock = MagicMock(
        return_value=create_valuestream(users=[]),
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
        return_value=create_organization(users=[]),
    )
    valuestream_mock = MagicMock(
        return_value=create_valuestream(users=[]),
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

    valuestream_mock = MagicMock(
        return_value=create_valuestream(),
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
    organization_mock = MagicMock(
        return_value=create_organization(),
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
    organization_mock = MagicMock(return_value=create_organization())
    monkeypatch.setattr(organizations_crud, "get_entity", organization_mock)

    result = requires_security([requires_org_access])(wrapped_test_func)()

    assert second_argument(organization_mock) == 1
    assert result == "success"


def test_requires_org_access_403(mock_request, monkeypatch):
    """Test requires org access function with 403 error."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    mock_request.json = {"organizationId": "1"}
    organization_mock = MagicMock(return_value=create_organization(users=[]))
    monkeypatch.setattr(organizations_crud, "get_entity", organization_mock)

    result = requires_security([requires_org_access])(wrapped_test_func)(org_id=1)

    assert second_argument(organization_mock) == 1
    assert result == ("Invalid permissions", 403)


def test_requires_team_access_org_admin(mock_request, monkeypatch):
    """Test requires team access function with org admin user."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    organizations_mock = MagicMock(return_value=create_organization())
    valuestreams_mock = MagicMock(return_value=create_valuestream(users=[]))
    teams_mock = MagicMock(return_value=create_team(users=[]))
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
    valuestream_mock = MagicMock(return_value=create_valuestream())
    team_mock = MagicMock(return_value=create_team(users=[]))
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
    team_mock = MagicMock(return_value=create_team())
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

    organizations_mock = MagicMock(return_value=create_organization(users=[]))
    valuestreams_mock = MagicMock(return_value=create_valuestream(users=[]))
    teams_mock = MagicMock(return_value=create_team(users=[]))

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


def test_requires_team_access_update_delete_team_feature_team_views(
    mock_request, mock_config_feature_team_views, monkeypatch
):
    """Test requires team access with update/delete team with feature flag on."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    team_mock = MagicMock(return_value=create_team())
    monkeypatch.setattr(
        teams_crud,
        "get_entity",
        team_mock,
    )
    result = requires_security([requires_team_access])(wrapped_test_func)(team_id=1)

    assert second_argument(team_mock) == 1
    assert result == "success"


def test_requires_team_access_update_or_delete_team_view(
    mock_request, mock_config_feature_team_views, monkeypatch
):
    """Test requires team access with update/delete team view."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})

    monkeypatch.setattr(
        team_views_crud, "get_entity", MagicMock(return_value=create_team_view())
    )
    monkeypatch.setattr(teams_crud, "get_entity", MagicMock(return_value=create_team()))
    result = requires_security([requires_team_access])(wrapped_test_func)(
        team_view_id=1
    )
    assert result == "success"


def test_requires_team_access_create_team_view(
    mock_request, mock_config_feature_team_views, monkeypatch
):
    """Test requires team access with create team view."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    mock_request.json = {"viewOwnerId": "1"}

    monkeypatch.setattr(teams_crud, "get_entity", MagicMock(return_value=create_team()))
    result = requires_security([requires_team_access])(wrapped_test_func)()
    assert result == "success"


def test_requires_team_access_update_delete_team_view_403(
    mock_request, mock_config_feature_team_views, monkeypatch
):
    """Test requires team access update/delete team view 403."""
    setattr(mock_request, "user", {"isAdmin": False, "id": 1, "username": "t"})
    mock_request.json = {"viewOwnerId": "1"}

    organizations_mock = MagicMock(return_value=create_organization(users=[]))
    valuestreams_mock = MagicMock(return_value=create_valuestream(users=[]))
    teams_mock = MagicMock(return_value=create_team(users=[]))
    team_view_mock = MagicMock(return_value=create_team_view(users=[]))

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
    monkeypatch.setattr(team_views_crud, "get_entity", team_view_mock)

    result = requires_security([requires_team_access])(wrapped_test_func)(
        team_view_id=1
    )
    assert result == ("Invalid permissions", 403)
