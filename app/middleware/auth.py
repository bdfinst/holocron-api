"""Authentication middleware."""
import json
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple

import jwt
from flask import Response, request

from app.config import SSO_ENABLED
from app.crud import organizations_crud, teams_crud, users_crud, valuestreams_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import UserSchema
from app.security import log_security_event

schema = UserSchema()


INVALID_PERMISSIONS = "Invalid permissions"


def set_user():
    """Set current user as property of the request."""
    token = request.headers.get("Authorization").split(" ")[-1]
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


def requires_org_leadership(**kwargs) -> Tuple[bool, Optional[str]]:
    """Restrict access for endpoint to users with org leadership access."""
    if not kwargs:
        user = getattr(request, "user", {"isOrgLeadership": False})
        if user["isOrgLeadership"]:
            return True, None

    return False, "ORG_LEADERSHIP"


def requires_org_access(**kwargs) -> Tuple[bool, Optional[str]]:
    """Restrict access for endpoint to users with org access."""
    if not kwargs:
        data = request.json
        if data is not None:
            current_org = (int)(data["organizationId"])
        else:
            return False, "ORGANIZATION_ADMIN"
    else:
        current_org = (int)(kwargs["org_id"])

    user = getattr(request, "user", {"id": 0})
    with generate_session() as session:
        organization = organizations_crud.get_entity(session, current_org)
        if any(
            organization_user.id == user["id"]
            for organization_user in organization.users
        ):
            return True, None

    return False, "ORGANIZATION_ADMIN"


def requires_vs_access(**kwargs) -> Tuple[bool, Optional[str]]:
    """Restrict access for endpoint to users with vs access."""
    if not kwargs:
        data = request.json
        if data is not None:
            current_valuestream = (int)(data["valuestreamId"])
        else:
            return False, "VALUESTREAM_ADMIN OR ORGANIZATION_ADMIN"
    else:
        current_valuestream = (int)(kwargs["valuestream_id"])

    user = getattr(request, "user", {"id": 0})
    with generate_session() as session:
        valuestream = valuestreams_crud.get_entity(session, current_valuestream)
        if any(
            valuestream_user.id == user["id"] for valuestream_user in valuestream.users
        ):
            return True, None

        organization = organizations_crud.get_entity(
            session, valuestream.organization_id
        )
        if any(
            organization_user.id == user["id"]
            for organization_user in organization.users
        ):
            return True, None

    return False, "VALUESTREAM_ADMIN OR ORGANIZATION_ADMIN"


def requires_team_access(**kwargs) -> Tuple[bool, Optional[str]]:
    """Restrict access for endpoint to users with team access."""
    current_team = (int)(kwargs["team_id"])
    user = getattr(request, "user", {"id": 0})
    with generate_session() as session:
        team = teams_crud.get_entity(session, current_team)
        if any(user["id"] == team_usr.id for team_usr in team.users):
            return True, None

        valuestream = valuestreams_crud.get_entity(session, team.valuestream_id)
        if any(
            valuestream_user.id == user["id"] for valuestream_user in valuestream.users
        ):
            return True, None

        organization = organizations_crud.get_entity(
            session, valuestream.organization_id
        )
        if any(
            organization_user.id == user["id"]
            for organization_user in organization.users
        ):
            return True, None

    return False, "TEAM_ADMIN OR VALUESTREAM_ADMIN OR ORGANIZATION_ADMIN"


def requires_admin(**_) -> Tuple[bool, Optional[str]]:
    """Restrict access for endpoint to admins."""
    user = getattr(request, "user", {"isAdmin": False})
    if not SSO_ENABLED or user["isAdmin"]:
        return True, None
    return False, "ADMIN"


def requires_security(arguments) -> Callable:
    """Restrict access based on the required groups."""

    def decorator(original_func):
        @wraps(original_func)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            permission_names = []
            for security_func in arguments:
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
