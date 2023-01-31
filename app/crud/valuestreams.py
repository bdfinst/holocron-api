"""BaseCRUD extension and instance for Valuestream model."""
import logging
from typing import Any, Dict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import Valuestream

from ._base import BaseCRUD
from .users import users_crud


class ValuestreamsCRUD(BaseCRUD[Valuestream]):
    """Base CRUD extension for Valuestream model."""

    @staticmethod
    def create_entity(session: Session, json: Dict[str, Any]) -> Valuestream:
        """Insert valuestream in database."""
        new_valuestream = Valuestream(
            name=json["name"],
            organization_id=json["organization_id"],
        )

        new_valuestream.users = [
            users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
        ]

        try:
            session.add(new_valuestream)
            session.commit()
            session.refresh(new_valuestream)
        except IntegrityError as err:
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError("organization_id", "not found") from err
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        return new_valuestream

    def update_entity(
        self, session: Session, json: Dict[str, Any], id_: int
    ) -> Valuestream:
        """Update valuestream in database."""
        valuestream = self.get_entity(session, id_)
        valuestream.name = json["name"]
        valuestream.organization_id = json["organization_id"]

        valuestream.users = [
            users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
        ]

        try:
            session.add(valuestream)
            session.commit()
            session.refresh(valuestream)
        except IntegrityError as err:
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError("organization_id", "not found") from err
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        return valuestream


valuestreams_crud = ValuestreamsCRUD(Valuestream)
