"""Test process_cycle_time_defect."""
from datetime import datetime

from app.models import StatusHistory, Ticket, TicketPriority, TicketStatus, TicketType
from app.processors.v2.cycle_time_defect import process_cycle_time_defect


def test_process_cycle_time_defect():
    """Test process_cycle_time_defect function."""
    cases = [
        (
            """Should calculate cycle time with expected
            defect and defect priorities""",
            [
                Ticket(
                    collector_target_id=1,
                    resource_id="1",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.FEATURE,
                    priority=TicketPriority.HIGHEST,
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
                            status=TicketStatus.IN_PROGRESS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                        ),
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="2",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.DEFECT,
                    priority=TicketPriority.HIGHEST,
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
                            status=TicketStatus.IN_PROGRESS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                        ),
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="3",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.DEFECT,
                    priority=TicketPriority.HIGH,
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
                            status=TicketStatus.IN_PROGRESS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                        ),
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="4",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.DEFECT,
                    priority=TicketPriority.MEDIUM,
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
                            status=TicketStatus.IN_PROGRESS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                        ),
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="5",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.DEFECT,
                    priority=TicketPriority.LOW,
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
                            status=TicketStatus.IN_PROGRESS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                        ),
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="6",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.DEFECT,
                    priority=TicketPriority.LOWEST,
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
                            status=TicketStatus.IN_PROGRESS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                        ),
                    ],
                ),
                Ticket(
                    collector_target_id=1,
                    resource_id="7",
                    assignee="someone",
                    status=TicketStatus.DONE,
                    ticket_type=TicketType.DEFECT,
                    priority=TicketPriority.LOWEST,
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
                            status=TicketStatus.IN_PROGRESS,
                        ),
                        StatusHistory(
                            ticket_id=1,
                            date=datetime(year=2000, month=1, day=5),
                            status=TicketStatus.DONE,
                        ),
                    ],
                ),
            ],
            (
                {
                    "2000-01-03": [1],
                },
                {"2000-01-03": [1, 1, 1, 1, 1, 1]},
                {"2000-01-03": [1]},
                {"2000-01-03": [1]},
                {"2000-01-03": [1]},
                {"2000-01-03": [1]},
                {"2000-01-03": [1, 1]},
            ),
        )
    ]

    for case in cases:
        _, case_input, expected = case
        actual = process_cycle_time_defect(case_input)
        assert expected == actual
