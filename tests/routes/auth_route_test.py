"""Authentication middlewares with routes integration tests."""
from unittest.mock import MagicMock

from pytest import fixture

from app.middleware import auth
from app.models import Team, User
from app.routes import pay_rates, teams, users
from tests.mocks import crud, request


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(users, "users_crud", crud)
    monkeypatch.setattr(pay_rates, "pay_rates_crud", crud)
    monkeypatch.setattr(teams, "teams_crud", crud)


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(auth, "request", request)
    yield request
    request.reset()


def test_requires_admin_example_route(client, mock_crud, mock_request, monkeypatch):
    """Test DELETE /api/v1/users/:id endpoint as example for requires_admin."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    test_cases = [
        ("""should allow admins to delete user""", True, 204),
        ("""should not allow non admins to delete user""", False, 403),
    ]
    for c in test_cases:
        description, is_admin, expected = c
        setattr(mock_request, "user", {"isAdmin": is_admin, "id": 1, "username": "t"})
        resp = client.delete("/api/v1/users/1")
        assert resp.status_code == expected, description


def test_requires_leadership_example_route(
    client, mock_crud, mock_request, monkeypatch
):
    """Test GET /api/v1/payrates endpoint as example for requires_leadership."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    test_cases = [
        ("""should allow leadership to see payrates""", True, 200),
        ("""should not allow non leadership to see payrates""", False, 403),
    ]
    for c in test_cases:
        description, is_leadership, expected = c
        setattr(
            mock_request,
            "user",
            {"isOrgLeadership": is_leadership, "id": 1, "username": "t"},
        )
        resp = client.get("/api/v1/payrates")
        assert resp.status_code == expected, description


def test_requires_admin_or_member_member_example_route(
    client, mock_crud, mock_request, monkeypatch
):
    """Test PUT /api/v1/team endpoint as example for requires_admin_or_member."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    test_cases = [
        ("""should allow team members to update team""", False, [User(id=1)], 200),
        ("""should allow admins to update team""", True, [], 200),
        (
            """should not allow non team members and non team admins to update""",
            False,
            [],
            403,
        ),
    ]
    for c in test_cases:
        description, is_admin, team_admins, expected = c
        setattr(mock_request, "user", {"id": 1, "isAdmin": is_admin, "username": "t"})
        monkeypatch.setattr(
            auth.teams_crud,
            "get_entity",
            MagicMock(return_value=Team(users=team_admins, team_size=1)),
        )
        monkeypatch.setattr(
            teams.teams_crud,
            "get_entity",
            MagicMock(return_value=Team(users=team_admins, team_size=1)),
        )
        monkeypatch.setattr(
            teams.teams_crud,
            "update_entity",
            MagicMock(return_value=Team(name="test2", users=team_admins, team_size=1)),
        )

        json = {"name": "test2", "valuestreamId": 1, "teamSize": 1}
        resp = client.put("/api/v1/teams/1", json=json)
        assert resp.status_code == expected, description
