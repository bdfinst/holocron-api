"""Process team history data."""

from datetime import datetime, timezone

from app.crud.team_history import team_history_crud
from app.crud.teams import teams_crud
from app.database import generate_session
from app.models import Team, TeamHistory
from app.utils.time_utils import total_days_diff


def delete_outdated_team_history():
    """Delete outdated team history data."""
    with generate_session() as session:
        teams: list[Team] = teams_crud.get_entities(session)
        for team in teams:
            team_history: list[TeamHistory] = team_history_crud.get_entities_for_team(
                session, team.id
            )
            for history in team_history:
                days_diff = total_days_diff(
                    history.created_at, datetime.now(timezone.utc)
                )
                if days_diff >= 365:
                    team_history_crud.delete_entity(session, history.id)
