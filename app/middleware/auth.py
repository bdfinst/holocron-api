"""Authentication middleware."""
import jwt
from flask import request

from app.crud import users_crud
from app.database import generate_session
from app.schemas import UserSchema

schema = UserSchema()


def set_user():
    """Set current user as property of the request."""
    token = jwt.decode(
        request.headers.get("Authorization"), options={"verify_signature": False}
    )
    with generate_session() as session:
        current_user = users_crud.upsert_sso_user(session, token)
        current_user = schema.dump(current_user)
    setattr(request, "user", current_user)
