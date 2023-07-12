"""Process cycle time and defect rate data.

Cycle time is weekly data represented by the dev_cycle_time key.
One list entry for each ticket that was closed in the week.
The value of that entry is the number of days the ticket was in progress.
Defect rate is weekly data with keys for each priority.
One list entry for each defect ticket opened with the given priority in the week.
The value is always 1.
"""
from typing import Dict, List, NamedTuple

from app import config
from app.models import Ticket
from app.processors.v1.utils import (
    days_between_dates,
    get_first_in_progress_date,
    is_completed_ticket,
    is_defect_ticket,
    is_epic_or_subtask_ticket,
    ticket_was_started,
)

from .types import ChartData, DateValue
from .utils import get_monday_string


def by_dev_cycle_time(ticket: Ticket) -> bool:
    """Filter out unwanted tickets."""
    return (
        ticket_was_started(ticket)
        and is_completed_ticket(ticket)
        and not is_epic_or_subtask_ticket(ticket)
        and not is_defect_ticket(ticket)
    )


def to_dev_cycle_time(ticket: Ticket) -> DateValue:
    """Get the DateValue for a ticket's cycle time."""
    last_status_date = ticket.status_history[-1].date

    return DateValue(
        get_monday_string(last_status_date),
        days_between_dates(get_first_in_progress_date(ticket), last_status_date),
    )


def to_defect_rate(ticket: Ticket) -> DateValue:
    """Get the DateValue for a defect."""
    return DateValue(get_monday_string(ticket.status_history[0].date), 1)


def by_defect_rate(ticket: Ticket) -> bool:
    """Return boolean representing if ticket is a defect."""
    return ticket.ticket_type in config.TICKET_TYPE_BUCKETS["defect_effort"]


def by_defect_rate_priority(tickets: List[Ticket]) -> Dict[str, List[DateValue]]:
    """Return mapping of defect tickets based on priority."""
    result: Dict[str, List[DateValue]] = {
        "HIGHEST": [],
        "HIGH": [],
        "MEDIUM": [],
        "LOW": [],
        "LOWEST": [],
    }
    for ticket in tickets:
        mapped_priority_label = config.TICKET_PRIORITY_MAPPINGS.get(
            ticket.priority, config.DEFAULT_TICKET_PRIORITY
        )
        if mapped_priority_label == config.TICKET_PRIORITIES["HIGHEST"]:
            result["HIGHEST"].append(to_defect_rate(ticket))
        elif mapped_priority_label == config.TICKET_PRIORITIES["HIGH"]:
            result["HIGH"].append(to_defect_rate(ticket))
        elif mapped_priority_label == config.TICKET_PRIORITIES["MEDIUM"]:
            result["MEDIUM"].append(to_defect_rate(ticket))
        elif mapped_priority_label == config.TICKET_PRIORITIES["LOW"]:
            result["LOW"].append(to_defect_rate(ticket))
        else:
            result["LOWEST"].append(to_defect_rate(ticket))
    return result


class CycleTimeDefectChartData(NamedTuple):
    """Type of chart data for cycle time and defect rate."""

    cycle_time: ChartData
    defect_rate: ChartData
    highest_defects: ChartData
    high_defects: ChartData
    medium_defects: ChartData
    low_defects: ChartData
    lowest_defects: ChartData


def process_cycle_time_defect(tickets: List[Ticket]) -> CycleTimeDefectChartData:
    """Process tickets into cycle time and defect data."""
    cycle_time_values = [
        to_dev_cycle_time(ticket) for ticket in tickets if by_dev_cycle_time(ticket)
    ]
    defect_rate_values = [
        to_defect_rate(ticket) for ticket in tickets if by_defect_rate(ticket)
    ]
    defects_by_priority_values = by_defect_rate_priority(
        [ticket for ticket in tickets if by_defect_rate(ticket)]
    )

    result = CycleTimeDefectChartData({}, {}, {}, {}, {}, {}, {})
    for item in cycle_time_values:
        result.cycle_time.setdefault(item.date, []).append(item.value)
    for item in defect_rate_values:
        result.defect_rate.setdefault(item.date, []).append(item.value)
    for item in defects_by_priority_values["HIGHEST"]:
        result.highest_defects.setdefault(item.date, []).append(item.value)
    for item in defects_by_priority_values["HIGH"]:
        result.high_defects.setdefault(item.date, []).append(item.value)
    for item in defects_by_priority_values["MEDIUM"]:
        result.medium_defects.setdefault(item.date, []).append(item.value)
    for item in defects_by_priority_values["LOW"]:
        result.low_defects.setdefault(item.date, []).append(item.value)
    for item in defects_by_priority_values["LOWEST"]:
        result.lowest_defects.setdefault(item.date, []).append(item.value)
    return result
