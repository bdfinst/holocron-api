"""Test data for ticket_boards."""
from datetime import datetime, timedelta

from app.models import (
    StatusHistory,
    Ticket,
    TicketBoard,
    TicketPriority,
    TicketStatus,
    TicketType,
)

all_status_history_types = [
    StatusHistory(
        ticket_id=1, date=datetime(year=2000, month=1, day=3), status=TicketStatus.TO_DO
    ),
    StatusHistory(
        ticket_id=1, date=datetime(year=2000, month=1, day=10), status=TicketStatus.DONE
    ),
    StatusHistory(
        ticket_id=1,
        date=datetime(year=2000, month=1, day=7),
        status=TicketStatus.IN_PROGRESS,
    ),
]

in_progress_history_types = [
    StatusHistory(
        ticket_id=2,
        date=datetime(year=2000, month=1, day=7) - timedelta(hours=1),
        status=TicketStatus.TO_DO,
    ),
    StatusHistory(
        ticket_id=2,
        date=datetime(year=2000, month=1, day=7),
        status=TicketStatus.IN_PROGRESS,
    ),
]

tickets = [
    Ticket(
        collector_target_id=1,
        resource_id=1,
        assignee="nobody",
        status=TicketStatus.DONE,
        ticket_type=TicketType.DEFECT,
        priority=TicketPriority.HIGHEST,
        status_history=all_status_history_types,
        super_ticket_id=None,
    ),
    Ticket(
        collector_target_id=2,
        resource_id=2,
        assignee="somebody",
        status=TicketStatus.IN_PROGRESS,
        ticket_type=TicketType.FEATURE,
        priority=TicketPriority.LOWEST,
        status_history=in_progress_history_types,
        super_ticket_id=None,
    ),
]


def create_ticket_board(
    id=1,
    collector_id=1,
    type="WORKFLOW",
    name="mock_ticket_board",
    url="https://test.com",
    tickets=tickets,
    last_collected=datetime(2020, 6, 17).timestamp(),
    resource_id=1,
    team_id=None,
):
    """Create mock ticket_board object with default values."""
    ticket_board = TicketBoard(
        collector_id=collector_id,
        type=type,
        name=name,
        url=url,
        tickets=tickets,
        last_collected=last_collected,
        resource_id=resource_id,
        team_id=team_id,
    )
    ticket_board.id = id
    return ticket_board


mock_ticket_boards = [create_ticket_board()]
mock_ticket_boards_last_collected = [
    create_ticket_board(
        tickets=[],
        last_collected=datetime(1999, 2, 2).timestamp(),
    ),
    create_ticket_board(tickets=[], last_collected=datetime(2022, 2, 2).timestamp()),
    create_ticket_board(tickets=[], last_collected=datetime(2010, 2, 2).timestamp()),
]
