"""Team CRUD tests."""
from unittest.mock import MagicMock

from pytest import fixture, raises
from sqlalchemy.exc import IntegrityError

from app.crud import collector_targets_crud
from app.crud import teams as teams_crud_mod
from app.crud import teams_crud
from app.crud.teams import is_workflow_only
from app.exceptions import HolocronIntegrityError
from app.models import Team, TicketBoard
from tests.mocks import mock_select
from tests.testdata import create_repository, create_team, create_ticket_board
from tests.utils import first_argument

json = {
    "name": "test",
    "team_size": 1,
    "user_ids": [],
    "collector_target_ids": [21],
    "valuestream_id": 1,
}


@fixture
def mock_sqlalchemy(monkeypatch):
    """Patch sqlalchemy."""
    monkeypatch.setattr(teams_crud_mod, "select", mock_select)


@fixture
def mock_team_collector_targets(monkeypatch):
    """Mock to satisfy one feature board per team."""
    monkeypatch.setattr(
        collector_targets_crud,
        "get_entity",
        MagicMock(
            return_value=create_ticket_board(
                id=21,
            )
        ),
    )


@fixture
def mock_is_workflow_only(monkeypatch):
    """Mock to satisfy is workflow only."""
    monkeypatch.setattr(teams_crud_mod, "is_workflow_only", lambda *_, **__: False)


def test_is_workflow_only(mock_session):
    """Test is_workflow_only method."""
    test_cases = [
        (
            """Should return true if team only has ticketboards.""",
            MagicMock(first=lambda *_, **__: create_ticket_board()),
            True,
        ),
        (
            """Should return false otherwise.""",
            MagicMock(first=lambda *_, **__: None),
            False,
        ),
    ]
    for test_case in test_cases:
        description, mock_scalars_first, expected = test_case
        mock_session.scalars = MagicMock(return_value=mock_scalars_first)
        assert expected == is_workflow_only(mock_session, create_team()), description


def test_get_entity_no_team_view(mock_session, mock_sqlalchemy):
    """Test get_entity_no_team_view method."""
    expected = (
        "SELECT * FROM teams "
        + "WHERE teams.view_owner_id IS NULL "
        + "WHERE teams.id = :id_1"
    )
    result = teams_crud.get_entity_no_team_view(mock_session, 1)
    assert result.statement == expected


def test_get_entity_no_team_view_error(mock_session, mock_sqlalchemy):
    """Test get_entity_no_team_view method error."""
    mock_scalars_return = MagicMock(first=lambda *_, **__: None)
    mock_session.scalars = MagicMock(return_value=mock_scalars_return)

    with raises(HolocronIntegrityError) as e:
        teams_crud.get_entity_no_team_view(mock_session, 1)
    assert "Invalid id" in str(e.value)


def test_get_entities_without_team_views(mock_session, mock_sqlalchemy):
    """Test get_entities_without_team_views method."""
    expected = "SELECT * FROM teams " + "WHERE teams.view_owner_id IS NULL"
    result = teams_crud.get_entities_without_team_views(mock_session)
    assert result[0].statement == expected


def test_create_entity(
    mock_session,
    mock_team_collector_targets,
    mock_is_workflow_only,
):
    """Test create_entity method."""
    result = teams_crud.create_entity(mock_session, json)
    team = first_argument(mock_session.add)
    mock_team_feature_board_id = 21

    assert team.name == "test"
    assert team.team_size == 1
    assert team.users == []
    assert len(team.collector_targets) == 1
    assert team.collector_targets[0].id == mock_team_feature_board_id
    assert team.valuestream_id == 1
    assert result == team


def test_create_entity_valuestream_id_error(
    mock_session,
    mock_team_collector_targets,
    mock_is_workflow_only,
):
    """Test create_entity method with invalid valuestream id."""

    def raise_integrity_error(*args, **kwargs):
        raise IntegrityError("psycopg2.errors.ForeignKeyViolation", None, None)

    mock_session.add = MagicMock(side_effect=raise_integrity_error)
    expected = "valuestream_id - not found"

    with raises(HolocronIntegrityError) as e:
        teams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_create_entity_unique_error(
    mock_session, mock_team_collector_targets, mock_is_workflow_only
):
    """Test create_entity method with uniqueness violation."""

    def raise_integrity_error(*args, **kwargs):
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.add = MagicMock(side_effect=raise_integrity_error)
    expected = "name - already in use"

    with raises(HolocronIntegrityError) as e:
        teams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_create_entity_unknown_error(
    mock_session, mock_team_collector_targets, mock_is_workflow_only
):
    """Test create_entity with an unknown error."""

    def raise_integrity_error(*args, **kwargs):
        raise IntegrityError("unknown", None, None)

    mock_session.add = MagicMock(side_effect=raise_integrity_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        teams_crud.create_entity(mock_session, json)

    assert expected == str(e.value)


def test_update_entity(
    mock_session, mock_team_collector_targets, mock_is_workflow_only
):
    """Test update_entity method."""
    expected = "SELECT * FROM teams WHERE teams.id = :id_1"

    result = teams_crud.update_entity(mock_session, json, 1)
    team = first_argument(mock_session.add)
    expected_feature_board_id = 21

    assert team.name == "test"
    assert team.team_size == 1
    assert team.users == []
    assert len(team.collector_targets) == 1
    assert team.collector_targets[0].id == expected_feature_board_id
    assert team.valuestream_id == 1
    assert first_argument(mock_session.scalars).statement == expected
    assert result == team


def test_update_entity_filter_team_views(
    mock_session, mock_team_collector_targets, mock_is_workflow_only
):
    """Test update_entity method."""
    expected = "SELECT * FROM teams WHERE teams.id = :id_1"

    result = teams_crud.update_entity(mock_session, json, 1)
    team = first_argument(mock_session.add)
    expected_feature_board_id = 21

    assert team.name == "test"
    assert team.team_size == 1
    assert team.users == []
    assert len(team.collector_targets) == 1
    assert team.collector_targets[0].id == expected_feature_board_id
    assert team.valuestream_id == 1
    assert first_argument(mock_session.scalars).statement == expected
    assert result == team


def test_update_entity_valuestream_id_error(
    mock_session, mock_team_collector_targets, mock_is_workflow_only
):
    """Test update_entity method with invalid valuestream id."""

    def raise_integrity_error(*args, **kwargs):
        raise IntegrityError("psycopg2.errors.ForeignKeyViolation", None, None)

    mock_session.add = MagicMock(side_effect=raise_integrity_error)
    expected = "valuestream_id - not found"

    with raises(HolocronIntegrityError) as e:
        teams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)


def test_update_entity_unique_error(
    mock_session, mock_team_collector_targets, mock_is_workflow_only
):
    """Test update_entity method with uniqueness violation."""

    def raise_integrity_error(*args, **kwargs):
        raise IntegrityError("psycopg2.errors.UniqueViolation", None, None)

    mock_session.add = MagicMock(side_effect=raise_integrity_error)
    expected = "name - already in use"

    with raises(HolocronIntegrityError) as e:
        teams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)


def test_update_entity_unknown_error(
    mock_session, mock_team_collector_targets, mock_is_workflow_only
):
    """Test update_entity with an unknown error."""

    def raise_integrity_error(*args, **kwargs):
        raise IntegrityError("unknown", None, None)

    mock_session.add = MagicMock(side_effect=raise_integrity_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        teams_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)
