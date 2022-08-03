"""Authentication middleware."""
import json
from typing import Callable

import jwt
from flask import Response, request

from app.config import SSO_ENABLED
from app.crud import teams_crud, users_crud
from app.database import generate_session
from app.schemas import UserSchema

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


def requires_admin(func: Callable) -> Callable:
    """Restrict access for endpoint to admins."""

    def wrapper(*args, **kwargs):
        user = getattr(request, "user", None)
        if not SSO_ENABLED or user["isAdmin"]:
            return func(*args, **kwargs)
        return INVALID_PERMISSIONS, 403

    wrapper.__name__ = func.__name__
    return wrapper


def requires_leadership(func: Callable) -> Callable:
    """Restrict access for endpoint to leadership."""

    def wrapper(*args, **kwargs):
        user = getattr(request, "user", None)
        if not SSO_ENABLED or user["isOrgLeadership"]:
            return func(*args, **kwargs)
        return INVALID_PERMISSIONS, 403

    wrapper.__name__ = func.__name__
    return wrapper


def requires_admin_or_member(func: Callable) -> Callable:
    """Restrict access for endpoint to admins or team members."""

    def wrapper(*args, **kwargs):
        user = getattr(request, "user", None)
        if not SSO_ENABLED or user["isAdmin"]:
            return func(*args, **kwargs)
        with generate_session() as session:
            team = teams_crud.get_entity(session, kwargs["team_id"])
            if user["id"] in team.users:
                return func(*args, **kwargs)
        return INVALID_PERMISSIONS, 403

    wrapper.__name__ = func.__name__
    return wrapper
