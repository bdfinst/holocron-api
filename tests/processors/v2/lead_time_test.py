"""Test process_lead_time."""
from datetime import datetime

from app.models import StatusHistory, Ticket, TicketStatus
from app.processors.v2.lead_time import process_lead_time


def test_process_lead_time():
    """Test process_lead_time function."""
    cases = [
        (
            """Should calculate lead time and throughput""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="28",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type="Task",
                    priority="Highest",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.TO_DO,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                        ),
                    ],
                ),
                # should not count this ticket since it is an epic or subtask
                Ticket(
                    collector_target_id=1,
                    resource_id="27",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type="Epic",
                    priority="Dumpster Full",
                    super_ticket_id=None,
                    status_history=[
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=3),
                            status=TicketStatus.TO_DO,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=4),
                            status=TicketStatus.DONE,
                        ),
                    ],
                ),
            ],
            ({"2000-01-03": [2]}, {"2000-01-03": [1]}),
        )
    ]

    for case in cases:
        _, case_input, expected = case
        actual = process_lead_time(case_input)
        assert expected == actual
