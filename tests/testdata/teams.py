"""Test data for teams."""
from app.models import Team

from .pipelines import mock_pipelines, mock_pipelines_last_collected
from .repositories import mock_repositories, mock_repositories_last_collected
from .ticket_boards import mock_ticket_boards, mock_ticket_boards_last_collected

mock_teams = [
    Team(
        name="mock_team",
        team_size=5,
        pipelines=mock_pipelines,
        repositories=mock_repositories,
        ticket_boards=mock_ticket_boards,
    )
]
mock_team_last_collected = Team(
    name="mock_team_lastCollected",
    team_size=1,
    pipelines=mock_pipelines_last_collected,
    ticket_boards=mock_ticket_boards_last_collected,
    repositories=mock_repositories_last_collected,
)
