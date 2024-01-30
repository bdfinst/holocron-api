"""Business logic team middleware."""

from functools import wraps
from typing import Callable, Tuple

from flask import request
from marshmallow import ValidationError
from sqlalchemy.orm import Session

from app.crud import collector_targets_crud, ticket_boards_crud, valuestreams_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas.v2 import TeamV2Schema, TeamViewV2Schema
from app.security import MALFORMED_REQ_PARAMS_MSG, get_sanitized_id, log_security_event

USED_COLLECTOR_TARGET_MSG = "collectorTargetIds - already in use"
TEAM_NAME_ALREADY_EXISTS_MSG = "name - already exists"

team_schema = TeamV2Schema()
team_view_schema = TeamViewV2Schema()


def is_ticket_board(session: Session, collector_target_id: int) -> bool:
    """Return whether collector_target_id is a ticket board."""
    try:
        ticket_boards_crud.get_entity(session, collector_target_id)
        return True
    except HolocronIntegrityError:
        return False


def is_collector_target_in_use_create(
    session: Session, collector_target_id: int
) -> bool:
    """Return whether collector target is in use when creating team."""
    collector_target = collector_targets_crud.get_entity(session, collector_target_id)
    return collector_target.team_id is not None


def is_collector_target_in_use_update(
    session: Session, collector_target_id: int, team_id: int
) -> bool:
    """Return whether collector target is in use when updating team."""
    collector_target = collector_targets_crud.get_entity(session, collector_target_id)
    return collector_target.team_id is not None and collector_target.team_id != team_id


def is_valid_team_data_for_create(*_, **__) -> Tuple[bool, str]:
    """Validate business logic when creating a team."""
    data = request.json
    name = ""
    valuestream_id = -1
    collector_target_ids = []
    if data is not None:
        name = (str)(data["name"])
        valuestream_id = get_sanitized_id(data["valuestreamId"])
        collector_target_ids = data["collectorTargetIds"]

    with generate_session() as session:
        valuestream = valuestreams_crud.get_entity(session, valuestream_id)
        validators = [
            (
                any(team.name == name for team in valuestream.teams),
                TEAM_NAME_ALREADY_EXISTS_MSG,
            ),
            (
                any(
                    is_collector_target_in_use_create(session, ct_id)
                    for ct_id in collector_target_ids
                ),
                USED_COLLECTOR_TARGET_MSG,
            ),
        ]
        for validator in validators:
            is_invalid, invalid_msg = validator
            if is_invalid:
                return False, invalid_msg
    return True, ""


def is_valid_team_data_for_update(*_, **kwargs) -> Tuple[bool, str]:
    """Validate business logic when updating a team."""
    team_id = get_sanitized_id(kwargs["team_id"])
    data = request.json
    name = ""
    valuestream_id = -1
    collector_target_ids = []
    if data is not None:
        name = (str)(data["name"])
        valuestream_id = get_sanitized_id(data["valuestreamId"])
        collector_target_ids = data["collectorTargetIds"]

    with generate_session() as session:
        valuestream = valuestreams_crud.get_entity(session, valuestream_id)
        validators = [
            (
                any(
                    team.name == name and team.id != team_id
                    for team in valuestream.teams
                ),
                TEAM_NAME_ALREADY_EXISTS_MSG,
            ),
            (
                any(
                    is_collector_target_in_use_update(session, ct_id, team_id)
                    for ct_id in collector_target_ids
                ),
                USED_COLLECTOR_TARGET_MSG,
            ),
        ]
        for validator in validators:
            is_invalid, invalid_msg = validator
            if is_invalid:
                return False, invalid_msg
    return True, ""


def requires_valid_team_data(original_func: Callable) -> Callable:
    """Restrict team data type middleware."""

    @wraps(original_func)
    def wrapper(*args, **kwargs):
        try:
            team_schema.load(request.json)
            is_valid, invalid_msg = (
                is_valid_team_data_for_update(*args, **kwargs)
                if kwargs
                else is_valid_team_data_for_create(*args, **kwargs)
            )
        except ValidationError as err:
            log_security_event(MALFORMED_REQ_PARAMS_MSG)
            return err.messages, 400
        except HolocronIntegrityError:
            return "Resource not found", 404
        return original_func(*args, **kwargs) if is_valid else (invalid_msg, 400)

    return wrapper


def is_valid_team_view_data_for_create(*_, **___) -> Tuple[bool, str]:
    """Validate business logic when creating a team view."""
    data = request.json
    collector_target_ids = data["collectorTargetIds"] if data is not None else []

    with generate_session() as session:
        validators = [
            (
                any(
                    is_collector_target_in_use_create(session, ct_id)
                    for ct_id in collector_target_ids
                ),
                USED_COLLECTOR_TARGET_MSG,
            ),
        ]
        for validator in validators:
            is_invalid, invalid_msg = validator
            if is_invalid:
                return False, invalid_msg
    return True, ""


def is_valid_team_view_data_for_update(*_, **kwargs) -> Tuple[bool, str]:
    """Validate business logic when updating a team view."""
    team_view_id = get_sanitized_id(kwargs["team_view_id"])
    data = request.json
    collector_target_ids = data["collectorTargetIds"] if data is not None else []

    with generate_session() as session:
        validators = [
            (
                any(
                    is_collector_target_in_use_update(session, ct_id, team_view_id)
                    for ct_id in collector_target_ids
                ),
                USED_COLLECTOR_TARGET_MSG,
            ),
        ]
        for validator in validators:
            is_invalid, invalid_msg = validator
            if is_invalid:
                return False, invalid_msg
    return True, ""


def requires_valid_team_view_data(original_func: Callable) -> Callable:
    """Restrict team view data type middleware."""

    @wraps(original_func)
    def wrapper(*args, **kwargs):
        try:
            team_view_schema.load(request.json)
            is_valid, invalid_msg = (
                is_valid_team_view_data_for_update(*args, **kwargs)
                if kwargs
                else is_valid_team_view_data_for_create(*args, **kwargs)
            )
        except ValidationError as err:
            log_security_event(MALFORMED_REQ_PARAMS_MSG)
            return err.messages, 400
        except HolocronIntegrityError:
            return "Resource not found", 404
        return original_func(*args, **kwargs) if is_valid else (invalid_msg, 400)

    return wrapper
