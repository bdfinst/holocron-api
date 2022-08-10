"""Test data for teams."""
from app.models import Team

from .pipelines import mock_pipelines
from .repositories import mock_repositories
from .ticket_boards import mock_ticket_boards

mock_teams = [
    Team(
        name="mock_team",
        team_size=5,
        pipelines=mock_pipelines,
        repositories=mock_repositories,
        ticket_boards=mock_ticket_boards,
    )
]
