"""BaseCRUD extension and instance for Pipeline model."""
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import Pipeline

from ._base import BaseCRUD
from .teams import teams_crud


class PipelinesCRUD(BaseCRUD[Pipeline]):
    """Base CRUD extension for Pipeline model."""

    def get_entity(self, session, id_: int) -> Pipeline:
        """Override get_entity to return only pipeline."""
        result = session.scalars(
            select(Pipeline)
            .where(Pipeline.pipeline_id.is_not(None))
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
