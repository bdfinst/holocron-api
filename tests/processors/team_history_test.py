"""Test scheduled team history methods."""

from datetime import datetime
from unittest.mock import MagicMock

from app.models import TeamHistory
from app.processors import team_history
from app.processors.team_history import (
    delete_outdated_team_history,
    process_team_history,
)
from tests.mocks import MockDateTime
from tests.testdata import create_team

mock_dt = MockDateTime(datetime(year=2000, month=1, day=4))


def create_team_history(team_id=1, team_size=1, created_at=datetime(2000, 1, 1)):
    """Create mock team_history object with default values."""
    team_history = TeamHistory(team_id=team_id, team_size=team_size)
    team_history.created_at = created_at
    return team_history


def test_delete_outdated_team_history_old_team(monkeypatch, mock_session):
    """Testing the deletion of outdated team histories."""
    list_of_teams = [
        create_team(
            team_size=3,
        )
    ]
    list_of_team_history = [
        create_team_history(
            created_at=datetime(year=2000, month=1, day=3),
            team_size=3,
        ),
        create_team_history(
            created_at=datetime(year=1998, month=1, day=3),
            team_size=3,
        ),
    ]

    delete_cb = MagicMock()
    monkeypatch.setattr(
        team_history.teams_crud, "get_entities", MagicMock(return_value=list_of_teams)
    )
    monkeypatch.setattr(
        team_history.team_history_crud,
        "get_entities_for_team",
        MagicMock(return_value=list_of_team_history),
    )
    monkeypatch.setattr(team_history.team_history_crud, "delete_entity", delete_cb)
    monkeypatch.setattr(team_history, "datetime", mock_dt)

    delete_outdated_team_history()
    delete_cb.assert_called_once()


def test_delete_outdated_team_history_no_old_team(monkeypatch, mock_session):
    """Testing the deletion of outdated team histories with no old team."""
    list_of_teams = [
        create_team(
            team_size=3,
        )
    ]
    list_of_team_history = [
        create_team_history(
            created_at=datetime(year=2000, month=1, day=3),
            team_size=3,
        ),
        create_team_history(
            created_at=datetime(year=2000, month=1, day=1),
            team_size=3,
        ),
    ]
    delete_cb = MagicMock()
    monkeypatch.setattr(
        team_history.teams_crud, "get_entities", MagicMock(return_value=list_of_teams)
    )
    monkeypatch.setattr(
        team_history.team_history_crud,
        "get_entities_for_team",
        MagicMock(return_value=list_of_team_history),
    )
    monkeypatch.setattr(team_history.team_history_crud, "delete_entity", delete_cb)
    monkeypatch.setattr(team_history, "datetime", mock_dt)

    delete_outdated_team_history()
    delete_cb.assert_not_called()


def test_process_team_size():
    """Testing processing team history data into weekly data."""
    test_cases = [
        (
            "It should format the data of multiple team histories correctly",
            [
                create_team_history(
                    team_size=3,
                    created_at=datetime(year=2000, month=1, day=5),
                ),
                create_team_history(
                    team_size=4,
                    created_at=datetime(year=2000, month=1, day=6),
                ),
                create_team_history(
                    team_size=5,
                    created_at=datetime(year=2000, month=1, day=10),
                ),
            ],
            {"team_size": {"2000_01": [3, 4], "2000_02": [5]}},
        ),
        (
            "It should result in array length 0 when there are no team histories",
            [],
            {"team_size": {}},
        ),
    ]

    for case in test_cases:
        description, input_case, expected = case
        actual = process_team_history(input_case)
        assert expected == actual, description
