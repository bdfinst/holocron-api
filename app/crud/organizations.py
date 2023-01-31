"""BaseCRUD extension and instance for Organization model."""
import logging
from typing import Any, Dict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import Organization

from ._base import BaseCRUD
from .users import users_crud


class OrganizationsCRUD(BaseCRUD[Organization]):
    """Base CRUD extension for Organization model."""

    @staticmethod
    def create_entity(session: Session, json: Dict[str, Any]) -> Organization:
        """Insert organization in database."""
        new_organization = Organization(name=json["name"])

        new_organization.users = [
            users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
        ]

        try:
            session.add(new_organization)
            session.commit()
            session.refresh(new_organization)
        except IntegrityError as err:
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        return new_organization

    def update_entity(
        self, session: Session, json: Dict[str, Any], id_: int
    ) -> Organization:
        """Update organization in database."""
        organization = self.get_entity(session, id_)
        organization.name = json["name"]

        organization.users = [
            users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
        ]

        try:
            session.add(organization)
            session.commit()
            session.refresh(organization)
        except IntegrityError as err:
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        return organization


organizations_crud = OrganizationsCRUD(Organization)
