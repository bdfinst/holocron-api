"""Test process_maintainability_score."""
from datetime import datetime

from app.models import ProjectIssue, ProjectIssueSeverity, ProjectIssueType
from app.processors.v2 import maintainability
from app.processors.v2.maintainability import process_maintainability_score
from tests.testdata import issues


class MockDatetime:
    """Mock Datetime class."""

    def now(self):
        """Mock now method."""
        return datetime(2020, 2, 1)


def test_process_maintainability_score(monkeypatch):
    """Test process_maintainability_score function."""
    monkeypatch.setattr(maintainability, "datetime", MockDatetime())
    cases = [
        (
            """Should calculate maintainability score.""",
            [
                ProjectIssue(
                    resource_id="1",
                    package="test",
                    collector_target_id=1,
                    severity=ProjectIssueSeverity.LOW,
                    type=ProjectIssueType.MAINTAINABILITY,
                    issue_url="test.com/1",
                    created_date=datetime(2020, 1, 1),
                    closed_date=datetime(2020, 1, 21),
                ),
                ProjectIssue(
                    resource_id="2",
                    package="test",
                    collector_target_id=1,
                    severity=ProjectIssueSeverity.MEDIUM,
                    type=ProjectIssueType.MAINTAINABILITY,
                    issue_url="test.com/2",
                    created_date=datetime(2020, 1, 15),
                    closed_date=None,
                ),
                # should not count this issue as it is not maintainability
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
            ],
            {
                "2020-01-06": [1],
                "2020-01-13": [1],
                "2020-01-20": [1, 3],
                "2020-01-27": [3],
            },
        )
    ]

    for case in cases:
        _, case_input, expected = case
        actual = process_maintainability_score(case_input)
        assert expected == actual
