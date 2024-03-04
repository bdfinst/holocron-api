"""Repositories CRUD tests."""

from unittest.mock import MagicMock

from pytest import fixture, raises

from app.crud import repositories, repositories_crud
from app.exceptions import HolocronIntegrityError
from tests.mocks import mock_func, mock_select


@fixture
def mock_sqlalchemy(monkeypatch):
    """Patch sqlalchemy."""
    monkeypatch.setattr(repositories, "select", mock_select)
    monkeypatch.setattr(repositories, "func", mock_func)


def test_get_count(mock_sqlalchemy, mock_session):
    """Test get_count method."""
    expected = (
        "SELECT COUNT(*) FROM collector_targets "
        + "WHERE collector_targets.type = :type_1"
    )
    result = repositories_crud.get_count(mock_session)

    assert result.statement == expected


def test_get_count_for_team(mock_sqlalchemy, mock_session):
    """Test get_count_for_team method."""
    expected = (
        "SELECT COUNT(*) FROM collector_targets "
        + "WHERE collector_targets.team_id = :team_id_1 "
        + "WHERE collector_targets.type = :type_1"
    )
    result = repositories_crud.get_count_for_team(mock_session, 1)

    assert result.statement == expected


def test_get_entity(mock_sqlalchemy, mock_session):
    """Test get_entity method."""
    expected = (
        "SELECT * FROM collector_targets "
        + "WHERE collector_targets.type = :type_1 "
        + "WHERE collector_targets.id = :id_1"
    )
    result = repositories_crud.get_entity(mock_session, 1)

    assert result.statement == expected


def test_get_entity_invalid_repository(mock_session):
    """Test get_entity method 404."""
    mock_session.scalars = MagicMock(
        return_value=MagicMock(first=lambda *_, **__: None)
    )

    with raises(HolocronIntegrityError) as e:
        repositories_crud.get_entity(mock_session, 1)
    assert "Invalid id" in str(e.value)


def test_get_entities(mock_sqlalchemy, mock_session):
    """Test get_entities method."""
    expected = (
        "SELECT * FROM collector_targets " + "WHERE collector_targets.type = :type_1"
    )

    result = repositories_crud.get_entities(mock_session)

    assert result[0].statement == expected


def test_get_entities_paginated(mock_sqlalchemy, mock_session):
    """Test get_entities_paginated method."""
    expected = (
        "SELECT * FROM collector_targets "
        + "WHERE collector_targets.type = :type_1 "
        + "OFFSET 0 LIMIT 100"
    )

    result = repositories_crud.get_entities_paginated(mock_session)

    assert result[0].statement == expected


def test_get_entities_for_team(mock_sqlalchemy, mock_session):
    """Test get_entities_for_team method."""
    expected = (
        "SELECT * FROM collector_targets "
        + "WHERE collector_targets.team_id = :team_id_1 "
        + "WHERE collector_targets.type = :type_1"
    )

    result = repositories_crud.get_entities_for_team(mock_session, 1)

    assert result[0].statement == expected


def test_get_entities_for_team_paginated(mock_sqlalchemy, mock_session):
    """Test get_entities_for_team_paginated method."""
    expected = (
        "SELECT * FROM collector_targets "
        + "WHERE collector_targets.team_id = :team_id_1 "
        + "WHERE collector_targets.type = :type_1 "
        + "OFFSET 0 LIMIT 100"
    )

    result = repositories_crud.get_entities_for_team_paginated(mock_session, 1)

    assert result[0].statement == expected
