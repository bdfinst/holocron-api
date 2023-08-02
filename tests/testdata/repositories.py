"""Test data for repositories."""
from datetime import datetime

from app.models import Branch, Commit, GitRequest, Repository

commits = [
    Commit(
        collector_target_id=1,
        sha="1234",
        is_merged=True,
        date=datetime(year=2000, month=1, day=3),
        author_username="test",
    ),
    Commit(
        collector_target_id=1,
        sha="4321",
        is_merged=False,
        date=datetime(year=2000, month=1, day=3),
        author_username="test",
    ),
]

git_requests = [
    GitRequest(
        collector_target_id=1,
        title="test request",
        is_open=True,
        first_opened=datetime(year=2000, month=1, day=3),
        last_updated=datetime(year=2000, month=1, day=3),
        merged_at=None,
        url="https://test-mr/-/23",
    ),
]

branches = [
    Branch(
        collector_target_id=1,
        last_updated=datetime(year=2000, month=1, day=3),
        name="test-branch",
        url="https://test-repo/-/branch-my-branch",
        is_default=False,
    )
]


def create_repository(
    id=1,
    collector_id=1,
    type="SCM",
    name="test",
    url="https://test.com",
    commits=commits,
    git_requests=git_requests,
    branches=branches,
    trunk_branch="master",
    last_collected=datetime(2020, 7, 17).timestamp(),
    resource_id=1,
    team_id=None,
):
    """Create mock repository object with default values."""
    repository = Repository(
        collector_id=collector_id,
        type=type,
        name=name,
        url=url,
        commits=commits,
        git_requests=git_requests,
        branches=branches,
        trunk_branch=trunk_branch,
        last_collected=last_collected,
        resource_id=resource_id,
        team_id=team_id,
    )
    repository.id = id
    return repository


mock_repositories = [create_repository()]
mock_repositories_last_collected = [
    create_repository(
        commits=[],
        git_requests=[],
        branches=[],
        last_collected=datetime(2022, 3, 3).timestamp(),
    ),
    create_repository(
        commits=[],
        git_requests=[],
        branches=[],
        last_collected=datetime(2010, 3, 3).timestamp(),
    ),
    create_repository(
        commits=[],
        git_requests=[],
        branches=[],
        last_collected=datetime(1990, 3, 3).timestamp(),
    ),
]
