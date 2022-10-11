"""Test data for ticket_boards."""
from datetime import datetime, timedelta

from app.models import StatusHistory, Ticket, TicketBoard

all_status_history_types = [
    StatusHistory(
        ticket_id=1, date=datetime(year=2000, month=1, day=3), status="To Do"
    ),
    StatusHistory(
        ticket_id=1, date=datetime(year=2000, month=1, day=10), status="Done"
    ),
    StatusHistory(
        ticket_id=1, date=datetime(year=2000, month=1, day=7), status="In Progress"
    ),
]

in_progress_history_types = [
    StatusHistory(
        ticket_id=2,
        date=datetime(year=2000, month=1, day=7) - timedelta(hours=1),
        status="To Do",
    ),
    StatusHistory(
        ticket_id=2, date=datetime(year=2000, month=1, day=7), status="In Progress"
    ),
]

tickets = [
    Ticket(
        board_id=1,
        ticket_id=1,
        assignee="nobody",
        status="Done",
        ticket_type="Bug",
        priority="Highest",
        status_history=all_status_history_types,
    ),
    Ticket(
        board_id=2,
        ticket_id=2,
        assignee="somebody",
        status="In Progress",
        ticket_type="Feature",
        priority="Lowest",
        status_history=in_progress_history_types,
    ),
]

mock_ticket_boards = [
    TicketBoard(
        collector_id=1,
        name="mock_ticket_board",
        url="https://jira.com/board",
        tickets=tickets,
        last_collected=datetime(2020, 6, 17).timestamp(),
    )
]
mock_ticket_boards_last_collected = [
    TicketBoard(
        collector_id=2,
        name="mock_ticket_board_lastCollected",
        url="https://jira/1",
        tickets=[],
        last_collected=datetime(1999, 2, 2).timestamp(),
    ),
    TicketBoard(
        collector_id=2,
        name="mock_ticket_board_lastCollected",
        url="https://jira/2",
        tickets=[],
        last_collected=datetime(2022, 2, 2).timestamp(),
    ),
    TicketBoard(
        collector_id=2,
        name="mock_ticket_board_lastCollected",
        url="https://jira/2",
        tickets=[],
        last_collected=datetime(2010, 2, 2).timestamp(),
    ),
]
