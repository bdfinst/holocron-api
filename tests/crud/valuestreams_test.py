"""Valuestream CRUD tests."""
from unittest.mock import MagicMock

from pytest import raises
from sqlalchemy.exc import IntegrityError

from app.crud import valuestreams_crud
from app.exceptions import HolocronIntegrityError
from tests.utils import first_argument

json = {"name": "test", "organization_id": 1}


def test_create_entity(mock_session):
    """Test create_entity method."""
    result = valuestreams_crud.create_entity(mock_session, json)
    valuestream = first_argument(mock_session.add)

    assert valuestream.name == "test"
    assert valuestream.organization_id == 1
    assert result == valuestream


def test_create_entity_organization_id_error(mock_session):
    """Test create_entity method with invalid organization id."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.ForeignKeyViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "organization_id - not found"

    with raises(HolocronIntegrityError) as e:
        valuestreams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_create_entity_unique_error(mock_session):
    """Test create_entity method with uniqueness violation."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "name - already in use"

    with raises(HolocronIntegrityError) as e:
        valuestreams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_create_entity_unknown_error(mock_session):
    """Test create_entity with an unknown error."""

    def commit_error():
        raise IntegrityError("unknown", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        valuestreams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_update_entity(mock_session):
    """Test update_entity method."""
    expected = "SELECT * FROM valuestreams WHERE valuestreams.id = :id_1"

    result = valuestreams_crud.update_entity(mock_session, json, 1)
    valuestream = first_argument(mock_session.add)

    assert valuestream.name == "test"
    assert valuestream.organization_id == 1
    assert first_argument(mock_session.scalars).statement == expected
    assert result == valuestream


def test_update_entity_organization_id_error(mock_session):
    """Test update_entity method with invalid organization id."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.ForeignKeyViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "organization_id - not found"

    with raises(HolocronIntegrityError) as e:
        valuestreams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)


def test_update_entity_unique_error(mock_session):
    """Test update_entity method with uniqueness violation."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "name - already in use"

    with raises(HolocronIntegrityError) as e:
        valuestreams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)


def test_update_entity_unknown_error(mock_session):
    """Test update_entity with an unknown error."""

    def commit_error():
        raise IntegrityError("unknown", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        valuestreams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)
