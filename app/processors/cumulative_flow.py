"""Process cumulative flow data.

Cumulative flow data is weekly data that contains backlog and wip keys.
One list entry for each ticket that was in the corresponding status that week.
The value of that entry is the age of the ticket in days.
This is calculated from the date the ticket was created,
and compared to either the end of the week, or when the ticket changed state.
"""
from datetime import datetime, timedelta
from typing import List, NamedTuple, Union

from app.models import Ticket

from .types import ChartData, DateValue
from .utils import (
    days_between_dates,
    flat_map,
    is_completed_ticket,
    is_epic_or_subtask_ticket,
    values_by_week,
)

TO_DO_STATUS = "To Do"
IN_PROGRESS_STATUS = "In Progress"
NOT_STARTED_STATUS = ""

ONE_WEEK_IN_SECONDS = 60 * 60 * 24 * 7


class DateValueWithStatus(NamedTuple):
    """DateValue with an additional status string."""

    date: datetime
    value: Union[int, float]
    status: str


def status_snap_shot(date: datetime, ticket: Ticket) -> str:
    """Check the status of a ticket at a given time."""
    next_status_date = ticket.status_history[0].date
    if date < next_status_date:
        return NOT_STARTED_STATUS
    index = 0
    while date > next_status_date and index < len(ticket.status_history) - 1:
        index += 1
        next_status_date = ticket.status_history[index].date
    if date < next_status_date:
        index -= 1
    return ticket.status_history[index].status


def build_date_list(dates: List[datetime]) -> List[datetime]:
    """Create a list of dates.

    Includes each end of week (Friday at 11:59pm) and each status change.
    Takes a list of status change dates, and adds each end of week to the list in order.
    """
    index = 0
    date_to_check = dates[index]
    days_to_add = {
        0: 4,  # monday is 0, we add 4 days
        1: 3,
        2: 2,
        3: 1,
        4: 0,
        5: 6,
        6: 5,
    }
    while date_to_check < dates[-1]:
        date_to_check += timedelta(days=days_to_add[date_to_check.weekday()])
        if date_to_check.hour == 23 and date_to_check.minute == 59:
            date_to_check += timedelta(days=7)
        date_to_check = date_to_check.replace(hour=23, minute=59)
        index += 1
        if date_to_check > dates[index]:
            date_to_check = dates[index]
        else:
            dates.insert(index, date_to_check)
    return dates


def is_unique(
    datevalue: DateValueWithStatus, datevaluelist: List[DateValueWithStatus]
) -> bool:
    """Check if the list contains another entry with the same week and status."""
    match = next(
        (
            d
            for d in datevaluelist
            if d.date.isocalendar().week == datevalue.date.isocalendar().week
            and d.status == datevalue.status
        ),
        None,
    )
    return match is None


def to_age_data(ticket: Ticket) -> List[DateValueWithStatus]:
    """Create the DateValueWithStatus list for a given ticket."""
    date_list = [history.date for history in ticket.status_history]
    if not is_completed_ticket(ticket):
        date_list.append(datetime.now())
    date_list = build_date_list(date_list)
    result: List[DateValueWithStatus] = []
    for date in date_list:
        days = days_between_dates(date_list[0], date)
        if len(result) > 0:
            result.append(DateValueWithStatus(date, days, result[-1].status))
        result.append(DateValueWithStatus(date, days, status_snap_shot(date, ticket)))
    if is_completed_ticket(ticket):
        days = days_between_dates(date_list[0], date_list[-1])
        result.append(DateValueWithStatus(date_list[-1], days, result[-1].status))
        result.append(
            DateValueWithStatus(
                date_list[-1],
                days,
                status_snap_shot(date_list[-1], ticket),
            )
        )

    return [
        item
        for index, item in enumerate(result)
        if is_unique(item, result[index + 1 :])
    ]


def process_cumulative_flow(tickets: List[Ticket]) -> ChartData:
    """Process tickets into cumulative flow data."""
    tickets_that_matter = [
        ticket for ticket in tickets if not is_epic_or_subtask_ticket(ticket)
    ]
    age_history = flat_map(tickets_that_matter, to_age_data)

    return {
        "backlog": values_by_week(
            [
                DateValue(item.date, item.value)
                for item in age_history
                if item.status == TO_DO_STATUS and item.value != 0
            ]
        ),
        "wip": values_by_week(
            [
                DateValue(item.date, item.value)
                for item in age_history
                if item.status == IN_PROGRESS_STATUS and item.value != 0
            ]
        ),
    }
