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
from .utils import values_by_week


def to_code_review_trend_date_value(git_request: GitRequest) -> DateValue:
    """Get the DateValue for a git_request's merged_at."""
    return DateValue(
        git_request.merged_at,
        total_days_diff(git_request.first_opened, git_request.merged_at),
    )


def process_code_review_trend(git_requests: List[GitRequest]) -> ChartData:
    """Process list of GitRequest into code review trend data."""
    merged_git_requests_trend_values = [
        to_code_review_trend_date_value(git_request)
        for git_request in git_requests
        if git_request.merged_at is not None and git_request.first_opened is not None
    ]
    code_review_trend_data: ChartData = {
        "age_in_days_review_was_open": values_by_week(merged_git_requests_trend_values),
    }
    return code_review_trend_data
