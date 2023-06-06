"""Test process_cycle_time_defect."""
from datetime import datetime

from pytest import fixture

from app.models import StatusHistory, Ticket
from app.processors.v1 import utils
from app.processors.v1.cycle_time_defect import process_cycle_time_defect
from tests.mocks import config

DONE_STATUS = "Done"
TO_DO_STATUS = "To Do"
IN_PROGRESS_STATUS = "In Progress"


@fixture
def mock_config(monkeypatch):
    """Mock configuration."""
    monkeypatch.setattr(utils, "config", config)
    yield config
    config.reset()


def test_process_cycle_time_defect(mock_config):
    """Test process_cycle_time_defect function."""
    mock_config.JIRA_TICKET_TYPE_BUCKETS = {
        "defect_effort": ["Bug", "Anomaly"],
        "unplanned": ["Unplanned"],
        "maintenance": ["Maintenance"],
        "feature": [],
    }
    mock_config.TICKET_PRIORITIES = {
        "HIGHEST": "Highest",
        "HIGH": "High",
        "MEDIUM": "Medium",
        "LOW": "Low",
        "LOWEST": "Lowest",
    }
    mock_config.JIRA_PRIORITY_MAPPINGS = {
        mock_config.TICKET_PRIORITIES["HIGHEST"]: mock_config.TICKET_PRIORITIES[
            "HIGHEST"
        ],
        mock_config.TICKET_PRIORITIES["HIGH"]: mock_config.TICKET_PRIORITIES["HIGH"],
        mock_config.TICKET_PRIORITIES["MEDIUM"]: mock_config.TICKET_PRIORITIES[
            "MEDIUM"
        ],
        mock_config.TICKET_PRIORITIES["LOW"]: mock_config.TICKET_PRIORITIES["LOW"],
        mock_config.TICKET_PRIORITIES["LOWEST"]: mock_config.TICKET_PRIORITIES[
            "LOWEST"
        ],
        1: mock_config.TICKET_PRIORITIES["HIGHEST"],
        2: mock_config.TICKET_PRIORITIES["HIGH"],
        3: mock_config.TICKET_PRIORITIES["MEDIUM"],
        4: mock_config.TICKET_PRIORITIES["LOW"],
        5: mock_config.TICKET_PRIORITIES["LOWEST"],
        "Critical": mock_config.TICKET_PRIORITIES["HIGHEST"],
    }
    mock_config.DEFAULT_TICKET_PRIORITY = mock_config.TICKET_PRIORITIES["LOWEST"]

    cases = [
        (
            """Should calculate cycle time with expected
            defect and defect priorities""",
            [
                Ticket(
                    board_id=1,
                    ticket_id=1,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Task",
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
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Bug",
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
                    ticket_id=3,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Bug",
                    priority="High",
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
                    ticket_id=4,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Bug",
                    priority="Medium",
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
                    ticket_id=5,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Bug",
                    priority="Low",
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
                    ticket_id=6,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Bug",
                    priority="Lowest",
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
                    ticket_id=7,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Bug",
                    priority="Dumpster Full",
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
            ],
            {
                "dev_cycle_time": {
                    "2000_01": [1],
                },
                "defect_rate": {"2000_01": [1, 1, 1, 1, 1, 1]},
                "highest_defects": {"2000_01": [1]},
                "high_defects": {"2000_01": [1]},
                "medium_defects": {"2000_01": [1]},
                "low_defects": {"2000_01": [1]},
                "lowest_defects": {"2000_01": [1, 1]},
            },
        )
    ]

    for case in cases:
        _, case_input, expected = case
        actual = process_cycle_time_defect(case_input)
        assert expected == actual
