"""BaseCRUD extension and instance for Pipeline model."""
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Pipeline

from ._base import BaseCRUD
from .teams import teams_crud


class PipelinesCRUD(BaseCRUD[Pipeline]):
    """Base CRUD extension for Pipeline model."""

    def get_entities(self, session: Session) -> Sequence[Pipeline]:
        """Override get_entities to return only pipelines."""
        return session.scalars(
            select(Pipeline).where(Pipeline.pipeline_id.is_not(None))
        ).all()

    @staticmethod
    def get_entities_for_team(session: Session, team_id: int) -> Sequence[Pipeline]:
        """Get all pipelines for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(Pipeline)
            .where(Pipeline.team_id == team.id)
            .where(Pipeline.pipeline_id.is_not(None))
        ).all()


pipelines_crud = PipelinesCRUD(Pipeline)
