"""BaseCRUD extension and instance for Valuestream model."""
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.models import Valuestream

from ._base import BaseCRUD


class ValuestreamsCRUD(BaseCRUD[Valuestream]):
    """Base CRUD extension for Valuestream model."""

    @staticmethod
    def create_entity(session: Session, json: Dict[str, Any]) -> Valuestream:
        """Insert valuestream in database."""
        new_valuestream = Valuestream(
            name=json.get("name"),
            organization_id=json.get("organization_id"),
        )

        session.add(new_valuestream)
        session.commit()
        session.refresh(new_valuestream)

        return new_valuestream

    def update_entity(
        self, session: Session, json: Dict[str, Any], id_: int
    ) -> Valuestream:
        """Update valuestream in database."""
        valuestream = self.get_entity(session, id_)
        valuestream.name = json.get("name")
        valuestream.organization_id = json.get("organization_id")

        session.add(valuestream)
        session.commit()
        session.refresh(valuestream)

        return valuestream


valuestreams_crud = ValuestreamsCRUD(Valuestream)
