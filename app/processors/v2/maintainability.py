"""Process maintainability data.

Maintainability score is weekly data represented by the maintainability_score key.
One list entry for each issue that was active during the week.
The value is a mapping based on issue severity.
"""
from datetime import datetime, timedelta
from typing import List

from app.models import ProjectIssue, ProjectIssueSeverity, ProjectIssueType
from app.processors.v1.utils import flat_map

from .types import ChartData, DateValue
from .utils import get_monday, values_by_week

SEVERITY_SCORE_MAPPING = {
    ProjectIssueSeverity.LOW: 1,
    ProjectIssueSeverity.MEDIUM: 3,
    ProjectIssueSeverity.HIGH: 10,
}


def get_active_issue_date_values(issue: ProjectIssue) -> List[DateValue]:
    """Split issue into list of DateValues for each week an issue was active."""
    dates: List[DateValue] = []
    end_date = (
        issue.closed_date
        if issue.closed_date is not None
        else get_monday(datetime.now() + timedelta(days=7))
    )
    date_to_check = get_monday(issue.created_date) + timedelta(days=7)
    while date_to_check <= end_date and date_to_check < datetime.now():
        dates.append(DateValue(date_to_check, SEVERITY_SCORE_MAPPING[issue.severity]))
        date_to_check += timedelta(days=7)
    return dates


def is_maintenance_issue(issue: ProjectIssue) -> bool:
    """Filter issues based on type."""
    return issue.type == ProjectIssueType.MAINTAINABILITY


def process_maintainability_score(issues: List[ProjectIssue]) -> ChartData:
    """Process issues into maintainability score data."""
    maintenance_issues = [issue for issue in issues if is_maintenance_issue(issue)]
    return {
        "maintainability_score": values_by_week(
            flat_map(maintenance_issues, get_active_issue_date_values)
        )
    }
