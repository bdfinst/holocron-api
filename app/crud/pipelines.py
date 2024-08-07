"""BaseCRUD extension and instance for Pipeline model."""

from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import CollectorTargetType, Pipeline

from ._base import BaseCRUD
from .teams import teams_crud


class PipelinesCRUD(BaseCRUD[Pipeline]):
    """Base CRUD extension for Pipeline model."""

    def get_count(self, session: Session) -> int:
        """Override get_count to only count pipelines."""
        query = (
            # pylint: disable-next=E1102; false positive
            session.query(func.count())
            .select_from(Pipeline)
            .where(Pipeline.type == CollectorTargetType.BUILD)
        )
        return query.scalar()

    def get_count_for_team(self, session: Session, team_id: int) -> int:
        """Override get_count_for_team to only count pipelines."""
        team = teams_crud.get_entity(session, team_id)
        query = (
            session.query(
                # pylint: disable-next=E1102; false positive
                func.count()
            )
            .select_from(Pipeline)
            .where(Pipeline.team_id == team.id)
            .where(Pipeline.type == CollectorTargetType.BUILD)
        )

        return query.scalar()

    def get_entity(self, session: Session, id_: int) -> Pipeline:
        """Override get_entity to return only pipeline."""
        result = session.scalars(
            select(Pipeline)
            .where(Pipeline.type == CollectorTargetType.BUILD)
            .where(Pipeline.id == id_)
        ).first()
        if result is None:
            raise HolocronIntegrityError(
                f"{Pipeline.__name__} id", f"Invalid id: {id_}"
            )
        return result

    def get_entities(self, session: Session) -> Sequence[Pipeline]:
        """Override get_entities to return only pipelines."""
        return session.scalars(
            select(Pipeline).where(Pipeline.type == CollectorTargetType.BUILD)
        ).all()

    def get_entities_paginated(
        self, session: Session, offset=0, limit=100
    ) -> Sequence[Pipeline]:
        """Override get_entities_paginated to return only pipelines."""
        return session.scalars(
            select(Pipeline)
            .where(Pipeline.type == CollectorTargetType.BUILD)
            .offset(offset)
            .limit(limit)
        ).all()

    @staticmethod
    def get_entities_for_team(session: Session, team_id: int) -> Sequence[Pipeline]:
        """Get all pipelines for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(Pipeline)
            .where(Pipeline.team_id == team.id)
            .where(Pipeline.type == CollectorTargetType.BUILD)
        ).all()

    @staticmethod
    def get_entities_for_team_paginated(
        session: Session, team_id: int, offset=0, limit=100
    ) -> Sequence[Pipeline]:
        """Get paginated pipelines for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(Pipeline)
            .where(Pipeline.team_id == team.id)
            .where(Pipeline.type == CollectorTargetType.BUILD)
            .offset(offset)
            .limit(limit)
        ).all()


pipelines_crud = PipelinesCRUD(Pipeline)
