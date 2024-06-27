"""Test process_cumulative_flow."""

from datetime import datetime

from app.models import StatusHistory, Ticket, TicketStatus
from app.processors.v2 import cumulative_flow
from app.processors.v2.cumulative_flow import (
    get_hist_stat_at_date,
    get_last_activity_date,
    get_uniq_weeks_latest_stat_hists,
    process_cumulative_flow,
)
from tests.mocks import MockDateTime

mock_dt = MockDateTime(datetime(year=2000, month=1, day=27))


def test_get_last_activity_date(monkeypatch):
    """Test get_last_activity_date function."""
    monkeypatch.setattr(cumulative_flow, "datetime", mock_dt)

    test_cases = [
        (
            """Return today if ticket is not completed.""",
            Ticket(
                collector_target_id=1,
                resource_id="200",
                assignee="someone",
                status=TicketStatus.IN_PROGRESS,
                ticket_type="Feature",
                priority="Highest",
                super_ticket_id=None,
                status_history=[
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=24),
                        status=TicketStatus.TO_DO,
                        assignee=None,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=25),
                        status=TicketStatus.IN_PROGRESS,
                        assignee=None,
                    ),
                ],
            ),
            datetime(year=2000, month=1, day=27),
        ),
        (
            """Return last activity date if ticket is completed.""",
            Ticket(
                collector_target_id=1,
                resource_id="200",
                assignee="someone",
                status=TicketStatus.TO_DO,
                ticket_type="Feature",
                priority="Highest",
                super_ticket_id=None,
                status_history=[
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=24),
                        status=TicketStatus.TO_DO,
                        assignee=None,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=25),
                        status=TicketStatus.IN_PROGRESS,
                        assignee=None,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=27),
                        status=TicketStatus.DONE,
                        assignee=None,
                    ),
                ],
            ),
            datetime(year=2000, month=1, day=25),
        ),
        (
            """Return last activity date if ticket is completed
            more than one time.""",
            Ticket(
                collector_target_id=1,
                resource_id="200",
                assignee="someone",
                status=TicketStatus.TO_DO,
                ticket_type="Feature",
                priority="Highest",
                super_ticket_id=None,
                status_history=[
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=24),
                        status=TicketStatus.TO_DO,
                        assignee=None,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=25),
                        status=TicketStatus.IN_PROGRESS,
                        assignee=None,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=26),
                        status=TicketStatus.DONE,
                        assignee=None,
                    ),
                    StatusHistory(
                        ticket_id=1,
                        date=datetime(year=2000, month=1, day=26, hour=12),
                        status=TicketStatus.DONE,
                        assignee=None,
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
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.IN_PROGRESS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=24),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # age of 3 business days in wip status
                    ],
                )
            ],
            (
                {},
                {"2000-01-24": [3]},
            ),
        ),
        (
            """Given that an issue is in backlog
            for the week despite fluctuating status,
            it should show as to do for the week,
            and show the age of the issue for the value of
            the last week.""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.TO_DO,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=24),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),  # age of 3 business days for first week
                        # should be computed here (not counting weekends)
                    ],
                )
            ],
            (
                {"2000-01-24": [3]},
                {},
            ),
        ),
        (
            """Given that an issue is fluctuating
            status between weeks, it should still show
            the last status for the week and the age
            for it during the last week.""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.IN_PROGRESS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=7),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),  # for week 2000-01-03 we should see this in backlog
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=11),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # for week 2000-01-10 we should see this in wip
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=18),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),  # for week 2000-01-17 it should be in backlog
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # age of 5 + 5 + 5 + 3 = 18 should be here
                        # for wip for this week (2000-01-24)
                    ],
                )
            ],
            (
                {
                    "2000-01-03": [-1],
                    "2000-01-17": [-1],
                },
                {
                    "2000-01-10": [-1],
                    "2000-01-24": [18],
                },
            ),
        ),
        (
            """Given it is a done issue, it should just
            show age for weeks when it was in progress
            or in backlog during it's final week in progress.""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=7),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),  # should be in backlog for week 2000-01-03
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=11),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # should be in wip for week 2000-01-10
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=18),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),  # age of 1 + 5 + 5 = 11 should be here for
                        # backlog for this week week 2000-01-17 backlog
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),  # nothing here, since it is a done status
                    ],
                )
            ],
            (
                {
                    "2000-01-03": [-1],
                    "2000-01-17": [11],
                },
                {
                    "2000-01-10": [-1],
                },
            ),
        ),  # front-end should handle when the
        # data does not show the latest week data.
        # for the average age of issues in backlog etc.
        (
            """Should ignore no effort
            tickets.""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=TicketStatus.DONE,
                            assignee=None,
                        )  # nothing here, since it is a done status
                    ],
                )
            ],
            (
                {},
                {},
            ),
        ),
        (
            """Should work as expected for
            with multiple tickets""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=18),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # week 2000-01-17 should show in wip with
                        # age 1
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),  # should show nothing on week 4.
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.IN_PROGRESS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),  # backlog in 2000-01-03 and 2000-01-10
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # wip in 2000-01-17
                        # and 18 days of age for week
                        # 2000-01-24
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="201",
                    assignee="someone",
                    status=TicketStatus.TO_DO,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),  # backlog: { 2000-01-24 : 2 } 2 days of age for week 2000-01-24
                    ],
                ),
                Ticket(  # testing an edge case for tickets
                    # that go from done to to_do or in progress again
                    collector_target_id=1,
                    resource_id="201",
                    assignee="someone",
                    status=TicketStatus.TO_DO,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),  # backlog: { 2000-01-03: -1 }
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # wip : { 2000-01-10: -1 }, { 2000-01-17: -1 }
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),  # ignore this
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),  # this should be the age now { 2000-01-24 : 18 }
                    ],
                ),
            ],
            (
                {
                    "2000-01-03": [-1, -1],
                    "2000-01-10": [-1],
                    "2000-01-24": [2, 18],
                },
                {
                    "2000-01-10": [-1],
                    "2000-01-17": [1, -1, -1],
                    "2000-01-24": [18],
                },
            ),
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
            progress date in week 2000-01-03, it should
            return TicketStatus.TO_DO.""",
            (
                datetime(year=2000, month=1, day=8),
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=1),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),
                    ],
                ),
            ),
            TicketStatus.TO_DO,
        ),
        (
            """Given date is before first in
            progress date in week 2000-01-10, it should
            return TicketStatus.TO_DO.""",
            (
                datetime(year=2000, month=1, day=15),
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=1),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),
                    ],
                ),
            ),
            TicketStatus.TO_DO,
        ),
        (
            """Given it is in between
            the interval of in progress and done.
            it should return in progress.""",
            (
                datetime(year=2000, month=1, day=22),
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=1),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),
                    ],
                ),
            ),
            TicketStatus.IN_PROGRESS,
        ),
        (
            """Given it is greater than the interval
            given. it should return last status.""",
            (
                datetime(year=2000, month=1, day=22),
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.IN_PROGRESS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=1),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                    ],
                ),
            ),
            TicketStatus.IN_PROGRESS,
        ),
        (
            """Given the date exists on the interval
            given. it should return that date's status.""",
            (
                datetime(year=2000, month=1, day=19),
                Ticket(
                    collector_target_id=1,
                    resource_id="200",
                    assignee="someone",
                    status=TicketStatus.IN_PROGRESS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=1),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=25),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=27),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                    ],
                ),
            ),
            TicketStatus.IN_PROGRESS,
        ),
    ]

    for case in cases:
        description, input_case, expected = case
        date, ticket = input_case
        actual = get_hist_stat_at_date(date, get_uniq_weeks_latest_stat_hists(ticket))
        assert expected == actual, description
