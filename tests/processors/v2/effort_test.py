"""Testing process_effort."""
from datetime import datetime

from pytest import fixture

from app.models import StatusHistory, Ticket
from app.processors.v1 import utils
from app.processors.v2 import effort
from app.processors.v2.effort import process_effort
from tests.mocks import MockDateTime, config

DONE_STATUS = "Done"
TO_DO_STATUS = "To Do"
IN_PROGRESS_STATUS = "In Progress"
mock_dt = MockDateTime(datetime(year=2000, month=1, day=23))


@fixture
def mock_config(monkeypatch):
    """Mock configuration."""
    monkeypatch.setattr(utils, "config", config)
    yield config
    config.reset()


def test_process_effort(monkeypatch, mock_config):
    """Testing process_effort hours case."""
    monkeypatch.setattr(effort, "datetime", mock_dt)

    mock_config.JIRA_TICKET_TYPE_BUCKETS = {
        "defect_effort": ["Bug", "Anomaly"],
        "unplanned": ["Unplanned"],
        "maintenance": ["Maintenance"],
        "feature": [],
    }
    test_cases = [
        (
            """"Should collect one for each category of bucket type""",
            [
                Ticket(
                    board_id=1,
                    ticket_id=1,
                    resource_id=1,
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
                            date=datetime(year=2000, month=1, day=4),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=DONE_STATUS,
                        ),
                    ],
                ),
                Ticket(
                    board_id=1,
                    ticket_id=2,
                    resource_id=2,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Bug",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=2,
                            date=datetime(year=2000, month=1, day=3),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=2,
                            date=datetime(year=2000, month=1, day=4),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=2,
                            date=datetime(year=2000, month=1, day=5),
                            status=DONE_STATUS,
                        ),
                    ],
                ),
                Ticket(
                    board_id=1,
                    ticket_id=3,
                    resource_id=3,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Maintenance",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=3,
                            date=datetime(year=2000, month=1, day=3),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=3,
                            date=datetime(year=2000, month=1, day=4),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=3,
                            date=datetime(year=2000, month=1, day=5),
                            status=DONE_STATUS,
                        ),
                    ],
                ),
                Ticket(
                    board_id=1,
                    ticket_id=4,
                    resource_id=4,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Unplanned",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=4,
                            date=datetime(year=2000, month=1, day=3),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=4,
                            date=datetime(year=2000, month=1, day=4),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=4,
                            date=datetime(year=2000, month=1, day=5),
                            status=DONE_STATUS,
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
                    board_id=1,
                    ticket_id=1,
                    resource_id=1,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=2),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=IN_PROGRESS_STATUS,
                        ),  # week 1 has 5 days worth of effort and ends on Jan 7
                        # week 2 has 5 days worth of effort and starts and ends from
                        # Jan 10 - Jan 14 business days, so expect to see 5 days
                        # of effort on week 1, and 5 days on week 2.
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=18),
                            status=DONE_STATUS,
                        ),  # Week 3 is from Jan 17 to Jan 21 business days,
                        # so expect to see 1 day of effort for this
                        # status.
                    ],
                ),
                Ticket(
                    board_id=1,
                    ticket_id=2,
                    resource_id=2,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=2),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=IN_PROGRESS_STATUS,
                        ),  # week 1 has 5 days worth of effort and ends on Jan 7
                        # week 2 has 5 days worth of effort and starts and ends from
                        # Jan 10 - Jan 14
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=19),
                            status=DONE_STATUS,
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
                    board_id=1,
                    ticket_id=1,
                    resource_id=1,
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
                            date=datetime(
                                year=2000, month=1, day=19, hour=12, minute=0, second=0
                            ),
                            status=IN_PROGRESS_STATUS,
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
                    board_id=1,
                    ticket_id=1,
                    resource_id=1,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3, hour=8, minute=30),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3, hour=9, minute=30),
                            status=IN_PROGRESS_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000, month=1, day=3, hour=12, minute=30
                            ),
                            status=DONE_STATUS,
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
                    board_id=1,
                    ticket_id=1,
                    resource_id=1,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Feature",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000, month=1, day=3, hour=12, minute=0, second=0
                            ),
                            status=TO_DO_STATUS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000, month=1, day=4, hour=8, minute=0, second=0
                            ),
                            status=IN_PROGRESS_STATUS,
                        ),  # 3.7 days of effort (24 - 8 = 16 hours of effort
                        # after issue in progress for the day) for week 1
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000, month=1, day=10, hour=12, minute=0, second=0
                            ),
                            status=TO_DO_STATUS,
                        ),  # .5 days of effort here for week 2
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(
                                year=2000, month=1, day=12, hour=12, minute=0, second=0
                            ),
                            status=IN_PROGRESS_STATUS,
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
                            status=DONE_STATUS,
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
