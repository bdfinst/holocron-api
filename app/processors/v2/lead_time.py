"""Process lead time and throughput data.

Lead time is weekly data represented by the story_lead_time key.
One list entry for each ticket that was closed during the week.
The value is the number of days since the ticket was created.
Throughput is weekly data represented by the throughput key.
One list entry for each ticket that was closed during the week.
The value is always 1.
"""
from typing import List, NamedTuple

from app.models import Ticket
from app.processors.v1.utils import (
    days_between_dates,
    is_completed_ticket,
    is_defect_ticket,
    is_epic_or_subtask_ticket,
)

from .types import ChartData, DateValue
from .utils import get_monday_string


def to_lead_time(ticket: Ticket) -> DateValue:
    """Get the DateValue for a ticket's lead time."""
    creation_date = ticket.status_history[0].date
    done_date = ticket.status_history[-1].date

    return DateValue(
        get_monday_string(done_date), days_between_dates(creation_date, done_date)
    )


def to_throughput(ticket: Ticket) -> DateValue:
    """Get the DateValue for a ticket's throughput."""
    done_date = ticket.status_history[-1].date
    return DateValue(get_monday_string(done_date), 1)


def by_lead_time(ticket: Ticket) -> bool:
    """Filter out unwanted tickets."""
    return (
        not is_epic_or_subtask_ticket(ticket)
        and not is_defect_ticket(ticket)
        and is_completed_ticket(ticket)
    )


class LeadTimeThroughputChartData(NamedTuple):
    """Type of chart data for lead time and throughput."""

    lead_time: ChartData
    throughput: ChartData


def process_lead_time(tickets: List[Ticket]) -> LeadTimeThroughputChartData:
    """Process tickets into lead time and throughput data."""
    lead_time_values = [
        to_lead_time(ticket) for ticket in tickets if by_lead_time(ticket)
    ]
    throughput_values = [
        to_throughput(ticket) for ticket in tickets if by_lead_time(ticket)
    ]

    result = LeadTimeThroughputChartData({}, {})
    for item in lead_time_values:
        result.lead_time.setdefault(item.date, []).append(item.value)
    for item in throughput_values:
        result.throughput.setdefault(item.date, []).append(item.value)
    return result
