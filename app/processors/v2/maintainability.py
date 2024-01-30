"""Process maintainability data.

The amount of maintainability issues is weekly data represented by
maintainability_issues key.
There are also keys for severity of maintainability issues such as 
maintainability_high_severity_issues,
maintainability_medium_severity_issues,
maintainability_low_severity_issues
which should total to the number of maintainability issues
in the week which is the maintainability_issues key.
"""

from typing import Dict, List, Tuple

from app.models import ProjectIssue, ProjectIssueSeverity, ProjectIssueType

from .types import ChartData
from .utils import get_issues_historical_data_stream


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
