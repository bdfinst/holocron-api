"""Base classes for metric-based database operations."""

from typing import Sequence, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import CollectorTarget, ModelBase

from ._base import BaseCRUD
from .teams import teams_crud

T = TypeVar("T", bound=ModelBase)


class BaseMetricCRUD(BaseCRUD[T]):
    """Extended base class for CRUD methods on team metric models."""

    def __init__(self, model: Type[T], target_model: Type[CollectorTarget]):
        """Initialize with the given model with collector target parent."""
        self.target_model = target_model
        super().__init__(model)

    def get_count_for_team(self, session: Session, team_id: int) -> int:
        """Get row count for a given team."""
        team = teams_crud.get_entity(session, team_id)
        query = (
            session.query(
                # pylint: disable-next=E1102; false positive
                func.count()
            )
            .select_from(self.model)
            .join(
                self.target_model,
                getattr(self.model, "collector_target_id") == self.target_model.id,
            )
            .where(self.target_model.team_id == team.id)
        )

        return query.scalar()

    def get_entities_for_team(self, session: Session, team_id: int) -> Sequence[T]:
        """Get all entities for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(self.model)
            .join(
                self.target_model,
                getattr(self.model, "collector_target_id") == self.target_model.id,
            )
            .where(self.target_model.team_id == team.id)
        ).all()

    def get_entities_for_team_paginated(
        self,
        session: Session,
        team_id: int,
        offset=0,
        limit=100,
    ) -> Sequence[T]:
        """Get paginated entities for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(self.model)
            .join(
                self.target_model,
                getattr(self.model, "collector_target_id") == self.target_model.id,
            )
            .where(self.target_model.team_id == team.id)
            .offset(offset)
            .limit(limit)
        ).all()
