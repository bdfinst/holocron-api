"""Utilities."""

from datetime import datetime, timedelta, timezone
from typing import Callable, Iterator, List, Optional, Tuple, TypeVar

from app import config
from app.models import (
    ProjectIssue,
    ProjectIssueSeverity,
    Ticket,
    TicketStatus,
    TicketType,
)

T = TypeVar("T")
V = TypeVar("V")


def flat_map(items: List[T], func: Callable[[T], List[V]]) -> List[V]:
    """Map and flatten."""
    result: List[V] = []
    for item in items:
        result.extend(func(item))
    return result


def get_monday(date: datetime) -> datetime:
    """Return the monday of a given date's week."""
    return date - timedelta(
        days=date.weekday(),
        hours=date.hour,
        minutes=date.minute,
        seconds=date.second,
        microseconds=date.microsecond,
    )


def get_monday_string(date: datetime) -> str:
    """Return the formatted YYYY-MM-DD of the date's week's Monday."""
    monday = get_monday(date)
    date_format = "%Y-%m-%d"
    return monday.strftime(date_format)


def average(numbers: List[float], default: float = 0) -> float:
    """Get average of list of numbers."""
    return default if not numbers else sum(numbers) / len(numbers)


def total_days_diff_workflow(start: datetime, end: datetime) -> float:
    """Return the total number of days between two dates."""
    hours_per_day = 24
    seconds_per_day = 60 * 60 * hours_per_day
    time_delta = end - start
    actual_days_effort = time_delta.days + time_delta.seconds / seconds_per_day

    if actual_days_effort * hours_per_day < config.MIN_EXPECTED_CYCLE_TIME_HOURS:
        return 0
    precision_factor = 10
    return round(actual_days_effort * precision_factor) / precision_factor


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
    return ticket.ticket_type == TicketType.DEFECT


def is_completed_ticket(ticket: Ticket) -> bool:
    """Return boolean representing if ticket is completed."""
    return (
        len(ticket.status_history) >= 1
        and ticket.status_history[0].status == TicketStatus.TO_DO
        and ticket.status_history[-1].status == TicketStatus.DONE
    )


def is_no_effort_ticket(ticket: Ticket) -> bool:
    """Return boolean representing if person did not work on ticket."""
    return (
        len(ticket.status_history) == 1
        and ticket.status_history[-1].status == TicketStatus.DONE
    )


def is_epic_or_subtask_ticket(ticket: Ticket) -> bool:
    """Return boolean representing if ticket is either an epic or subtask."""
    return ticket.ticket_type in ["Epic", "Sub-task"]


def ticket_was_started(ticket: Ticket) -> bool:
    """Return boolean representing if ticket was started."""
    return any(
        (
            history.status == TicketStatus.IN_PROGRESS
            for history in ticket.status_history
        )
    )


def get_first_in_progress_date(ticket: Ticket) -> datetime:
    """Return date ticket first moved to in progress."""
    return next(
        history.date
        for history in ticket.status_history
        if history.status == TicketStatus.IN_PROGRESS
    )


def is_in_progress(ticket: Ticket) -> bool:
    """Return boolean representing if ticket is in progress."""
    return ticket.status == TicketStatus.IN_PROGRESS


def is_between_dates(
    date_to_check: datetime, first_date: datetime, second_date: Optional[datetime]
) -> bool:
    """Return boolean representing if date_to_check is between first and second date."""
    date_to_check = date_to_check.replace(tzinfo=timezone.utc)
    first_date = first_date.replace(tzinfo=timezone.utc)
    if second_date is not None:
        second_date = second_date.replace(tzinfo=timezone.utc)

    if second_date is not None and second_date < first_date:
        raise ValueError("first_date must not be after second_date")
    if date_to_check < first_date:
        return False
    if second_date is None:
        return True
    if date_to_check > second_date:
        return False
    return True


def get_issues_historical_data_stream(
    issues: Iterator[ProjectIssue],
) -> Iterator[Tuple[str, ProjectIssueSeverity]]:
    """Yield issues metrics."""
    for issue in issues:
        end_date = (
            issue.closed_date
            if issue.closed_date is not None
            else get_monday(datetime.now() + timedelta(days=7))
        ).astimezone(timezone.utc)
        date_to_check = get_monday(issue.created_date).astimezone(
            timezone.utc
        ) + timedelta(days=7)
        while date_to_check <= end_date and date_to_check < datetime.now(timezone.utc):
            monday_string = get_monday_string(date_to_check)
            date_to_check += timedelta(days=7)
            yield monday_string, issue.severity
