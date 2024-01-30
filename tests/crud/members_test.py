"""Member CRUD tests."""

from unittest.mock import MagicMock

from pytest import fixture, raises
from sqlalchemy.exc import IntegrityError

from app.crud import members as members_crud_mod
from app.crud import members_crud, teams_members_crud
from app.exceptions import HolocronIntegrityError
from tests.mocks import mock_select
from tests.testdata import create_member
from tests.utils import first_argument


@fixture
def mock_sqlalchemy(monkeypatch):
    """Patch sqlalchemy."""
    monkeypatch.setattr(members_crud_mod, "select", mock_select)


def test_create_entity(mock_session):
    """Test members_crud.create_entity."""
    json = {"username": "test-username", "name": "test-name"}
    result = members_crud.create_entity(mock_session, json)
    member = first_argument(mock_session.add)

    assert member.username == "test-username"
    assert member.name == "test-name"
    assert result == member


def test_create_entity_error(mock_session):
    """Test members_crud.create_entity."""

    def raises_integrity_error(*args, **kwargs):
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.add = MagicMock(side_effect=raises_integrity_error)
    expected = "username - already in use"

    with raises(HolocronIntegrityError) as e:
        members_crud.create_entity(
            mock_session, {"username": "test-username", "name": "test-name"}
        )

    assert expected == str(e.value)


def test_find_entity_by_username(mock_session, mock_sqlalchemy):
    """Test members_crud.find_entity_by_username."""
    expected = "SELECT * FROM members WHERE members.username = :username_1"
    result = members_crud.find_entity_by_username(mock_session, "test")
    assert result.statement == expected


def test_create_entities(monkeypatch, mock_session):
    """Test teams_members_crud.create_entities."""
    monkeypatch.setattr(
        members_crud_mod,
        "get_or_create_member",
        MagicMock(return_value=create_member()),
    )

    json = [{"start_date": "2020-01-01T00:00:00.000Z", "member": {}}]
    result = teams_members_crud.create_entities(mock_session, json, 1)
    teams_members = first_argument(mock_session.add)

    assert teams_members.member_id == 1
    assert teams_members.team_id == 1
    assert teams_members.start_date == "2020-01-01T00:00:00.000Z"
    assert result == [teams_members]


def test_create_entities_error(monkeypatch, mock_session):
    """Test teams_members_crud.create_entities."""


def test_get_or_create_member(monkeypatch):
    """Test get_or_create_member function."""

    class MockMembersCRUD:
        """Mock class for members_crud."""

        def find_entity_by_username(self, session, username):
            """Mock method."""
            if username == "exists":
                return "found"

        def create_entity(self, session, json):
            """Mock method."""
            return "created"

    monkeypatch.setattr(members_crud_mod, "members_crud", MockMembersCRUD())

    test_cases = [{"username": "exists"}, {"username": "does not exist"}]
    expected = ["found", "created"]

    results = [members_crud_mod.get_or_create_member(None, case) for case in test_cases]

    assert results == expected
