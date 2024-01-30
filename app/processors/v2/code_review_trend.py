"""Process code review trend data.

Code Review trend is the weekly data that contains
'age_in_days_review_was_open' key which represents an array
of numbers where each item represents the GitRequest, and
the number for the item is the amount in days the
GitRequest was open from last_updated to merged_at.
"""

from typing import List

from app.models import GitRequest
from app.utils.time_utils import total_days_diff

from .types import ChartData, DateValue
from .utils import get_monday_string


def process_code_review_trend(
    git_requests: List[GitRequest],
) -> ChartData:
    """Process list of GitRequest into code review trend data."""
    merged_git_requests_trend_values = [
        DateValue(
            get_monday_string(gr.merged_at),
            total_days_diff(gr.first_opened, gr.merged_at),
        )
        for gr in git_requests
        if gr.merged_at is not None and gr.first_opened is not None
    ]

    result: ChartData = {}
    for item in merged_git_requests_trend_values:
        result.setdefault(item.date, []).append(item.value)
    return result
