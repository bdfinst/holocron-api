"""BaseCRUD extension and instance for ValueStream model."""

import logging
from typing import Any, Dict, Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import ValueStream

from ._base import BaseCRUD
from .users import users_crud


class ValueStreamsCRUD(BaseCRUD[ValueStream]):
    """Base CRUD extension for ValueStream model."""

    def get_entity_without_team_views(self, session: Session, id_: int) -> ValueStream:
        """Get value stream by id without team views."""
        value_stream: ValueStream = self.get_entity(session, id_)
        result = ValueStream(
            name=value_stream.name,
            organization_id=value_stream.organization_id,
            users=value_stream.users,
            teams=[team for team in value_stream.teams if team.view_owner_id is None],
        )
        result.id = value_stream.id
        return result

    def get_entities_without_team_views(
        self, session: Session
    ) -> Sequence[ValueStream]:
        """Get all value streams without team views."""
        value_streams: Sequence[ValueStream] = self.get_entities(session)
        result = []
        for value_stream in value_streams:
            new_vs = ValueStream(
                name=value_stream.name,
                organization_id=value_stream.organization_id,
                users=value_stream.users,
                teams=[
                    team for team in value_stream.teams if team.view_owner_id is None
                ],
            )
            new_vs.id = value_stream.id
            result.append(new_vs)
        return result

    def get_entities_without_team_views_paginated(
        self, session: Session, offset=0, limit=100
    ) -> Sequence[ValueStream]:
        """Get paginated value streams without team views."""
        value_streams: Sequence[ValueStream] = self.get_entities_paginated(
            session, offset=offset, limit=limit
        )
        result = []
        for value_stream in value_streams:
            new_vs = ValueStream(
                name=value_stream.name,
                organization_id=value_stream.organization_id,
                users=value_stream.users,
                teams=[
                    team for team in value_stream.teams if team.view_owner_id is None
                ],
            )
            new_vs.id = value_stream.id
            result.append(new_vs)
        return result

    @staticmethod
    def create_entity(session: Session, json: Dict[str, Any]) -> ValueStream:
        """Insert value stream in database."""
        new_value_stream = ValueStream(
            name=json["name"],
            organization_id=json["organization_id"],
        )

        new_value_stream.users = [
            users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
        ]

        try:
            session.add(new_value_stream)
            session.commit()
            session.refresh(new_value_stream)
        except IntegrityError as err:
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError("organization_id", "not found") from err
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        return new_value_stream

    def update_entity(
        self, session: Session, json: Dict[str, Any], id_: int
    ) -> ValueStream:
        """Update value stream in database."""
        value_stream: ValueStream = self.get_entity(session, id_)
        value_stream.name = json["name"]
        value_stream.organization_id = json["organization_id"]

        try:
            value_stream.users = [
                users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
            ]
            session.add(value_stream)
            session.commit()
            session.refresh(value_stream)
        except IntegrityError as err:
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError("organization_id", "not found") from err
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        vs_no_team_views = ValueStream(
            name=value_stream.name,
            organization_id=value_stream.organization_id,
            users=value_stream.users,
            teams=[team for team in value_stream.teams if team.view_owner_id is None],
        )
        vs_no_team_views.id = value_stream.id

        return vs_no_team_views


value_streams_crud = ValueStreamsCRUD(ValueStream)
