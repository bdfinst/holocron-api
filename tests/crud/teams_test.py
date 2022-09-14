"""Team CRUD tests."""
from unittest.mock import MagicMock

from pytest import raises
from sqlalchemy.exc import IntegrityError

from app.crud import collector_targets_crud, teams_crud
from app.exceptions import HolocronIntegrityError
from app.models import Repository
from tests.utils import first_argument

json = {
    "name": "test",
    "team_size": 1,
    "user_ids": [],
    "collector_target_ids": [],
    "valuestream_id": 1,
}


def test_create_entity(mock_session):
    """Test create_entity method."""
    result = teams_crud.create_entity(mock_session, json)
    team = first_argument(mock_session.add)

    assert team.name == "test"
    assert team.team_size == 1
    assert team.users == []
    assert team.collector_targets == []
    assert team.valuestream_id == 1
    assert result == team


def test_create_entity_valuestream_id_error(mock_session):
    """Test create_entity method with invalid valuestream id."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.ForeignKeyViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "valuestream_id - not found"

    with raises(HolocronIntegrityError) as e:
        teams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_create_entity_unique_error(mock_session):
    """Test create_entity method with uniqueness violation."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "name - already in use"

    with raises(HolocronIntegrityError) as e:
        teams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_create_entity_collector_targets_error(mock_session, monkeypatch):
    """Test create_entity with collector targets error."""
    expected = "collectorTargetIds - already in use"
    mock_team_json = {
        "name": "test",
        "team_size": 1,
        "user_ids": [],
        "collector_target_ids": [1],
        "valuestream_id": 1,
    }
    monkeypatch.setattr(
        collector_targets_crud,
        "get_entity",
        MagicMock(
            return_value=Repository(
                collector_id=1,
                url="https://test-repo.com",
                id=1,
                team_id=42,
            )
        ),
    )

    with raises(HolocronIntegrityError) as e:
        teams_crud.create_entity(mock_session, mock_team_json)

    assert expected == str(e.value)


def test_create_entity_unknown_error(mock_session):
    """Test create_entity with an unknown error."""

    def commit_error():
        raise IntegrityError("unknown", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        teams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_update_entity(mock_session):
    """Test update_entity method."""
    expected = "SELECT * FROM teams WHERE teams.id = :id_1"

    result = teams_crud.update_entity(mock_session, json, 1)
    team = first_argument(mock_session.add)

    assert team.name == "test"
    assert team.team_size == 1
    assert team.users == []
    assert team.collector_targets == []
    assert team.valuestream_id == 1
    assert first_argument(mock_session.scalars).statement == expected
    assert result == team


def test_update_entity_valuestream_id_error(mock_session):
    """Test update_entity method with invalid valuestream id."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.ForeignKeyViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "valuestream_id - not found"

    with raises(HolocronIntegrityError) as e:
        teams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)


def test_update_entity_unique_error(mock_session):
    """Test update_entity method with uniqueness violation."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "name - already in use"

    with raises(HolocronIntegrityError) as e:
        teams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)


def test_update_entity_collector_targets_error(mock_session, monkeypatch):
    """Test update_entity with collector targets error."""
    expected = "collectorTargetIds - already in use"
    mock_team_json = {
        "name": "test",
        "team_size": 1,
        "user_ids": [],
        "collector_target_ids": [1],
        "valuestream_id": 1,
    }
    monkeypatch.setattr(
        collector_targets_crud,
        "get_entity",
        MagicMock(
            return_value=Repository(
                collector_id=1,
                url="https://test-repo.com",
                id=1,
                team_id=42,
            )
        ),
    )

    with raises(HolocronIntegrityError) as e:
        teams_crud.update_entity(mock_session, mock_team_json, 1)

    assert expected == str(e.value)


def test_update_entity_unknown_error(mock_session):
    """Test update_entity with an unknown error."""

    def commit_error():
        raise IntegrityError("unknown", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        teams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)
