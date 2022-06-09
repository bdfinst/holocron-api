"""Base classes for model-based database operations."""
from typing import Generic, List, Type, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import CollectorTarget, ModelBase, Pipeline, Repository, TicketBoard

T = TypeVar("T", bound=ModelBase)


class BaseCRUD(Generic[T]):
    """Base class for CRUD methods."""

    def __init__(self, model: Type[ModelBase]):
        """Initialize with the given model."""
        self.model = model

    def get_entities(self, session: Session) -> List[T]:
        """Get all entities."""
        return session.scalars(select(self.model)).all()

    def get_entity(self, session: Session, id_: int) -> T:
        """Get entity by id."""
        return session.scalars(select(self.model).where(self.model.id == id_)).first()

    def delete_entity(self, session: Session, id_: int):
        """Delete entity by id."""
        session.execute(delete(self.model).where(self.model.id == id_))
        session.commit()


class BaseMetricCRUD(BaseCRUD[T]):
    """Extended base class for CRUD methods on team metric models."""

    def __init__(self, model: Type[ModelBase], target_model: Type[CollectorTarget]):
        """Initialize with the given model with collector target parent."""
        if target_model == Repository:
            id_field = "repository_id"
        elif target_model == Pipeline:
            id_field = "pipeline_id"
        elif target_model == TicketBoard:
            id_field = "board_id"
        else:
            raise ValueError("Target model is not a CollectorTarget type.")

        if not hasattr(model, id_field):
            raise TypeError(f"{model} has no attribute {id_field}")

        self.target_model = target_model
        self.id_field = id_field
        super().__init__(model)

    def get_entities_for_team(self, session: Session, team_id: int) -> List[T]:
        """Get all entities for a given team."""
        return session.scalars(
            select(self.model)
            .join(
                self.target_model,
                getattr(self.model, self.id_field) == self.target_model.id,
            )
            .where(self.target_model.team_id == team_id)
        ).all()
