"""Utilities."""
from datetime import datetime, timedelta
from typing import Callable, List, TypeVar

from app import config
from app.models import Ticket

from .types import DateValue, WeeklyData

T = TypeVar("T")
V = TypeVar("V")

IN_PROGRESS = "In Progress"


def flat_map(items: List[T], func: Callable[[T], List[V]]) -> List[V]:
    """Map and flatten."""
    result: List[V] = []
    for item in items:
        result.extend(func(item))
    return result


def get_fmt_year_week(date: datetime) -> str:
    """Return the formatted <year_number>_<week_number> of date."""
    iso_date = date.isocalendar()
    week_str = f"{iso_date.week}" if iso_date.week >= 10 else f"0{iso_date.week}"
    return f"{iso_date.year}_{week_str}"


def values_by_week(data: List[DateValue]) -> WeeklyData:
    """Convert data to format the charts can consume."""
    values: WeeklyData = {}

    for item in data:
        year_week_str = get_fmt_year_week(item.date)
        values.setdefault(year_week_str, []).append(item.value)

    return values


def days_between_dates(start: datetime, end: datetime) -> float:
    """Determine the number of days between two dates, rounded to one decimal place."""
    hours_per_day = 24
    seconds_per_day = 60 * 60 * hours_per_day
    time_delta = end - start
    actual_days_effort = time_delta.days + time_delta.seconds / seconds_per_day

    saturday = 5
    sunday = 6
    while start < end:
        if start.weekday() in [saturday, sunday]:
            actual_days_effort -= 1
        start += timedelta(days=1)

    if actual_days_effort * hours_per_day < config.MIN_EXPECTED_CYCLE_TIME_HOURS:
        return 0

    precision_factor = 10

    return round(actual_days_effort * precision_factor) / precision_factor


def is_defect_ticket(ticket: Ticket) -> bool:
    """Return boolean representing if ticket is for a defect."""
    return ticket.ticket_type in config.JIRA_TICKET_TYPE_BUCKETS["defect_effort"]


def is_completed_ticket(ticket: Ticket) -> bool:
    """Return boolean representing if ticket is completed."""
    return (
        len(ticket.status_history) >= 1
        and ticket.status_history[0].status == "To Do"
        and ticket.status_history[-1].status == "Done"
    )


def is_epic_or_subtask_ticket(ticket: Ticket) -> bool:
    """Return boolean representing if ticket is either an epic or subtask."""
    return ticket.ticket_type in ["Epic", "Sub-task"]


def ticket_was_started(ticket: Ticket) -> bool:
    """Return boolean representing if ticket was started."""
    return any((history.status == IN_PROGRESS for history in ticket.status_history))


def get_first_in_progress_date(ticket: Ticket) -> datetime:
    """Return date ticket first moved to in progress."""
    return next(
        history.date
        for history in ticket.status_history
        if history.status == IN_PROGRESS
    )


def is_in_progress(ticket: Ticket) -> bool:
    """Return boolean representing if ticket is in progress."""
    return ticket.status == IN_PROGRESS
