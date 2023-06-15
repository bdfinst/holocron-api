"""Process cycle time and defect rate data.

Cycle time is weekly data represented by the dev_cycle_time key.
One list entry for each ticket that was closed in the week.
The value of that entry is the number of days the ticket was in progress.
Defect rate is weekly data with keys for each priority.
One list entry for each defect ticket opened with the given priority in the week.
The value is always 1.
"""
from typing import List

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
from .utils import values_by_week


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
        last_status_date,
        days_between_dates(get_first_in_progress_date(ticket), last_status_date),
    )


def to_defect_rate(ticket: Ticket) -> DateValue:
    """Get the DateValue for a defect."""
    return DateValue(ticket.status_history[0].date, 1)


def by_defect_rate(ticket: Ticket) -> bool:
    """Return boolean representing if ticket is a defect."""
    return ticket.ticket_type in config.JIRA_TICKET_TYPE_BUCKETS["defect_effort"]


def by_defect_rate_priority(priority: str, ticket: Ticket) -> bool:
    """Return boolean representing if ticket has priority and is a defect."""
    mapped_priority_label = config.JIRA_PRIORITY_MAPPINGS.get(
        ticket.priority, config.DEFAULT_TICKET_PRIORITY
    )
    return by_defect_rate(ticket) and mapped_priority_label == priority


def process_cycle_time_defect(tickets: List[Ticket]) -> ChartData:
    """Process tickets into cycle time and defect data."""
    return {
        "dev_cycle_time": values_by_week(
            [
                to_dev_cycle_time(ticket)
                for ticket in tickets
                if by_dev_cycle_time(ticket)
            ]
        ),
        "defect_rate": values_by_week(
            [to_defect_rate(ticket) for ticket in tickets if by_defect_rate(ticket)]
        ),
        "highest_defects": values_by_week(
            [
                to_defect_rate(ticket)
                for ticket in tickets
                if by_defect_rate_priority(config.TICKET_PRIORITIES["HIGHEST"], ticket)
            ]
        ),
        "high_defects": values_by_week(
            [
                to_defect_rate(ticket)
                for ticket in tickets
                if by_defect_rate_priority(config.TICKET_PRIORITIES["HIGH"], ticket)
            ]
        ),
        "medium_defects": values_by_week(
            [
                to_defect_rate(ticket)
                for ticket in tickets
                if by_defect_rate_priority(config.TICKET_PRIORITIES["MEDIUM"], ticket)
            ]
        ),
        "low_defects": values_by_week(
            [
                to_defect_rate(ticket)
                for ticket in tickets
                if by_defect_rate_priority(config.TICKET_PRIORITIES["LOW"], ticket)
            ]
        ),
        "lowest_defects": values_by_week(
            [
                to_defect_rate(ticket)
                for ticket in tickets
                if by_defect_rate_priority(config.TICKET_PRIORITIES["LOWEST"], ticket)
            ]
        ),
    }
