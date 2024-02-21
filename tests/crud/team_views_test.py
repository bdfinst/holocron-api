"""Team views CRUD tests."""

from unittest.mock import MagicMock

from pytest import fixture, raises

from app.crud import collector_targets_crud
from app.crud import team_views as teams_view_crud_mod
from app.crud import team_views_crud, teams_crud
from app.exceptions import HolocronIntegrityError
from tests.mocks import mock_select
from tests.testdata import create_team, create_team_view, create_ticket_board
from tests.utils import first_argument

json = {"name": "test", "collector_target_ids": [21], "view_owner_id": 1}


@fixture
def mock_teams_crud_helper_functions(monkeypatch):
    """Mock get_team_validation_data in app.crud.teams."""
    monkeypatch.setattr(teams_view_crud_mod, "is_workflow_only", lambda *_, **__: False)


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
def mock_teams_crud(monkeypatch):
    """."""
    monkeypatch.setattr(teams_crud, "get_entity", MagicMock(return_value=create_team()))


@fixture
def mock_teams_view_crud(monkeypatch):
    """."""
    monkeypatch.setattr(
        team_views_crud, "get_entity", MagicMock(return_value=create_team_view())
    )


@fixture
def mock_sqlalchemy(monkeypatch):
    """Patch sqlalchemy."""
    monkeypatch.setattr(teams_view_crud_mod, "select", mock_select)


def test_get_entity(mock_session, mock_sqlalchemy):
    """Test get_entity method."""
    expected = (
        "SELECT * FROM teams "
        + "WHERE teams.view_owner_id IS NOT NULL "
        + "WHERE teams.id = :id_1"
    )

    result = team_views_crud.get_entity(mock_session, 1)

    assert result.statement == expected


def test_get_entity_error(mock_session, mock_sqlalchemy):
    """Test get_entity method error."""
    mock_scalars_return = MagicMock(first=lambda *_, **__: None)
    mock_session.scalars = MagicMock(return_value=mock_scalars_return)

    with raises(HolocronIntegrityError) as e:
        team_views_crud.get_entity(mock_session, 1)
    assert "Invalid id" in str(e.value)


def test_get_entities(mock_session, mock_sqlalchemy):
    """Test get_entities method."""
    expected = "SELECT * FROM teams " + "WHERE teams.view_owner_id IS NOT NULL"
    result = team_views_crud.get_entities(mock_session)
    assert result[0].statement == expected


def test_get_entities_paginated(mock_session, mock_sqlalchemy):
    """Test get_entities_paginated method."""
    expected = (
        "SELECT * FROM teams "
        + "WHERE teams.view_owner_id IS NOT NULL "
        + "OFFSET 0 LIMIT 100"
    )
    result = team_views_crud.get_entities_paginated(mock_session)
    assert result[0].statement == expected


def test_create_entity(
    mock_session,
    mock_team_collector_targets,
    mock_teams_crud,
    mock_teams_crud_helper_functions,
):
    """Test create_entities method."""
    result = team_views_crud.create_entity(mock_session, json)
    team_view = first_argument(mock_session.add)

    assert team_view.name == "test"
    assert team_view.view_owner_id == 1
    assert len(team_view.collector_targets) == 1
    assert team_view.collector_targets[0].id == json["collector_target_ids"][0]
    assert result == team_view


def test_update_entity(
    mock_session, mock_teams_view_crud, mock_teams_crud_helper_functions, monkeypatch
):
    """Test update_entity method."""
    monkeypatch.setattr(
        collector_targets_crud,
        "get_entity",
        MagicMock(
            return_value=create_ticket_board(
                id=21,
            )
        ),
    )
    result = team_views_crud.update_entity(mock_session, json, create_team_view().id)
    team_view = first_argument(mock_session.add)

    assert team_view.name == json["name"]
    assert team_view.view_owner_id == json["view_owner_id"]
    assert len(team_view.collector_targets) == 1
    assert team_view.collector_targets[0].id == json["collector_target_ids"][0]
    assert result == team_view
