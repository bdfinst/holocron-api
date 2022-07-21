"""Repositories CRUD tests."""
from pytest import fixture

from app.crud import repositories, repositories_crud
from tests.mocks import mock_select


@fixture
def mock_sqlalchemy(monkeypatch):
    """Patch sqlalchemy."""
    monkeypatch.setattr(repositories, "select", mock_select)


def test_get_entities(mock_sqlalchemy, mock_session):
    """Test get_entities method."""
    expected = (
        "SELECT * FROM collector_targets "
        + "WHERE collector_targets.repository_id IS NOT NULL"
    )

    result = repositories_crud.get_entities(mock_session)

    assert result[0].statement == expected


def test_get_entities_for_team(mock_sqlalchemy, mock_session):
    """Test get_entities_for_team method."""
    expected = (
        "SELECT * FROM collector_targets "
        + "WHERE collector_targets.team_id = :team_id_1 "
        + "WHERE collector_targets.repository_id IS NOT NULL"
    )

    result = repositories_crud.get_entities_for_team(mock_session, 1)

    assert result[0].statement == expected
