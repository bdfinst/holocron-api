"""Value stream CRUD tests."""

from unittest.mock import MagicMock

from pytest import fixture, raises
from sqlalchemy.exc import IntegrityError

from app.crud import value_streams_crud
from app.exceptions import HolocronIntegrityError
from tests.testdata import create_team, create_team_view, create_value_stream
from tests.utils import first_argument

json = {"name": "test", "organization_id": 1, "user_ids": []}


@fixture
def mock_value_streams_crud(monkeypatch):
    """Mock value streams crud."""
    monkeypatch.setattr(
        value_streams_crud,
        "get_entity",
        MagicMock(
            return_value=create_value_stream(teams=[create_team(), create_team_view()])
        ),
    )
    monkeypatch.setattr(
        value_streams_crud,
        "get_entities",
        MagicMock(
            return_value=[
                create_value_stream(teams=[create_team(), create_team_view()])
            ]
        ),
    )
    monkeypatch.setattr(
        value_streams_crud,
        "get_entities_paginated",
        MagicMock(
            return_value=[
                create_value_stream(teams=[create_team(), create_team_view()])
            ]
        ),
    )


def test_get_entity_without_team_views(mock_session, mock_value_streams_crud):
    """Test get_entity_without_team_views method."""
    expected = create_value_stream(teams=[create_team()])

    result = value_streams_crud.get_entity_without_team_views(mock_session, 1)

    assert result == expected


def test_get_entities_without_team_views(mock_session, mock_value_streams_crud):
    """Test get_entities_without_team_views method."""
    expected = [create_value_stream(teams=[create_team()])]

    result = value_streams_crud.get_entities_without_team_views(mock_session)

    assert expected == result


def test_get_entities_without_team_views_paginated(
    mock_session, mock_value_streams_crud
):
    """Test get_entities_without_team_views_paginated method."""
    expected = [create_value_stream(teams=[create_team()])]

    result = value_streams_crud.get_entities_without_team_views_paginated(mock_session)

    assert expected == result


def test_create_entity(mock_session):
    """Test create_entity method."""
    result = value_streams_crud.create_entity(mock_session, json)
    value_stream = first_argument(mock_session.add)

    assert value_stream.name == "test"
    assert value_stream.organization_id == 1
    assert result == value_stream


def test_create_entity_organization_id_error(mock_session):
    """Test create_entity method with invalid organization id."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.ForeignKeyViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "organization_id - not found"

    with raises(HolocronIntegrityError) as e:
        value_streams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_create_entity_unique_error(mock_session):
    """Test create_entity method with uniqueness violation."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "name - already in use"

    with raises(HolocronIntegrityError) as e:
        value_streams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_create_entity_unknown_error(mock_session):
    """Test create_entity with an unknown error."""

    def commit_error():
        raise IntegrityError("unknown", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        value_streams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_update_entity(mock_session, mock_value_streams_crud):
    """Test update_entity method."""
    expected_add = create_value_stream(
        name=json["name"],
        organization_id=json["organization_id"],
        users=[],
        teams=[create_team(), create_team_view()],
    )
    expected_return = create_value_stream(
        name=json["name"],
        organization_id=json["organization_id"],
        users=[],
        teams=[create_team()],
    )

    value_stream_result = value_streams_crud.update_entity(mock_session, json, 1)
    value_stream = first_argument(mock_session.add)

    assert value_stream == expected_add
    assert value_stream_result == expected_return


def test_update_entity_organization_id_error(mock_session):
    """Test update_entity method with invalid organization id."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.ForeignKeyViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "organization_id - not found"

    with raises(HolocronIntegrityError) as e:
        value_streams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)


def test_update_entity_unique_error(mock_session):
    """Test update_entity method with uniqueness violation."""

    def commit_error():
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "name - already in use"

    with raises(HolocronIntegrityError) as e:
        value_streams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)


def test_update_entity_unknown_error(mock_session):
    """Test update_entity with an unknown error."""

    def commit_error():
        raise IntegrityError("unknown", None, None)

    mock_session.commit = MagicMock(side_effect=commit_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        value_streams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)
