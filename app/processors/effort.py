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

from .utils import IN_PROGRESS, get_fmt_year_week

# hash table containing
# the week in the format <year_number>_<week_number> in string
# and the overall effort (int or float) as value for that week
WeekAndEffortTable = Dict[str, Union[int, float]]
# the key is the week in the format <year_number>_<week_number>
# in string, and the value is a list containing the
# effort/cost spent for each ticket.
WeekAndEffortTableForTickets = Dict[str, List[Union[int, float]]]


def days_between_dates(start: datetime, end: datetime) -> float:
    """Return the total number of days between two dates."""
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
    """Upsert a week entry for distirbution table (table)."""
    if week in table:  # we are still processing old
        # week data, so we accumulate effort spent
        table[week] += effort_spent
    else:  # we have received a new week data
        table[week] = effort_spent


def get_intrvl_effort_dist(
    in_prog_date: datetime, stop_prog_date: datetime, assignee_count: int
) -> WeekAndEffortTable:
    """Return effort distribution by week for two date intervals."""

    def calculate_effort(days_spent: float) -> float:
        """Return the effort days given days_spent and the number of assignees."""
        return days_spent * assignee_count

    intrvl_effort_dist: WeekAndEffortTable = {}
    days_effort = days_between_dates(in_prog_date, stop_prog_date)

    # handling the case that days spent are less than 1
    if days_effort < 1:
        year_week = get_fmt_year_week(in_prog_date)
        return {year_week: calculate_effort(days_effort)}

    # process effort spent during the day of progress.
    curr_date = in_prog_date.replace(hour=23, minute=59, second=59)
    intrvl_effort_dist[get_fmt_year_week(in_prog_date)] = days_between_dates(
        in_prog_date, curr_date
    )
    # recompute days difference from the end of the day since
    # we forwarded time by computing effort during the day of
    # progress.
    days_effort = days_between_dates(curr_date, stop_prog_date)
    # skip weekends, and calculate effort with hash of the week
    # as long as it is not a partial effort day remaining.
    while days_effort >= 1:
        curr_date, days_effort = curr_date + timedelta(days=1), days_effort - 1
        weekends_days = [5, 6]
        if curr_date.weekday() in weekends_days:
            continue
        # will create a new week entry if the day addition is
        # a new week and put effort in there, otherwise it will
        # stick with the old effort entry and sum the effort.
        year_week = get_fmt_year_week(curr_date)
        upsert_week_entry(year_week, calculate_effort(1), intrvl_effort_dist)

    # at this points days_effort should be less than 1
    # but we gotta take into account that someone could have
    # spent time working on the ticket during the day and
    # finished it during the day with effort < 1 day.
    if days_effort > 0:
        year_week_stop_date = get_fmt_year_week(stop_prog_date)
        upsert_week_entry(
            year_week_stop_date,
            calculate_effort(days_effort),
            intrvl_effort_dist,
        )
    return intrvl_effort_dist


def get_effort_distribution(ticket: Ticket) -> WeekAndEffortTable:
    """Return the distribution of effort for ticket."""
    assignee_count = 1  # the default value of assginees for now
    # must change when we figure out how many assignees are working on the ticket
    last_in_prog_date, last_status_was_in_prog = ticket.status_history[0], False
    effort_dist_for_ticket: WeekAndEffortTable = {}

    def accumulate_effort(intrvl_effort: WeekAndEffortTable):
        """Accumulate effort for week based on effort interval effort."""
        for week, effort_spent in intrvl_effort.items():
            # need to do this because we don't just update keys
            # we sum them for effort spent on ticket
            upsert_week_entry(week, effort_spent, effort_dist_for_ticket)

    for history in ticket.status_history:
        if history.status == IN_PROGRESS:
            last_in_prog_date = history.date
            last_status_was_in_prog = True
        elif last_status_was_in_prog:
            accumulate_effort(
                get_intrvl_effort_dist(last_in_prog_date, history.date, assignee_count)
            )
            last_status_was_in_prog = False

    if last_status_was_in_prog:
        accumulate_effort(
            get_intrvl_effort_dist(last_in_prog_date, datetime.now(), assignee_count)
        )
    return effort_dist_for_ticket


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
        # STILL HAVE TO DO COSTS
        accumulate_ticket_effort(effort_dist_for_ticket, chart_data_cost[effort_type])
    return {"hours": chart_data_hours, "costs": chart_data_hours}
