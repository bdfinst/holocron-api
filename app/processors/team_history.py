"""Process team history data."""

from datetime import datetime, timezone
from typing import Sequence

from app.crud.team_history import team_history_crud
from app.crud.teams import teams_crud
from app.database import generate_session
from app.models import TeamHistory
from app.utils.time_utils import total_days_diff

from .types import ChartData, DateValue
from .utils import values_by_week


def delete_outdated_team_history() -> None:
    """Delete outdated team history data."""
    with generate_session() as session:
        teams = teams_crud.get_entities(session)
        for team in teams:
            team_history = team_history_crud.get_entities_for_team(session, team.id)
            for history in team_history:
                days_diff = total_days_diff(
                    history.created_at, datetime.now(timezone.utc)
                )
                if days_diff >= 365:
                    team_history_crud.delete_entity(session, history.id)


def process_team_size(team_history: TeamHistory) -> DateValue:
    """Get the DateValue for a team size."""
    return DateValue(team_history.created_at, team_history.team_size)


def process_team_history(team_history: Sequence[TeamHistory]) -> ChartData:
    """Process team size into weekly data."""
    return {
        "team_size": values_by_week([process_team_size(hist) for hist in team_history])
    }
