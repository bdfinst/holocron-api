"""Test data for projects."""
from datetime import datetime

from app.models import Project, ProjectIssue, ProjectIssueSeverity, ProjectIssueType

issues = [
    ProjectIssue(
        resource_id="1",
        package="test",
        collector_target_id=1,
        severity=ProjectIssueSeverity.LOW,
        type=ProjectIssueType.MAINTAINABILITY,
        issue_url="test.com/1",
        created_date=datetime(2020, 1, 1),
        closed_date=datetime(2020, 2, 1),
    ),
    ProjectIssue(
        resource_id="2",
        package="test",
        collector_target_id=1,
        severity=ProjectIssueSeverity.MEDIUM,
        type=ProjectIssueType.MAINTAINABILITY,
        issue_url="test.com/2",
        created_date=datetime(2020, 2, 1),
        closed_date=None,
    ),
    ProjectIssue(
        resource_id="3",
        package="test",
        collector_target_id=1,
        severity=ProjectIssueSeverity.LOW,
        type=ProjectIssueType.VULNERABILITY,
        issue_url="test.com/3",
        created_date=datetime(2020, 1, 1),
        closed_date=None,
    ),
]


def create_project(
    id=1,
    collector_id=1,
    name="mock_project",
    url="https://test.com",
    issues=issues,
    last_collected=datetime(2020, 8, 17).timestamp(),
    resource_id=1,
    type="project_analysis",
    team_id=None,
):
    """Create mock project object with default values."""
    project = Project(
        collector_id=collector_id,
        name=name,
        url=url,
        issues=issues,
        last_collected=last_collected,
        resource_id=resource_id,
        type=type,
        team_id=team_id,
    )
    project.id = id
    return project


mock_projects = [create_project()]
mock_projects_last_collected = [
    create_project(issues=[], last_collected=datetime(2022, 3, 3).timestamp()),
    create_project(issues=[], last_collected=datetime(2010, 3, 3).timestamp()),
    create_project(issues=[], last_collected=datetime(1990, 3, 3).timestamp()),
]
