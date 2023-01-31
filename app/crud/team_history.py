"""BaseCRUD extension and instance for Team History model."""
import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import Team, TeamHistory

from ._base import BaseCRUD


class TeamHistoryCRUD(BaseCRUD[TeamHistory]):
    """Base CRUD extention for TeamHistory Model."""

    @staticmethod
    def create_entity(session: Session, team: Team) -> TeamHistory:
        """Insert team history in database."""
        new_team_history = TeamHistory(
            team_size=team.team_size,
            team_id=team.id,
        )
        try:
            session.add(new_team_history)
            session.commit()
            session.refresh(new_team_history)
        except IntegrityError as err:
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError("team_id", "not found") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        return new_team_history

    @staticmethod
    def get_entities_for_team(session: Session, team_id: int) -> Sequence[TeamHistory]:
        """Get all team history given an team id."""
        return session.scalars(
            select(TeamHistory).where(TeamHistory.team_id == team_id)
        ).all()


team_history_crud = TeamHistoryCRUD(TeamHistory)
