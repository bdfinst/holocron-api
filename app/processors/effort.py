"""Process effort data.

Effort data is weekly data with two versions for time and money.
Contains keys representing effort type: feature, defect, maintenance, and unplanned.
One list entry for each ticket that was in progress during that week.
Type of ticket determines type of effort.
Value for time is number of days the ticket was in progress that week.
Value for money is the time value multiplied by the assignee's pay rate.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Union

from app import config
from app.models import Ticket

from .utils import IN_PROGRESS

# hash table containing
# the week in the format <year_number>_<week_number> in string
# and the overall effort (int or float) as value for that week
WeekAndEffortTable = Dict[str, Union[int, float]]
# the key is the week in the format <year_number>_<week_number>
# in string, and the value is a list containing the
# effort spent for each ticket.
WeekAndEffortTableForTickets = Dict[str, List[Union[int, float]]]


def get_fmt_year_week(date: datetime) -> str:
    """Return the formatted <year_number>_<week_number> of date."""
    iso_date = date.isocalendar()
    week_str = f"{iso_date.week}" if iso_date.week >= 10 else f"0{iso_date.week}"
    return f"{iso_date.year}_{week_str}"


def days_between_dates(start: datetime, end: datetime) -> float:
    """Return the number of days between two dates."""
    hours_per_day = 24
    seconds_per_day = 60 * 60 * hours_per_day
    time_delta = end - start
    actual_days_effort = time_delta.days + time_delta.seconds / seconds_per_day

    if actual_days_effort * hours_per_day < config.MIN_EXPECTED_CYCLE_TIME_HOURS:
        return 0
    precision_factor = 10
    return round(actual_days_effort * precision_factor) / precision_factor


def upsert_week_entry(
    week: str, effort_spent: Union[float, int], table: WeekAndEffortTable
):
    """Create a week effort if week not found otherwise sum with effort."""
    if week in table:  # we are still processing old
        # week data
        table[week] += effort_spent
    else:  # we have received a new week data
        table[week] = effort_spent


def get_intrvl_effort(
    in_prog_date: datetime, stop_prog_date: datetime, assignee_count: int
) -> WeekAndEffortTable:
    """Return the table containg effort data for two date interval."""
    week_effort_hash_table: WeekAndEffortTable = {}
    days_effort = days_between_dates(in_prog_date, stop_prog_date)

    def calculate_effort(days_spent: float, assignee_count: int) -> float:
        """Return the effort days given days_spent and the number of assignees."""
        return days_spent * assignee_count

    # handling the case that days spent are less than 1
    if days_effort < 1:
        year_week = get_fmt_year_week(in_prog_date)
        return {year_week: calculate_effort(days_effort, assignee_count)}

    # process effort spent during the day of progress.
    curr_date = in_prog_date.replace(hour=23, minute=59, second=59)
    week_effort_hash_table[get_fmt_year_week(in_prog_date)] = days_between_dates(
        in_prog_date, curr_date
    )
    weekends_days = [5, 6]
    # recompute days difference from the end of the day since
    # we forwarded time by computing effort during the day of
    # progress.
    days_effort = days_between_dates(curr_date, stop_prog_date)
    # skip weekdays, and calculate effort with hash of the week
    while days_effort > 0:
        curr_date += timedelta(days=1)
        days_effort -= 1
        year_week = get_fmt_year_week(curr_date)
        if curr_date.weekday() in weekends_days:
            continue
        # will create a new week entry if the day addition is
        # a new week and put effort in there, otherwise it will
        # stick with the old effort entry and sum the effort.
        upsert_week_entry(
            year_week, calculate_effort(1, assignee_count), week_effort_hash_table
        )

    # at this points days_effort should be less than 0
    # but we gotta take into account that someone could have
    # spent time working on the ticket during the day and
    # finished it during the day with effort < 1 day (hence abs value).
    days_effort = abs(days_effort)
    year_week_stop_date = get_fmt_year_week(stop_prog_date)
    upsert_week_entry(
        year_week_stop_date,
        calculate_effort(days_effort, assignee_count),
        week_effort_hash_table,
    )
    return week_effort_hash_table


def get_effort_distribution(ticket: Ticket) -> WeekAndEffortTable:
    """Return the list of effort spent on each date the ticket was in progress."""
    assignee_count = 1  # the default value of assginees for now
    # must change when we figure out how many assignees are working on the ticket
    last_in_prog_date, last_status_was_in_prog = ticket.status_history[0], False
    week_and_effort_table: WeekAndEffortTable = {}

    def accumulate_effort(intrvl_effort: WeekAndEffortTable):
        """Accumulate effort for week based on effort interval effort."""
        for week, effort_spent in intrvl_effort.items():
            # need to do this because we don't just update keys
            # we sum them for effort spent on ticket
            upsert_week_entry(week, effort_spent, week_and_effort_table)

    for history in ticket.status_history:
        if history.status == IN_PROGRESS:
            last_in_prog_date = history.date
            last_status_was_in_prog = True
        elif last_status_was_in_prog:
            accumulate_effort(
                get_intrvl_effort(last_in_prog_date, history.date, assignee_count)
            )
            last_status_was_in_prog = False

    if last_status_was_in_prog:
        accumulate_effort(
            get_intrvl_effort(last_in_prog_date, datetime.now(), assignee_count)
        )
    return week_and_effort_table


def process_effort(
    tickets: List[Ticket],
) -> Dict[str, Dict[str, WeekAndEffortTableForTickets]]:
    """Process tickets into effort data."""
    chart_data_hours: Dict[str, WeekAndEffortTableForTickets] = {
        key: {} for key in config.JIRA_TICKET_TYPE_BUCKETS
    }
    chart_data_cost: Dict[str, WeekAndEffortTableForTickets] = {
        key: {} for key in config.JIRA_TICKET_TYPE_BUCKETS
    }

    def accumulate_ticket_effort(dist: WeekAndEffortTable, table: WeekAndEffortTable):
        """Accumulate ticket effort for each week."""
        for week, effort_spent in dist.items():
            if week in table:
                table[week].append(effort_spent)
            else:
                table[week] = [effort_spent]

    for ticket in tickets:
        effort_type = next(
            (
                key
                for key, value in config.JIRA_TICKET_TYPE_BUCKETS.items()
                if ticket.ticket_type in value
            ),
            "feature",
        )
        effort_dist_for_ticket = get_effort_distribution(ticket)
        accumulate_ticket_effort(effort_dist_for_ticket, chart_data_hours[effort_type])
        accumulate_ticket_effort(effort_dist_for_ticket, chart_data_cost[effort_type])
    return {"hours": chart_data_hours, "costs": chart_data_hours}
