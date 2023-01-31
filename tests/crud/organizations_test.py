"""Organization CRUD tests."""
from unittest.mock import MagicMock

from pytest import raises
from sqlalchemy.exc import IntegrityError

from app.crud import organizations_crud
from app.exceptions import HolocronIntegrityError
from tests.utils import first_argument

json = {"name": "test", "user_ids": []}


def test_create_entity(mock_session):
    """Test create_entity method."""
    result = organizations_crud.create_entity(mock_session, json)
    organization = first_argument(mock_session.add)

    assert organization.name == "test"
    assert result == organization


def test_create_entity_unique_error(mock_session):
    """Test create_entity method with uniqueness violation."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "name - already in use"

    with raises(HolocronIntegrityError) as e:
        organizations_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_create_entity_unknown_error(mock_session):
    """Test create_entity with an unknown error."""

    def commit_error():
        raise IntegrityError("unknown", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        organizations_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_update_entity(mock_session):
    """Test update_entity method."""
    expected = "SELECT * FROM organizations WHERE organizations.id = :id_1"

    result = organizations_crud.update_entity(mock_session, json, 1)
    organization = first_argument(mock_session.add)

    assert organization.name == "test"
    assert first_argument(mock_session.scalars).statement == expected
    assert result == organization


def test_update_entity_unique_error(mock_session):
    """Test update_entity method with uniqueness violation."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "name - already in use"

    with raises(HolocronIntegrityError) as e:
        organizations_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)


def test_update_entity_unknown_error(mock_session):
    """Test update_entity with an unknown error."""

    def commit_error():
        raise IntegrityError("unknown", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        organizations_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)
