"""Process cumulative flow data.

Cumulative flow data is weekly data that contains backlog and wip keys.
One list entry for each ticket that was in the corresponding status that week.
The value of that entry -1 if that is not the last week of activity for
the ticket, otherwise the value is the age of the ticket (business days not counting
weekends).
"""

from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Dict, List, NamedTuple, Union

from app.models import StatusHistory, Ticket, TicketStatus

from .types import ChartData, DateValue
from .utils import (
    days_between_dates,
    get_monday_string,
    is_completed_ticket,
    is_epic_or_subtask_ticket,
    is_no_effort_ticket,
    total_days_diff_workflow,
)

# data structure that store the
# week distribution for the category (wip or backlog)
# where week is str in the format <year_number>_<week_number>
# and value is the age of the ticket in the given week.
WeekDistribution = Dict[str, Union[int, float]]
# data structure that stores the (wip, and backlog)
# as keys for dictionary, and the week distribution
# as value for a ticket (based on how many days
# the ticket was in progress or in backlog).
TicketCumFlowDistribution = Dict[str, WeekDistribution]


def get_hist_stat_at_date(
    date: datetime, latest_stat_hist4unique_weeks: List[StatusHistory]
) -> TicketStatus:
    """Return the status history of the ticket on a given date."""
    # binary search the status since the ticket status histories are
    # sorted, and return what the status would be
    # on the given date.
    low_idx, high_idx = 0, len(latest_stat_hist4unique_weeks) - 1
    while low_idx < high_idx:
        mid_idx = (low_idx + high_idx) // 2
        if date < latest_stat_hist4unique_weeks[mid_idx].date:
            high_idx = mid_idx - 1
        elif date > latest_stat_hist4unique_weeks[mid_idx].date:
            low_idx = mid_idx + 1
        else:
            break
    # after binary search is finished, we need to
    # find where it would be.
    closest_match, is_first_date, is_last_date = (
        latest_stat_hist4unique_weeks[low_idx],
        low_idx == 0,
        low_idx == len(latest_stat_hist4unique_weeks) - 1,
    )
    if closest_match.date > date and not is_first_date:
        before_closest_match = latest_stat_hist4unique_weeks[low_idx - 1]
        return before_closest_match.status
    if closest_match.date < date and not is_last_date:
        after_closest_match = latest_stat_hist4unique_weeks[low_idx + 1]
        return after_closest_match.status
    return closest_match.status


def get_uniq_weeks_latest_stat_hists(ticket: Ticket) -> List[StatusHistory]:
    """Return status history with activity based on latest date with unique weeks."""
    # example, if ticket.status_history contains
    # two dates that are both in the same week,
    # then the value for the week_to_max_stat_hist
    # will contain the history item containing the latest date
    uniq_week_stat_hist: Dict[str, StatusHistory] = OrderedDict()
    # skip done status
    hists_with_activity = iter(
        h for h in ticket.status_history if h.status != TicketStatus.DONE
    )
    for history in hists_with_activity:
        week = get_monday_string(history.date)
        uniq_week_stat_hist[week] = history
    return [history for _, history in uniq_week_stat_hist.items()]


def get_last_activity_date(ticket: Ticket) -> datetime:
    """Return the last activity of a ticket before done otherwise current date."""
    if not is_completed_ticket(ticket):
        return datetime.now()
    idx_of_last_activity_status = next(
        (
            i
            for i in range(len(ticket.status_history) - 1, -1, -1)
            if ticket.status_history[i].status != TicketStatus.DONE
        ),
    )
    return ticket.status_history[idx_of_last_activity_status].date


def get_ticket_cum_flow(ticket: Ticket) -> TicketCumFlowDistribution:
    """Return the cumulative flow distribution for a ticket."""

    def get_cum_flow_bucket(ticket_status: TicketStatus) -> str:
        """Return the bucket the value goes in given ticket status."""
        return "wip" if ticket_status == TicketStatus.IN_PROGRESS else "backlog"

    ticket_cum_flow: Dict[str, Dict[str, Union[int, float]]] = {
        "wip": {},
        "backlog": {},
    }
    first_activity_date, last_activity_date = (
        ticket.status_history[0].date,
        get_last_activity_date(ticket),
    )
    # first fill in the
    # status history buckets for
    # ticket_cum_flow based off of dates
    # that exist in status history.
    latest_stat_hist4unique_weeks = get_uniq_weeks_latest_stat_hists(ticket)
    for history in latest_stat_hist4unique_weeks:
        week = get_monday_string(history.date)
        bucket = get_cum_flow_bucket(history.status)
        ticket_cum_flow[bucket][week] = -1

    # then fill in the gaps with week
    # that are formed from status history
    curr_date = first_activity_date
    days_diff = total_days_diff_workflow(curr_date, last_activity_date)
    while days_diff >= 1:
        week = get_monday_string(curr_date)
        hist_status = get_hist_stat_at_date(curr_date, latest_stat_hist4unique_weeks)
        bucket = get_cum_flow_bucket(hist_status)
        # if the ticket bucket week value has not already been
        # set based on latest_stat_hist4unique_weeks, then set the week
        # data with the given bucket ("wip" or "backlog")
        if (
            week not in ticket_cum_flow["wip"]
            and week not in ticket_cum_flow["backlog"]
        ):
            ticket_cum_flow[bucket][week] = -1
        curr_date, days_diff = curr_date + timedelta(days=1), days_diff - 1
    # at this point we might have some days_diff > 0
    # but we do not care, since we only care about
    # which week it would be at given the last
    # activity date.
    last_week = get_monday_string(last_activity_date)
    last_week_status = get_hist_stat_at_date(
        last_activity_date, latest_stat_hist4unique_weeks
    )
    last_week_bucket = get_cum_flow_bucket(last_week_status)
    ticket_cum_flow[last_week_bucket][last_week] = days_between_dates(
        first_activity_date, last_activity_date
    )
    return ticket_cum_flow


class CumulativeFlowChartData(NamedTuple):
    """Type of chart data for cumulative flow."""

    backlog: ChartData
    wip: ChartData


def process_cumulative_flow(tickets: List[Ticket]) -> CumulativeFlowChartData:
    """Process tickets into cumulative flow data."""
    tickets_that_matter = iter(
        ticket
        for ticket in tickets
        if not is_epic_or_subtask_ticket(ticket) and not is_no_effort_ticket(ticket)
    )

    backlog_values: List[DateValue] = []
    wip_values: List[DateValue] = []
    for ticket in tickets_that_matter:
        ticket_cum_flow = get_ticket_cum_flow(ticket)
        wip_values.extend(
            DateValue(week, value) for week, value in ticket_cum_flow["wip"].items()
        )
        backlog_values.extend(
            DateValue(week, value) for week, value in ticket_cum_flow["backlog"].items()
        )

    result = CumulativeFlowChartData({}, {})
    for item in backlog_values:
        result.backlog.setdefault(item.date, []).append(item.value)
    for item in wip_values:
        result.wip.setdefault(item.date, []).append(item.value)
    return result
