"""Test data for repositories."""
from datetime import datetime

from app.models import Branch, Commit, GitRequest, Repository

commits = [
    Commit(
        repository_id=1,
        sha="1234",
        is_merged=True,
        date=datetime(year=2000, month=1, day=3),
    ),
    Commit(
        repository_id=1,
        sha="4321",
        is_merged=False,
        date=datetime(year=2000, month=1, day=3),
    ),
]

git_requests = [
    GitRequest(
        repository_id=1,
        title="test request",
        is_open=True,
        last_updated=datetime(year=2000, month=1, day=3),
        url="https://test-mr/-/23",
    ),
]

branches = [
    Branch(
        repository_id=1,
        last_updated=datetime(year=2000, month=1, day=3),
        name="test-branch",
        url="https://test-repo/-/branch-my-branch",
    )
]

mock_repositories = [
    Repository(
        collector_id=1,
        url="https://test-repo.com",
        commits=commits,
        git_requests=git_requests,
        branches=branches,
        last_collected=datetime(2020, 7, 17).timestamp(),
    )
]
mock_repositories_last_collected = [
    Repository(
        collector_id=3,
        url="https://gitlab/1",
        commits=[],
        git_requests=[],
        branches=[],
        last_collected=datetime(2022, 3, 3).timestamp(),
    ),
    Repository(
        collector_id=3,
        url="https://gitlab/1",
        commits=[],
        git_requests=[],
        branches=[],
        last_collected=datetime(2010, 3, 3).timestamp(),
    ),
    Repository(
        collector_id=3,
        url="https://gitlab/1",
        commits=[],
        git_requests=[],
        branches=[],
        last_collected=datetime(1990, 3, 3).timestamp(),
    ),
]
