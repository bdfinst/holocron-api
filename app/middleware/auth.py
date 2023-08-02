"""Authentication middleware."""
import json
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

import jwt
from flask import Response, request
from sqlalchemy.orm import Session

from app.config import FEATURE_FLAGS, SSO_ENABLED
from app.crud import (
    organizations_crud,
    team_views_crud,
    teams_crud,
    users_crud,
    valuestreams_crud,
)
from app.crud.organizations import OrganizationsCRUD
from app.crud.teams import TeamsCRUD
from app.crud.valuestreams import ValuestreamsCRUD
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.models import Team, Valuestream
from app.schemas.v2 import UserV2Schema
from app.security import get_sanitized_id, log_security_event

schema = UserV2Schema()


INVALID_PERMISSIONS = "Invalid permissions"
FEATURE_NOT_PERMITTED = "Feature not yet permitted"


def set_user() -> None:
    """Set current user as property of the request."""
    token = request.headers.get("Authorization", "").split(" ")[-1]
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    with generate_session() as session:
        current_user = users_crud.upsert_sso_user(session, decoded_token)
        current_user = schema.dump(current_user)
    setattr(request, "user", current_user)


def strip_returns(string: str) -> str:
    """Strip out line and carriage returns."""
    while "%0A" in string or "%0D" in string:
        string = string.replace("%0A", "")
        string = string.replace("%0D", "")
    return string


def return_user(response: Response) -> Response:
    """Add the current user to the response headers."""
    user_json = json.dumps(getattr(request, "user", None))
    user_json = strip_returns(user_json)
    response.headers["X-User"] = user_json
    return response


def log_unpriviledge_user_access(user: Dict[str, Any], access_group: str):
    """Log when lower privledge user access higher level."""
    msg = f"NON {access_group} USER ACCESS: {user['username']} (id: {user['id']})"
    log_security_event(msg)


def requires_org_leadership(**_) -> Tuple[bool, Optional[str]]:
    """Restrict access for endpoint to users with org leadership access."""
    user = getattr(request, "user", {"isOrgLeadership": False})
    return (True, None) if user["isOrgLeadership"] else (False, "ORG_LEADERSHIP")


class EntityType(Enum):
    """Enum for team, valuestream, or organization."""

    TEAM = "team"
    VALUESTREAM = "valuestream"
    ORGANIZATION = "organization"


def check_entity_access(
    entity_type: EntityType, entity_id: int, session: Session, user_id: int
) -> bool:
    """Check if user has access to a given team, valuestream, or organization.

    If not, recursively checks containing valuestream/organization as well.
    """
    crud: Union[TeamsCRUD, ValuestreamsCRUD, OrganizationsCRUD]
    if entity_type == EntityType.TEAM:
        crud = teams_crud
    elif entity_type == EntityType.VALUESTREAM:
        crud = valuestreams_crud
    else:
        crud = organizations_crud

    entity = crud.get_entity(session, entity_id)

    if any(entity_user.id == user_id for entity_user in entity.users):
        return True

    if entity_type == EntityType.TEAM:
        entity = cast(Team, entity)
        return check_entity_access(
            EntityType.VALUESTREAM, entity.valuestream_id, session, user_id
        )
    if entity_type == EntityType.VALUESTREAM:
        entity = cast(Valuestream, entity)
        return check_entity_access(
            EntityType.ORGANIZATION, entity.organization_id, session, user_id
        )
    return False


def requires_org_access(**kwargs) -> Tuple[bool, Optional[str]]:
    """Restrict access for endpoint to users with org access."""
    if not kwargs:
        data = request.json
        if data is not None:
            org_id = get_sanitized_id(data["organizationId"])
        else:
            return False, "ORGANIZATION_ADMIN"
    else:
        org_id = get_sanitized_id(kwargs["org_id"])

    user = getattr(request, "user", {"id": 0})
    with generate_session() as session:
        if check_entity_access(EntityType.ORGANIZATION, org_id, session, user["id"]):
            return True, None

    return False, "ORGANIZATION_ADMIN"


def requires_vs_access(**kwargs) -> Tuple[bool, Optional[str]]:
    """Restrict access for endpoint to users with vs access."""
    if not kwargs:
        data = request.json
        if data is not None:
            vs_id = get_sanitized_id(data["valuestreamId"])
        else:
            return False, "VALUESTREAM_ADMIN OR ORGANIZATION_ADMIN"
    else:
        vs_id = get_sanitized_id(kwargs["valuestream_id"])

    user = getattr(request, "user", {"id": 0})
    with generate_session() as session:
        if check_entity_access(EntityType.VALUESTREAM, vs_id, session, user["id"]):
            return True, None

    return False, "VALUESTREAM_ADMIN OR ORGANIZATION_ADMIN"


def get_team_id_for_team_access_feature_team_views(session: Session, **kwargs) -> int:
    """Get team id for requires_team_access for feature team views."""
    if kwargs:
        if "team_view_id" not in kwargs:
            # team_id in kwargs (update/delete team method)
            return get_sanitized_id(kwargs["team_id"])
        # (update/delete team view)
        team_view_id = get_sanitized_id(kwargs["team_view_id"])
        team_view = team_views_crud.get_entity(session, team_view_id)
        return team_view.view_owner_id if team_view.view_owner_id is not None else -1
    # creating team view
    data = request.json
    return get_sanitized_id(data["viewOwnerId"]) if data is not None else -1


def requires_team_access(**kwargs) -> Tuple[bool, Optional[str]]:
    """Restrict access for endpoint to users with team access."""
    user = getattr(request, "user", {"id": 0})
    with generate_session() as session:
        team_id = (
            get_team_id_for_team_access_feature_team_views(session, **kwargs)
            if FEATURE_FLAGS["FEATURE_TEAM_VIEWS"]
            else get_sanitized_id(kwargs["team_id"])
        )
        if check_entity_access(EntityType.TEAM, team_id, session, user["id"]):
            return True, None

    return False, "TEAM_ADMIN OR VALUESTREAM_ADMIN OR ORGANIZATION_ADMIN"


def requires_admin(**_) -> Tuple[bool, Optional[str]]:
    """Restrict access for endpoint to admins."""
    user = getattr(request, "user", {"isAdmin": False})
    return (True, None) if user["isAdmin"] or not SSO_ENABLED else (False, "ADMIN")


def requires_security(security_functions: List[Callable]) -> Callable:
    """Restrict access based on the required groups."""

    def decorator(original_func):
        @wraps(original_func)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            permission_names = []
            for security_func in security_functions:
                try:
                    success, name = security_func(**kwargs)
                except HolocronIntegrityError:
                    return "Resource not found", 404
                if success:
                    return original_func(*args, **kwargs)
                permission_names.append(name)
            result = " OR ".join(permission_names)
            log_unpriviledge_user_access(user, result)
            return INVALID_PERMISSIONS, 403

        return wrapper

    return decorator
