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
from typing import Deque, Dict, List, Tuple, Union

from app import config
from app.models import Ticket

from .types import ChartData, DateValue
from .utils import IN_PROGRESS

# contains the weeks as str in the format <year_number>_<week_number>
# as keys, and value as a number indicating the effort spent that week.
WeeksDataForTicket = Dict[str, Union[int, float]]

def calculate_effort(days_spent: float, assignee_count: int) -> float:
    """Return the effort days given days_spent and the number of assignees."""
    return days_spent * assignee_count

def calculate_week_data_for_ticket(in_progress_date: datetime, current_date: datetime, assignee_count: int) -> WeeksDataForTicket:
    """Return the WeeksDataForTicket given an in progress date, and current date."""
    # FIRST CASE: days <= 5
    # in which case the effort is going to be
    # just days difference * assignee count.
    # SECOND CASE: days > 5
    


def process_ticket(ticket: Ticket) -> WeeksDataForTicket:
    """Return the list of effort spent on each date the ticket was in progress."""
    assignee_count = 1 # the default value of assginees for now
    # must change when we figure out how many assignees are working on the ticket
    last_in_prog_date, last_status_was_in_prog = ticket.status_history[0], False
    chart_data: ChartData = {} # dictionary containig
    # the week number in the format <year_number>_<week_number>
    # as keys, and number as value.
    for history in ticket.status_history:
        if history.status == IN_PROGRESS:
            last_in_prog_date = history.date
            last_status_was_in_prog = True
        elif last_status_was_in_prog:

            last_status_was_in_prog = False
    return chart_data



def process_effort(tickets: List[Ticket]) -> Dict[str, ChartData]:
    """Process tickets into effort data."""
    for ticket in tickets:
        effort_type = next(
            (
                key
                for key, value in config.JIRA_TICKET_TYPE_BUCKETS.items()
                if ticket.ticket_type in value
            ),
            "feature",
        )