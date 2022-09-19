"""Base classes for metric-based database operations."""
from typing import List, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CollectorTarget, ModelBase

from ._base import BaseCRUD
from .teams import teams_crud

T = TypeVar("T", bound=ModelBase)


class BaseMetricCRUD(BaseCRUD[T]):
    """Extended base class for CRUD methods on team metric models."""

    def __init__(
        self,
        model: Type[ModelBase],
        target_model: Type[CollectorTarget],
        model_foreign_key_field_to_target: str,
    ):
        """Initialize with the given model with collector target parent."""
        if not hasattr(model, model_foreign_key_field_to_target):
            raise TypeError(
                f"{model} has no attribute {model_foreign_key_field_to_target}"
            )
        self.target_model = target_model
        self.fk_id_field = model_foreign_key_field_to_target
        super().__init__(model)

    def get_entities_for_team(self, session: Session, team_id: int) -> List[T]:
        """Get all entities for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(self.model)
            .join(
                self.target_model,
                getattr(self.model, self.fk_id_field) == self.target_model.id,
            )
            .where(self.target_model.team_id == team.id)
        ).all()
