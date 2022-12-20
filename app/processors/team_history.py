"""Process team history data."""

from datetime import datetime, timezone
from typing import List

from app.crud.team_history import team_history_crud
from app.crud.teams import teams_crud
from app.database import generate_session
from app.models import Team, TeamHistory
from app.utils.time_utils import total_days_diff

from .types import ChartData, DateValue
from .utils import values_by_week


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


def process_team_size(team_history: TeamHistory) -> DateValue:
    """Get the DateValue for a team size."""
    return DateValue(team_history.created_at, team_history.team_size)


def process_team_size_histories(team_size_histories: List[TeamHistory]) -> ChartData:
    """Process team size into weekly data."""
    return {
        "team_size": values_by_week(
            [process_team_size(team_size) for team_size in team_size_histories]
        )
    }
