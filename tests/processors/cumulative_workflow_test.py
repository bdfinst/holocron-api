"""Test process_cumulative_flow."""
from datetime import datetime

from app.models import StatusHistory, Ticket
from app.processors import cumulative_flow
from app.processors.cumulative_flow import process_cumulative_flow, status_snap_shot
from tests.mocks import MockDateTime

TO_DO_STATUS = "To Do"
IN_PROGRESS_STATUS = "In Progress"
DONE_STATUS = "Done"

mock_dt = MockDateTime(datetime(year=2000, month=1, day=27))


def test_status_snapshot():
    """Test status_snapshot function."""
    cases = [
        (
            (
                datetime(year=2000, month=1, day=8),
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=1),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=DONE_STATUS,
                        ),
                    ],
                ),
            ),
            TO_DO_STATUS,
        ),
        (
            (
                datetime(year=2000, month=1, day=15),
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=1),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=DONE_STATUS,
                        ),
                    ],
                ),
            ),
            TO_DO_STATUS,
        ),
        (
            (
                datetime(year=2000, month=1, day=22),
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=1),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=DONE_STATUS,
                        ),
                    ],
                ),
            ),
            IN_PROGRESS_STATUS,
        ),
    ]

    for case in cases:
        input_case, expected = case
        date, ticket = input_case
        actual = status_snap_shot(date, ticket)
        assert expected == actual


def test_process_cumulative_flow(monkeypatch):
    """Test process_cumulative_flow function."""
    monkeypatch.setattr(cumulative_flow, "datetime", mock_dt)

    cases = [
        (
            """It should calculate the age of tickets
            that are in progress and in backlog""",
            [
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=18),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=DONE_STATUS,
                        ),
                    ],
                ),
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=IN_PROGRESS_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=IN_PROGRESS_STATUS,
                        ),
                    ],
                ),
                Ticket(
                    board_id=1,
                    ticket_id=201,
                    assignee="someone",
                    status=TO_DO_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=TO_DO_STATUS,
                        ),
                    ],
                ),
            ],
            {
                "wip": {"2000_03": [4, 15], "2000_04": [5, 18]},
                "backlog": {
                    "2000_01": [5],
                    "2000_02": [10],
                    "2000_03": [1, 12],
                    "2000_04": [2],
                },
            },
        ),
    ]

    for case in cases:
        _, input_case, expected = case
        actual = process_cumulative_flow(input_case)
        assert expected == actual
