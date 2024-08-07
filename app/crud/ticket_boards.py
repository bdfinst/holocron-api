"""BaseCRUD extension and instance for TicketBoard model."""

from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import CollectorTargetType, TicketBoard

from ._base import BaseCRUD
from .teams import teams_crud


class TicketBoardsCRUD(BaseCRUD[TicketBoard]):
    """Base CRUD extension for TicketBoard model."""

    def get_count(self, session: Session) -> int:
        """Override get_count to only count ticket boards."""
        query = (
            # pylint: disable-next=E1102; false positive
            session.query(func.count())
            .select_from(TicketBoard)
            .where(TicketBoard.type == CollectorTargetType.WORKFLOW)
        )
        return query.scalar()

    def get_count_for_team(self, session: Session, team_id: int) -> int:
        """Override get_count_for_team to only count ticket boards."""
        team = teams_crud.get_entity(session, team_id)
        query = (
            session.query(
                # pylint: disable-next=E1102; false positive
                func.count()
            )
            .select_from(TicketBoard)
            .where(TicketBoard.team_id == team.id)
            .where(TicketBoard.type == CollectorTargetType.WORKFLOW)
        )

        return query.scalar()

    def get_entity(self, session: Session, id_: int) -> TicketBoard:
        """Override get_entity to return only ticket board."""
        result = session.scalars(
            select(TicketBoard)
            .where(TicketBoard.type == CollectorTargetType.WORKFLOW)
            .where(TicketBoard.id == id_)
        ).first()
        if result is None:
            raise HolocronIntegrityError(
                f"{TicketBoard.__name__} id", f"Invalid id: {id_}"
            )
        return result

    def get_entities(self, session: Session) -> Sequence[TicketBoard]:
        """Override get_entities to return only ticket boards."""
        return session.scalars(
            select(TicketBoard).where(TicketBoard.type == CollectorTargetType.WORKFLOW)
        ).all()

    def get_entities_paginated(
        self, session: Session, offset=0, limit=100
    ) -> Sequence[TicketBoard]:
        """Override get_entities_paginated to return only ticket boards."""
        return session.scalars(
            select(TicketBoard)
            .where(TicketBoard.type == CollectorTargetType.WORKFLOW)
            .offset(offset)
            .limit(limit)
        ).all()

    @staticmethod
    def get_entities_for_team(session: Session, team_id: int) -> Sequence[TicketBoard]:
        """Get all ticket boards for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(TicketBoard)
            .where(TicketBoard.team_id == team.id)
            .where(TicketBoard.type == CollectorTargetType.WORKFLOW)
        ).all()

    @staticmethod
    def get_entities_for_team_paginated(
        session: Session, team_id: int, offset=0, limit=100
    ) -> Sequence[TicketBoard]:
        """Get paginated ticket boards for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(TicketBoard)
            .where(TicketBoard.team_id == team.id)
            .where(TicketBoard.type == CollectorTargetType.WORKFLOW)
            .offset(offset)
            .limit(limit)
        ).all()


ticket_boards_crud = TicketBoardsCRUD(TicketBoard)
