"""BaseCRUD extension and instance for Team model."""
import logging
from dataclasses import dataclass
from typing import Any, Dict, Set

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import Team, TicketBoard

from ._base import BaseCRUD
from .collector_targets import collector_targets_crud
from .users import users_crud

_USED_MSG = "already in use"
_NO_FEATURE_BOARDS_MSG = "team needs at least one feature board"


@dataclass
class TeamValidationData:
    """Class used to help in data validation logic."""

    team: Team
    all_ticket_board_ids: Set[int]


def validate_business_logic_create(team_validation_data: TeamValidationData):
    """Validate business logic when creating a team."""
    validation_checkers = [
        (
            all(
                ct.id not in team_validation_data.all_ticket_board_ids
                for ct in team_validation_data.team.collector_targets
            ),
            "collectorTargetIds",
            _NO_FEATURE_BOARDS_MSG,
        ),
        (
            any(
                ct.team_id is not None
                for ct in team_validation_data.team.collector_targets
            ),
            "collectorTargetIds",
            _USED_MSG,
        ),
    ]
    for checker in validation_checkers:
        is_invalid, invalid_field, reason_for_invalid = checker
        if is_invalid:
            raise HolocronIntegrityError(invalid_field, reason_for_invalid)


def validate_business_logic_update(team_validation_data: TeamValidationData):
    """Validate business logic when updating team."""
    validation_checkers = [
        (
            all(
                ct.id not in team_validation_data.all_ticket_board_ids
                for ct in team_validation_data.team.collector_targets
            ),
            "collectorTargetIds",
            _NO_FEATURE_BOARDS_MSG,
        ),
        (
            any(
                ct.team_id is not None and ct.team_id != team_validation_data.team.id
                for ct in team_validation_data.team.collector_targets
            ),
            "collectorTargetIds",
            _USED_MSG,
        ),
    ]
    for checker in validation_checkers:
        is_invalid, invalid_field, reason_for_invalid = checker
        if is_invalid:
            raise HolocronIntegrityError(invalid_field, reason_for_invalid)


def get_team_validation_data(session: Session, team: Team) -> TeamValidationData:
    """Return team validation data."""
    all_ticket_boards = session.scalars(
        select(TicketBoard).where(TicketBoard.board_id.is_not(None))
    ).all()
    return TeamValidationData(team, {t.id for t in all_ticket_boards})


def is_workflow_only(team_validation_data: TeamValidationData) -> bool:
    """Return if team only has workflow data."""
    return all(
        t.id in team_validation_data.all_ticket_board_ids
        for t in team_validation_data.team.collector_targets
    )


class TeamsCRUD(BaseCRUD[Team]):
    """Base CRUD extension for Team model."""

    @staticmethod
    def create_entity(session: Session, json: Dict[str, Any]) -> Team:
        """Insert team in database."""
        new_team = Team(
            name=json.get("name"),
            team_size=json.get("team_size"),
            valuestream_id=json.get("valuestream_id"),
        )

        new_team.users = [
            users_crud.get_entity(session, user_id)
            for user_id in json.get("user_ids", [])
        ]
        new_team.collector_targets = [
            collector_targets_crud.get_entity(session, target_id)
            for target_id in json.get("collector_target_ids", [])
        ]
        team_validation_data = get_team_validation_data(session, new_team)
        new_team.is_workflow_only = is_workflow_only(team_validation_data)
        validate_business_logic_create(team_validation_data)
        try:
            session.add(new_team)
            session.commit()
            session.refresh(new_team)
        except IntegrityError as err:
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError("valuestream_id", "not found") from err
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        return new_team

    def update_entity(self, session: Session, json: Dict[str, Any], id_: int) -> Team:
        """Update team in database."""
        team = self.get_entity(session, id_)
        team.name = json.get("name")
        team.team_size = json.get("team_size")
        team.valuestream_id = json.get("valuestream_id")

        team.users = [
            users_crud.get_entity(session, user_id)
            for user_id in json.get("user_ids", [])
        ]
        team.collector_targets = [
            collector_targets_crud.get_entity(session, target_id)
            for target_id in json.get("collector_target_ids", [])
        ]
        team_validation_data = get_team_validation_data(session, team)
        team.is_workflow_only = is_workflow_only(team_validation_data)
        validate_business_logic_update(team_validation_data)
        try:
            session.add(team)
            session.commit()
            session.refresh(team)
        except IntegrityError as err:
            if "psycopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError("valuestream_id", "not found") from err
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("name", _USED_MSG) from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        return team


teams_crud = TeamsCRUD(Team)
