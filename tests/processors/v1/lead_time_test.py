"""Test process_lead_time."""
from datetime import datetime

from pytest import fixture

from app.models import StatusHistory, Ticket
from app.processors.v1 import utils
from app.processors.v1.lead_time import process_lead_time
from tests.mocks import config

DONE_STATUS = "Done"
TO_DO_STATUS = "To Do"


@fixture
def mock_config(monkeypatch):
    """Mock configuration."""
    monkeypatch.setattr(utils, "config", config)
    yield config
    config.reset()


def test_process_lead_time(mock_config):
    """Test process_lead_time function."""
    mock_config.TICKET_TYPE_BUCKETS = {
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
    mock_config.TICKET_PRIORITY_MAPPINGS = {
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
            """Should calculate lead time and throughput""",
            [
                Ticket(
                    board_id=1,
                    ticket_id=28,
                    resource_id=28,
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
                            date=datetime(year=2000, month=1, day=5),
                            status=DONE_STATUS,
                        ),
                    ],
                ),
                # should not count this ticket since it is an epic or subtask
                Ticket(
                    board_id=1,
                    ticket_id=27,
                    resource_id=27,
                    assignee="someone",
                    status=DONE_STATUS,
                    ticket_type="Epic",
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
                            status=DONE_STATUS,
                        ),
                    ],
                ),
            ],
            {"story_lead_time": {"2000_01": [2]}, "throughput": {"2000_01": [1]}},
        )
    ]

    for case in cases:
        _, case_input, expected = case
        actual = process_lead_time(case_input)
        assert expected == actual
