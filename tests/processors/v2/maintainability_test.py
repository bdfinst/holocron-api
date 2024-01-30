"""Test process_maintainability_data."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

from app.models import ProjectIssue, ProjectIssueSeverity, ProjectIssueType
from app.processors.v2 import utils
from app.processors.v2.maintainability import process_maintainability_data


def test_process_maintainability_data(monkeypatch):
    """Test process_maintainability_data function."""
    monkeypatch.setattr(
        utils,
        "datetime",
        MagicMock(
            now=lambda *_, **__: datetime(2020, 2, 1).replace(tzinfo=timezone.utc)
        ),
    )
    cases = [
        (
            """Should calculate maintainability issues.""",
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
                ProjectIssue(
                    resource_id="4",
                    package="test",
                    collector_target_id=1,
                    severity=ProjectIssueSeverity.HIGH,
                    type=ProjectIssueType.MAINTAINABILITY,
                    issue_url="test.com/4",
                    created_date=datetime(2020, 1, 1),
                    closed_date=datetime(2020, 1, 21),
                ),
            ],
            (
                {  # all issues date map
                    "2020-01-06": [1, 1],
                    "2020-01-13": [1, 1],
                    "2020-01-20": [1, 1, 1],
                    "2020-01-27": [1],
                },
                {  # low severity issues date map
                    "2020-01-06": [1],
                    "2020-01-13": [1],
                    "2020-01-20": [1],
                },
                {  # medium severity issues date map
                    "2020-01-20": [1],
                    "2020-01-27": [1],
                },
                {  # high severity issues date map
                    "2020-01-06": [1],
                    "2020-01-13": [1],
                    "2020-01-20": [1],
                },
            ),
        )
    ]

    for case in cases:
        _, case_input, expected = case
        actual = process_maintainability_data(case_input)
        assert expected == actual
