"""BaseCRUD extension and instance for Team views model."""

import logging
from typing import Any, Dict, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import Team

from ._base import BaseCRUD
from .collector_targets import collector_targets_crud
from .teams import is_workflow_only, teams_crud


class TeamViewsCRUD(BaseCRUD[Team]):
    """Base CRUD extension for Team views model."""

    def get_entity(self, session: Session, id_: int) -> Team:
        """Get team view."""
        team_view = session.scalars(
            select(Team).where(Team.view_owner_id.is_not(None)).where(Team.id == id_)
        ).first()
        if team_view is None:
            raise HolocronIntegrityError(f"{Team.__name__} id", f"Invalid id: {id_}")
        return team_view

    def get_entities(self, session: Session) -> Sequence[Team]:
        """Get all team views."""
        return session.scalars(
            select(Team).where(Team.view_owner_id.is_not(None))
        ).all()

    def get_entities_paginated(
        self, session: Session, offset=0, limit=100
    ) -> Sequence[Team]:
        """Get paginated team views."""
        return session.scalars(
            select(Team)
            .where(Team.view_owner_id.is_not(None))
            .offset(offset)
            .limit(limit)
        ).all()

    def update_entity(self, session: Session, json: Dict[str, Any], id_: int) -> Team:
        """Update a team view in the database."""
        team_view: Team = self.get_entity(session, id_)

        team_view.name = json["name"]

        try:
            team_view.collector_targets = [
                collector_targets_crud.get_entity(session, target_id)
                for target_id in json["collector_target_ids"]
            ]
            team_view.is_workflow_only = is_workflow_only(session, team_view)
            session.add(team_view)
            session.commit()
        except IntegrityError as err:
            session.rollback()
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError(
                    "value_stream_id or view_owner_id", "not found"
                ) from err
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        session.refresh(team_view)
        return team_view

    def create_entity(self, session: Session, json: Dict[str, Any]) -> Team:
        """Insert team in database."""
        owning_team: Team = teams_crud.get_entity(session, json["view_owner_id"])

        new_team_view = Team(
            name=json["name"],
            view_owner_id=json["view_owner_id"],
            value_stream_id=owning_team.value_stream_id,
            team_size=owning_team.team_size,
        )

        new_team_view.users = owning_team.users
        new_team_view.collector_targets = [
            collector_targets_crud.get_entity(session, target_id)
            for target_id in json["collector_target_ids"]
        ]

        new_team_view.is_workflow_only = is_workflow_only(session, new_team_view)
        try:
            session.add(new_team_view)
            session.commit()
        except IntegrityError as err:
            session.rollback()
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError(
                    "value_stream_id or view_owner_id", "not found"
                ) from err
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        session.refresh(new_team_view)
        return new_team_view


team_views_crud = TeamViewsCRUD(Team)
