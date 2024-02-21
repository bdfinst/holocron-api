"""BaseCRUD extension and instance for Valuestream model."""

import logging
from typing import Any, Dict, Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import Valuestream

from ._base import BaseCRUD
from .users import users_crud


class ValuestreamsCRUD(BaseCRUD[Valuestream]):
    """Base CRUD extension for Valuestream model."""

    def get_entity_without_team_views(self, session: Session, id_: int) -> Valuestream:
        """Get valuestream by id without team views."""
        valuestream: Valuestream = self.get_entity(session, id_)
        result = Valuestream(
            name=valuestream.name,
            organization_id=valuestream.organization_id,
            users=valuestream.users,
            teams=[team for team in valuestream.teams if team.view_owner_id is None],
        )
        result.id = valuestream.id
        return result

    def get_entities_without_team_views(
        self, session: Session
    ) -> Sequence[Valuestream]:
        """Get all valuestreams without team views."""
        valuestreams: Sequence[Valuestream] = self.get_entities(session)
        result = []
        for valuestream in valuestreams:
            new_vs = Valuestream(
                name=valuestream.name,
                organization_id=valuestream.organization_id,
                users=valuestream.users,
                teams=[
                    team for team in valuestream.teams if team.view_owner_id is None
                ],
            )
            new_vs.id = valuestream.id
            result.append(new_vs)
        return result

    def get_entities_without_team_views_paginated(
        self, session: Session, offset=0, limit=100
    ) -> Sequence[Valuestream]:
        """Get paginated valuestreams without team views."""
        valuestreams: Sequence[Valuestream] = self.get_entities_paginated(
            session, offset=offset, limit=limit
        )
        result = []
        for valuestream in valuestreams:
            new_vs = Valuestream(
                name=valuestream.name,
                organization_id=valuestream.organization_id,
                users=valuestream.users,
                teams=[
                    team for team in valuestream.teams if team.view_owner_id is None
                ],
            )
            new_vs.id = valuestream.id
            result.append(new_vs)
        return result

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
        valuestream: Valuestream = self.get_entity(session, id_)
        valuestream.name = json["name"]
        valuestream.organization_id = json["organization_id"]

        try:
            valuestream.users = [
                users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
            ]
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

        vs_no_team_views = Valuestream(
            name=valuestream.name,
            organization_id=valuestream.organization_id,
            users=valuestream.users,
            teams=[team for team in valuestream.teams if team.view_owner_id is None],
        )
        vs_no_team_views.id = valuestream.id

        return vs_no_team_views


valuestreams_crud = ValuestreamsCRUD(Valuestream)
