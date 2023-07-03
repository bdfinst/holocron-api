"""Test data for teams."""
from app.models import Team

from .pipelines import mock_pipelines, mock_pipelines_last_collected
from .projects import mock_projects, mock_projects_last_collected
from .repositories import mock_repositories, mock_repositories_last_collected
from .ticket_boards import mock_ticket_boards, mock_ticket_boards_last_collected
from .users import mock_users


def create_team(
    id=1,
    name="mock team",
    team_size=5,
    pipelines=mock_pipelines,
    projects=mock_projects,
    repositories=mock_repositories,
    ticket_boards=mock_ticket_boards,
    users=mock_users,
    valuestream_id=1,
    is_workflow_only=False,
    view_owner_id=None,
):
    """Create mock team object with default values."""
    collector_targets = pipelines + repositories + ticket_boards
    team = Team(
        name=name,
        team_size=team_size,
        pipelines=pipelines,
        projects=projects,
        repositories=repositories,
        ticket_boards=ticket_boards,
        users=users,
        valuestream_id=valuestream_id,
        is_workflow_only=is_workflow_only,
        collector_targets=collector_targets,
        view_owner_id=view_owner_id,
    )
    team.id = id
    return team


def create_team_view(
    id=2,
    name="mock team view",
    team_size=5,
    pipelines=mock_pipelines,
    projects=mock_projects,
    repositories=mock_repositories,
    ticket_boards=mock_ticket_boards,
    users=mock_users,
    valuestream_id=1,
    is_workflow_only=False,
    view_owner_id=1,
):
    """Create mock team object with default values."""
    collector_targets = pipelines + repositories + ticket_boards
    team = Team(
        name=name,
        team_size=team_size,
        pipelines=pipelines,
        projects=projects,
        repositories=repositories,
        ticket_boards=ticket_boards,
        users=users,
        valuestream_id=valuestream_id,
        is_workflow_only=is_workflow_only,
        collector_targets=collector_targets,
        view_owner_id=view_owner_id,
    )
    team.id = id
    return team


mock_teams = [create_team()]
mock_team_last_collected = create_team(
    pipelines=mock_pipelines_last_collected,
    ticket_boards=mock_ticket_boards_last_collected,
    repositories=mock_repositories_last_collected,
    projects=mock_projects_last_collected,
)
