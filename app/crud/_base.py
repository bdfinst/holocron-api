"""Base classes for model-based database operations."""
from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import ModelBase

T = TypeVar("T", bound=ModelBase)


class BaseCRUD(Generic[T]):
    """Base class for CRUD methods."""

    def __init__(self, model: Type[T]):
        """Initialize with the given model."""
        self.model = model

    def get_entities(self, session: Session) -> Sequence[T]:
        """Get all entities."""
        return session.scalars(select(self.model)).all()

    def get_entity(self, session: Session, id_: int) -> T:
        """Get entity by id."""
        result = session.scalars(select(self.model).where(self.model.id == id_)).first()
        if result is None:
            raise HolocronIntegrityError(
                f"{self.model.__name__} id", f"Invalid id: {id_}"
            )
        return result

    def delete_entity(self, session: Session, id_: int):
        """Delete entity by id."""
        session.execute(delete(self.model).where(self.model.id == id_))
        session.commit()
