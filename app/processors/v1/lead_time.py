"""Process lead time and throughput data.

Lead time is weekly data represented by the story_lead_time key.
One list entry for each ticket that was closed during the week.
The value is the number of days since the ticket was created.
Throughput is weekly data represented by the throughput key.
One list entry for each ticket that was closed during the week.
The value is always 1.
"""
from typing import List

from app.models import Ticket

from .types import ChartData, DateValue
from .utils import (
    days_between_dates,
    is_completed_ticket,
    is_defect_ticket,
    is_epic_or_subtask_ticket,
    values_by_week,
)


def to_lead_time(ticket: Ticket) -> DateValue:
    """Get the DateValue for a ticket's lead time."""
    creation_date = ticket.status_history[0].date
    done_date = ticket.status_history[-1].date

    return DateValue(done_date, days_between_dates(creation_date, done_date))


def to_throughput(ticket: Ticket) -> DateValue:
    """Get the DateValue for a ticket's throughput."""
    done_date = ticket.status_history[-1].date
    return DateValue(done_date, 1)


def by_lead_time(ticket: Ticket) -> bool:
    """Filter out unwanted tickets."""
    return (
        not is_epic_or_subtask_ticket(ticket)
        and not is_defect_ticket(ticket)
        and is_completed_ticket(ticket)
    )


def process_lead_time(tickets: List[Ticket]) -> ChartData:
    """Process tickets into lead time and throughput data."""
    return {
        "story_lead_time": values_by_week(
            [to_lead_time(ticket) for ticket in tickets if by_lead_time(ticket)]
        ),
        "throughput": values_by_week(
            [to_throughput(ticket) for ticket in tickets if by_lead_time(ticket)]
        ),
    }
