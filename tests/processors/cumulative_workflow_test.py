"""Test process_cumulative_flow."""
from datetime import datetime

from app.models import StatusHistory, Ticket
from app.processors import cumulative_flow
from app.processors.cumulative_flow import (
    get_hist_stat_at_date,
    get_last_activity_date,
    get_uniq_weeks_latest_stat_hists,
    process_cumulative_flow,
)
from tests.mocks import MockDateTime

TO_DO_STATUS = "To Do"
IN_PROGRESS_STATUS = "In Progress"
DONE_STATUS = "Done"

mock_dt = MockDateTime(datetime(year=2000, month=1, day=27))


def test_get_last_activity_date(monkeypatch):
    """Test get_last_activity_date function."""
    monkeypatch.setattr(cumulative_flow, "datetime", mock_dt)

    test_cases = [
        (
            """Return today if ticket is not completed.""",
            Ticket(
                board_id=1,
                ticket_id=200,
                assignee="someone",
                status=IN_PROGRESS_STATUS,
                ticket_type="Feature",
                priority="Highest",
                super_ticket_id=None,
                status_history=[
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=24),
                        status=TO_DO_STATUS,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=25),
                        status=IN_PROGRESS_STATUS,
                    ),
                ],
            ),
            datetime(year=2000, month=1, day=27),
        ),
        (
            """Return last activity date if ticket is completed.""",
            Ticket(
                board_id=1,
                ticket_id=200,
                assignee="someone",
                status=TO_DO_STATUS,
                ticket_type="Feature",
                priority="Highest",
                super_ticket_id=None,
                status_history=[
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=24),
                        status=TO_DO_STATUS,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=25),
                        status=IN_PROGRESS_STATUS,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=27),
                        status=DONE_STATUS,
                    ),
                ],
            ),
            datetime(year=2000, month=1, day=25),
        ),
        (
            """Return last activity date if ticket is completed
            more than one time.""",
            Ticket(
                board_id=1,
                ticket_id=200,
                assignee="someone",
                status=TO_DO_STATUS,
                ticket_type="Feature",
                priority="Highest",
                super_ticket_id=None,
                status_history=[
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=24),
                        status=TO_DO_STATUS,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=25),
                        status=IN_PROGRESS_STATUS,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=26),
                        status=DONE_STATUS,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=26, hour=12),
                        status=DONE_STATUS,
                    ),
                ],
            ),
            datetime(year=2000, month=1, day=25),
        ),
    ]
    for test_case in test_cases:
        description, input_case, expected = test_case
        assert get_last_activity_date(input_case) == expected, description


def test_cumulative_flow(monkeypatch):
    """Test cumulative flow calculation."""
    monkeypatch.setattr(cumulative_flow, "datetime", mock_dt)

    cases = [
        (
            """Given that an issue is in progress
            towards the end of the week despite fluctuating status,
            it should show as in progress for the week,
            and show the age of the issue for the value of
            the last week.""",
            [
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=IN_PROGRESS_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=24),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=IN_PROGRESS_STATUS,
                        ),  # age of 3 business days in wip status
                    ],
                )
            ],
            {
                "wip": {"2000_04": [3]},
                "backlog": {},
            },
        ),
        (
            """Given that an issue is in backlog
            for the week despite fluctuating status,
            it should show as to do for the week,
            and show the age of the issue for the value of
            the last week.""",
            [
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=TO_DO_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=24),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=TO_DO_STATUS,
                        ),  # age of 3 business days for first week
                        # should be computed here (not counting weekends)
                    ],
                )
            ],
            {
                "wip": {},
                "backlog": {"2000_04": [3]},
            },
        ),
        (
            """Given that an issue is fluctuating
            status between weeks, it should still show
            the last status for the week and the age
            for it during the last week.""",
            [
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=IN_PROGRESS_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=7),
                            status=TO_DO_STATUS,
                        ),  # for week 2000_01 we should see this in backlog
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=11),
                            status=IN_PROGRESS_STATUS,
                        ),  # for week 2000_02 we should see this in wip
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=18),
                            status=TO_DO_STATUS,
                        ),  # for week 2000_03 it should be in backlog
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=IN_PROGRESS_STATUS,
                        )  # age of 5 + 5 + 5 + 3 = 18 should be here
                        # for wip for this week (2000_04)
                    ],
                )
            ],
            {
                "wip": {
                    "2000_02": [-1],
                    "2000_04": [18],
                },
                "backlog": {
                    "2000_01": [-1],
                    "2000_03": [-1],
                },
            },
        ),
        (
            """Given it is a done issue, it should just
            show age for weeks when it was in progress
            or in backlog during it's final week in progress.""",
            [
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=7),
                            status=TO_DO_STATUS,
                        ),  # should be in backlog for week 2000_01
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=11),
                            status=IN_PROGRESS_STATUS,
                        ),  # should be in wip for week 2000_02
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=18),
                            status=TO_DO_STATUS,
                        ),  # age of 1 + 5 + 5 = 11 should be here for
                        # backlog for this week week 2000_03 backlog
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=DONE_STATUS,
                        ),  # nothing here, since it is a done status
                    ],
                )
            ],
            {
                "wip": {
                    "2000_02": [-1],
                },
                "backlog": {
                    "2000_01": [-1],
                    "2000_03": [11],
                },
            },
        ),  # front-end should handle when the
        # data does not show the latest week data.
        # for the average age of issues in backlog etc.
        (
            """Should ignore no effort
            tickets.""",
            [
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=DONE_STATUS,
                        )  # nothing here, since it is a done status
                    ],
                )
            ],
            {
                "wip": {},
                "backlog": {},
            },
        ),
        (
            """Should work as expected for
            with multiple tickets""",
            [
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
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
                        ),  # week 2000_03 should show in wip with
                        # age 1
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=DONE_STATUS,
                        ),  # should show nothing on week 4.
                    ],
                ),
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=IN_PROGRESS_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TO_DO_STATUS,
                        ),  # backlog in 2000_01 and 2000_02
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=IN_PROGRESS_STATUS,
                        ),  # wip in 2000_03
                        # and 18 days of age for week
                        # 2000_04
                    ],
                ),
                Ticket(
                    board_id=1,
                    ticket_id=201,
                    assignee="someone",
                    status=TO_DO_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=TO_DO_STATUS,
                        ),  # backlog: { 2000_04 : 2 } 2 days of age for week 2000_04
                    ],
                ),
                Ticket(  # testing an edge case for tickets
                    # that go from done to to_do or in progress again
                    board_id=1,
                    ticket_id=201,
                    assignee="someone",
                    status=TO_DO_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TO_DO_STATUS,
                        ),  # backlog: { 2000_01: -1 }
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=IN_PROGRESS_STATUS,
                        ),  # wip : { 2000_02: -1 }, { 2000_03: -1 }
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=DONE_STATUS,
                        ),  # ignore this
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=TO_DO_STATUS,
                        ),  # this should be the age now { 2000_04 : 18 }
                    ],
                ),
            ],
            {
                "wip": {"2000_02": [-1], "2000_03": [1, -1, -1], "2000_04": [18]},
                "backlog": {
                    "2000_01": [-1, -1],
                    "2000_02": [-1],
                    "2000_04": [2, 18],
                },
            },
        ),
    ]
    for case in cases:
        description, input_case, expected = case
        assert process_cumulative_flow(input_case) == expected, description


def test_get_hist_stat_at_date():
    """Test get_hist_stat_at_date function."""
    cases = [
        (
            """Given date is before first in
            progress date in week 2000_01, it should
            return TO_DO_STATUS.""",
            (
                datetime(year=2000, month=1, day=8),
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
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
            """Given date is before first in
            progress date in week 2000_02, it should
            return TO_DO_STATUS.""",
            (
                datetime(year=2000, month=1, day=15),
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
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
            """Given it is in between
            the interval of in progress and done.
            it should return in progress.""",
            (
                datetime(year=2000, month=1, day=22),
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
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
        (
            """Given it is greater than the interval
            given. it should return last status.""",
            (
                datetime(year=2000, month=1, day=22),
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=IN_PROGRESS_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
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
                    ],
                ),
            ),
            IN_PROGRESS_STATUS,
        ),
        (
            """Given the date exists on the interval
            given. it should return that date's status.""",
            (
                datetime(year=2000, month=1, day=19),
                Ticket(
                    board_id=1,
                    ticket_id=200,
                    assignee="someone",
                    status=IN_PROGRESS_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
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
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=IN_PROGRESS_STATUS,
                        ),
                    ],
                ),
            ),
            IN_PROGRESS_STATUS,
        ),
    ]

    for case in cases:
        description, input_case, expected = case
        date, ticket = input_case
        actual = get_hist_stat_at_date(date, get_uniq_weeks_latest_stat_hists(ticket))
        assert expected == actual, description
