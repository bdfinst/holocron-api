"""Test scheduled team history methods."""

from datetime import datetime
from unittest.mock import MagicMock

from app.crud.team_history import team_history_crud
from app.crud.teams import teams_crud
from app.models import Team, TeamHistory
from app.processors import team_history
from app.processors.team_history import (
    delete_outdated_team_history,
    process_team_size_histories,
)
from tests.mocks import MockDateTime

mock_dt = MockDateTime(datetime(year=2000, month=1, day=4))


def test_delete_outdated_team_history_old_team(monkeypatch, mock_session):
    """Testing the deletion of outdated team histories."""
    list_of_teams = [
        Team(
            name="Test1",
            team_size=3,
            id=1,
        )
    ]
    list_of_team_history = [
        TeamHistory(
            id=1,
            team_id=1,
            created_at=datetime(year=2000, month=1, day=3),
            team_size=3,
        ),
        TeamHistory(
            id=2,
            team_id=1,
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
        Team(
            name="Test1",
            team_size=3,
            id=1,
        )
    ]
    list_of_team_history = [
        TeamHistory(
            id=1,
            team_id=1,
            created_at=datetime(year=2000, month=1, day=3),
            team_size=3,
        ),
        TeamHistory(
            id=2,
            team_id=1,
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
                TeamHistory(
                    team_size=3,
                    team_id=1,
                    created_at=datetime(year=2000, month=1, day=5),
                ),
                TeamHistory(
                    team_size=4,
                    team_id=1,
                    created_at=datetime(year=2000, month=1, day=6),
                ),
                TeamHistory(
                    team_size=5,
                    team_id=1,
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
        _, input_case, expected = case
        actual = process_team_size_histories(input_case)
        assert expected == actual
