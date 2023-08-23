"""Process maintainability data.

Maintainability score is weekly data represented by the maintainability_score key.
One list entry for each issue that was active during the week.
The value is a mapping based on issue severity.
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterator, List, Tuple

from app.models import ProjectIssue, ProjectIssueSeverity, ProjectIssueType

from .types import ChartData
from .utils import get_monday, get_monday_string


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


def process_maintainability_data(
    issues: List[ProjectIssue],
) -> Tuple[ChartData, ChartData, ChartData, ChartData]:
    """Process issues that relate to maintainability."""
    issues_chart_data: ChartData = {}
    issues_severity_chart_data: Dict[ProjectIssueSeverity, ChartData] = {
        ProjectIssueSeverity.HIGH: {},
        ProjectIssueSeverity.MEDIUM: {},
        ProjectIssueSeverity.LOW: {},
    }
    historical_data_stream = get_issues_historical_data_stream(
        issue for issue in issues if issue.type == ProjectIssueType.MAINTAINABILITY
    )
    for historical_data in historical_data_stream:
        monday_string, severity = historical_data
        issues_chart_data.setdefault(monday_string, []).append(1)
        issues_severity_chart_data[severity].setdefault(monday_string, []).append(1)

    return (
        issues_chart_data,
        issues_severity_chart_data[ProjectIssueSeverity.HIGH],
        issues_severity_chart_data[ProjectIssueSeverity.MEDIUM],
        issues_severity_chart_data[ProjectIssueSeverity.LOW],
    )
