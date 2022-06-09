"""BaseCRUD extension and instance for TicketBoard model."""
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import TicketBoard

from ._base import BaseCRUD


class TicketBoardsCRUD(BaseCRUD[TicketBoard]):
    """Base CRUD extension for TicketBoard model."""

    def get_entities(self, session: Session) -> List[TicketBoard]:
        """Override get_entities to return only ticket boards."""
        return session.scalars(
            select(TicketBoard).where(TicketBoard.board_id.is_not(None))
        ).all()

    @staticmethod
    def get_entities_for_team(session: Session, team_id: int) -> List[TicketBoard]:
        """Get all ticket boards for a given team."""
        return session.scalars(
            select(TicketBoard)
            .where(TicketBoard.team_id == team_id)
            .where(TicketBoard.board_id.is_not(None))
        ).all()


ticket_boards_crud = TicketBoardsCRUD(TicketBoard)
