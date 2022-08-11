"""Process effort data.

Effort data is weekly data with two versions for time and money.
Contains keys representing effort type: feature, defect, maintenance, and unplanned.
One list entry for each ticket that was in progress during that week.
Type of ticket determines type of effort.
Value for time is number of days the ticket was in progress that week.
Value for money is the time value multiplied by the assignee's pay rate.
"""
from collections import deque
from datetime import datetime, timedelta
from typing import Deque, Dict, List, Tuple

from app import config
from app.models import Ticket

from .types import ChartData, DateValue
from .utils import days_between_dates, values_by_week


def calculate_effort(days_spent: float, assignee_count: int) -> float:
    """Return the effort days given days_spent and the number of assignees."""
    return days_spent * assignee_count


def process_ticket(ticket: Ticket) -> List[DateValue]:
    """Return the list of effort spent on each date the ticket was in progress."""
    default_assignee_count = 1
    last_in_prog_date, last_status_was_in_prog = ticket.status_history[0], False
    date_queue: Deque[DateValue] = deque([])

    for history in ticket.status_history:
        if history.status == "In Progress":
            last_in_prog_date = history.date
            last_status_was_in_prog = True
        elif last_status_was_in_prog:
            days_spent = days_between_dates(last_in_prog_date, history.date)
            date_queue.append(
                DateValue(
                    last_in_prog_date,
                    calculate_effort(days_spent, default_assignee_count),
                )
            )
            last_status_was_in_prog = False

    if last_status_was_in_prog:
        effort = calculate_effort(
            days_between_dates(last_in_prog_date, datetime.now()),
            default_assignee_count,
        )
        date_queue.append(DateValue(last_in_prog_date, effort))

    return list(date_queue)


def get_partial_day(date: datetime) -> float:
    """Calculate the partial day amount."""
    seconds_in_minute = 60
    seconds_in_hour = 60 * seconds_in_minute
    seconds_in_day = 24 * seconds_in_hour

    seconds_in_date = date.hour * seconds_in_hour + date.minute * seconds_in_minute
    time_passed_ratio = seconds_in_date / seconds_in_day

    return round(time_passed_ratio * 10) / 10 or 1.0


def get_days_until(day_of_week: str, date: datetime) -> Tuple[datetime, int]:
    """Get the date and number of days until the next given weekday."""
    days_of_week_values = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    business_day_value = days_of_week_values[day_of_week.lower()]
    calendar_day_value = business_day_value

    current_day_value = date.weekday()
    if business_day_value < current_day_value:
        business_days_per_week = 5
        calendar_days_per_week = 7
        business_day_value += business_days_per_week
        calendar_day_value += calendar_days_per_week

    business_days_until = business_day_value - current_day_value
    calendar_days_until = calendar_day_value - current_day_value
    return (date + timedelta(days=calendar_days_until), business_days_until)


def spread_effort(total_effort: DateValue) -> List[DateValue]:
    """Spread effort into weeks of DateValue."""
    effort = []

    current_value = total_effort.value
    current_date = total_effort.date
    days_effort = get_partial_day(current_date)

    while current_value > 0:
        friday, days_difference = get_days_until("friday", current_date)
        days_effort = min(current_value, days_effort + days_difference)

        effort.append(DateValue(friday, days_effort))
        current_value -= days_effort
        days_diff_after_first_run = 1
        days_effort = days_diff_after_first_run
        current_date = get_days_until("monday", friday)[0]

    return effort


def process_effort(tickets: List[Ticket]) -> Dict[str, ChartData]:
    """Process tickets into effort data."""
    chart_data_hours: Dict[str, List[DateValue]] = {
        key: [] for key in config.JIRA_TICKET_TYPE_BUCKETS
    }
    chart_data_cost = chart_data_hours.copy()

    for ticket in tickets:
        ticket_type = next(
            (
                key
                for key, value in config.JIRA_TICKET_TYPE_BUCKETS.items()
                if ticket.ticket_type in value
            ),
            "feature",
        )

        total_effort = process_ticket(ticket)
        effort = []

        for entry in total_effort:
            effort += spread_effort(entry)
        chart_data_hours[ticket_type] += effort
    return {
        "hours": {
            key: values_by_week(value) for key, value in chart_data_hours.items()
        },
        "costs": {key: values_by_week(value) for key, value in chart_data_cost.items()},
    }
