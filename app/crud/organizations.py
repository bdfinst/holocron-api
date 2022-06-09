"""BaseCRUD extension and instance for Organization model."""
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.models import Organization

from ._base import BaseCRUD


class OrganizationsCRUD(BaseCRUD[Organization]):
    """Base CRUD extension for Organization model."""

    @staticmethod
    def create_entity(session: Session, json: Dict[str, Any]) -> Organization:
        """Insert organization in database."""
        new_organization = Organization(name=json.get("name"))

        session.add(new_organization)
        session.commit()
        session.refresh(new_organization)

        return new_organization

    def update_entity(
        self, session: Session, json: Dict[str, Any], id_: int
    ) -> Organization:
        """Update organization in database."""
        organization = self.get_entity(session, id_)
        organization.name = json.get("name")

        session.add(organization)
        session.commit()
        session.refresh(organization)

        return organization


organizations_crud = OrganizationsCRUD(Organization)
