"""Testing process_effort."""

from datetime import datetime

from app.models import StatusHistory, Ticket, TicketStatus, TicketType
from app.processors.v2 import effort
from app.processors.v2.effort import process_effort
from tests.mocks import MockDateTime

mock_dt = MockDateTime(datetime(year=2000, month=1, day=23))


def test_process_effort(monkeypatch):
    """Testing process_effort hours case."""
    monkeypatch.setattr(effort, "datetime", mock_dt)

    test_cases = [
        (
            """"Should collect one for each category of bucket type""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="1",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.FEATURE,
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
                            date=datetime(year=2000, month=1, day=4),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="2",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.DEFECT,
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=2,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=2,
                            date=datetime(year=2000, month=1, day=4),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=2,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="3",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.MAINTENANCE,
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=3,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=3,
                            date=datetime(year=2000, month=1, day=4),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=3,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="4",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.UNPLANNED,
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=4,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=4,
                            date=datetime(year=2000, month=1, day=4),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=4,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),
                    ],
                ),
            ],
            (
                {"2000-01-03": [1]},
                {"2000-01-03": [1]},
                {"2000-01-03": [1]},
                {"2000-01-03": [1]},
                {"2000-01-03": [1]},
                {"2000-01-03": [1]},
                {"2000-01-03": [1]},
                {"2000-01-03": [1]},
            ),
        ),
        (
            """Given there is one issue in progress for more than
        one week, it should spread the effort into different
        week buckets.""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="1",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.FEATURE,
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=2),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # week 1 has 5 days worth of effort and ends on Jan 7
                        # week 2 has 5 days worth of effort and starts and ends from
                        # Jan 10 - Jan 14 business days, so expect to see 5 days
                        # of effort on week 1, and 5 days on week 2.
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=18),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),  # Week 3 is from Jan 17 to Jan 21 business days,
                        # so expect to see 1 day of effort for this
                        # status.
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="2",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.FEATURE,
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=2),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # week 1 has 5 days worth of effort and ends on Jan 7
                        # week 2 has 5 days worth of effort and starts and ends from
                        # Jan 10 - Jan 14
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),
                    ],
                ),
            ],
            (
                {
                    "2000-01-03": [5, 5],
                    "2000-01-10": [5, 5],
                    "2000-01-17": [1, 2],
                },
                {
                    "2000-01-03": [5, 5],
                    "2000-01-10": [5, 5],
                    "2000-01-17": [1, 2],
                },
                {},
                {},
                {},
                {},
                {},
                {},
            ),
        ),
        (
            """It should calculate effort till current date
            if the issue is still in progress.""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="1",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.FEATURE,
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
                            date=datetime(
                                year=2000, month=1, day=19, hour=12, minute=0, second=0
                            ),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # should be 12 hour progress + 24 hour progress (20th Jan)
                        # + 24 hour (21st Jan) = 2.5 days
                    ],
                ),
            ],
            (
                {"2000-01-17": [2.5]},
                {"2000-01-17": [2.5]},
                {},
                {},
                {},
                {},
                {},
                {},
            ),
        ),
        (
            """Should calculate partial effort""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="1",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.FEATURE,
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3, hour=8, minute=30),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3, hour=9, minute=30),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000, month=1, day=3, hour=12, minute=30
                            ),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),  # 3 hours worth of effort translates to 3/24 = 0.1 days
                        # worth of effort.
                    ],
                ),
            ],
            (
                {"2000-01-03": [0.1]},
                {"2000-01-03": [0.1]},
                {},
                {},
                {},
                {},
                {},
                {},
            ),
        ),
        (
            """Should calculate effort for status
            that changes progress back to back.""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="1",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.FEATURE,
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000, month=1, day=3, hour=12, minute=0, second=0
                            ),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000, month=1, day=4, hour=8, minute=0, second=0
                            ),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # 3.7 days of effort (24 - 8 = 16 hours of effort
                        # after issue in progress for the day) for week 1
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000, month=1, day=10, hour=12, minute=0, second=0
                            ),
                            status=TicketStatus.TO_DO,
                            assignee=None,
                        ),  # .5 days of effort here for week 2
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000, month=1, day=12, hour=12, minute=0, second=0
                            ),
                            status=TicketStatus.IN_PROGRESS,
                            assignee=None,
                        ),  # 2.5 days of effort here for week 2
                        # so total of 3 for week 2
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000,
                                month=1,
                                day=21,
                                hour=23,
                                minute=59,
                                second=59,
                            ),
                            status=TicketStatus.DONE,
                            assignee=None,
                        ),  # 5 days of effort for week 3
                    ],
                ),
            ],
            (
                {"2000-01-03": [3.7], "2000-01-10": [3], "2000-01-17": [5]},
                {"2000-01-03": [3.7], "2000-01-10": [3], "2000-01-17": [5]},
                {},
                {},
                {},
                {},
                {},
                {},
            ),
        ),
    ]

    for case in test_cases:
        description, input_case, expected = case
        actual = process_effort(input_case)
        assert expected == actual, description
