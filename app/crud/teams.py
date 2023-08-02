"""BaseCRUD extension and instance for Team model."""
import logging
from typing import Any, Dict, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import CollectorTarget, CollectorTargetType, Team, TicketBoard

from ._base import BaseCRUD
from .collector_targets import collector_targets_crud
from .users import users_crud


def is_workflow_only(session: Session, team: Team) -> bool:
    """Return if team only has workflow data."""

    def is_ticket_board(target: CollectorTarget):
        queried_ticket_board = session.scalars(
            select(TicketBoard)
            .where(TicketBoard.type == CollectorTargetType.WORKFLOW)
            .where(TicketBoard.id == target.id)
        ).first()
        return queried_ticket_board is not None

    return all(is_ticket_board(ct) for ct in team.collector_targets)


class TeamsCRUD(BaseCRUD[Team]):
    """Base CRUD extension for Team model."""

    def get_entity_no_team_view(self, session: Session, id_: int) -> Team:
        """Get team that is not team view."""
        team = session.scalars(
            select(Team).where(Team.view_owner_id.is_(None)).where(Team.id == id_)
        ).first()
        if team is None:
            raise HolocronIntegrityError(f"{Team.__name__} id", f"Invalid id: {id_}")
        return team

    def get_entities_without_team_views(self, session: Session) -> Sequence[Team]:
        """Get all teams without team views."""
        return session.scalars(select(Team).where(Team.view_owner_id.is_(None))).all()

    @staticmethod
    def create_entity(session: Session, json: Dict[str, Any]) -> Team:
        """Insert team in database."""
        new_team = Team(
            name=json["name"],
            team_size=json["team_size"],
            valuestream_id=json["valuestream_id"],
        )

        new_team.users = [
            users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
        ]
        new_team.collector_targets = [
            collector_targets_crud.get_entity(session, target_id)
            for target_id in json["collector_target_ids"]
        ]
        new_team.is_workflow_only = is_workflow_only(session, new_team)
        try:
            session.add(new_team)
        except IntegrityError as err:
            session.rollback()
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError("valuestream_id", "not found") from err
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        session.commit()
        session.refresh(new_team)
        return new_team

    def update_entity(self, session: Session, json: Dict[str, Any], id_: int) -> Team:
        """Update team in database."""
        team: Team = self.get_entity(session, id_)
        team.name = json["name"]
        team.team_size = json["team_size"]
        team.valuestream_id = json["valuestream_id"]

        team.users = [
            users_crud.get_entity(session, user_id) for user_id in json["user_ids"]
        ]
        team.collector_targets = [
            collector_targets_crud.get_entity(session, target_id)
            for target_id in json["collector_target_ids"]
        ]
        team.is_workflow_only = is_workflow_only(session, team)
        try:
            session.add(team)
        except IntegrityError as err:
            session.rollback()
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError("valuestream_id", "not found") from err
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        session.commit()
        session.refresh(team)
        return team


teams_crud = TeamsCRUD(Team)
