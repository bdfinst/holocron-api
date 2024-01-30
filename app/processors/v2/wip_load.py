"""Process WIP load data.

WIP load data is a number representing the current number of WIP tickets.
"""

from typing import List

from app.models import Ticket

from .utils import is_epic_or_subtask_ticket, is_in_progress


def by_wipload(ticket: Ticket) -> bool:
    """Decide whether a ticket is wip ticket."""
    return not is_epic_or_subtask_ticket(ticket) and is_in_progress(ticket)


def process_wip_load(tickets: List[Ticket]) -> int:
    """Process tickets into WIP load data."""
    return len([ticket for ticket in tickets if by_wipload(ticket)])
