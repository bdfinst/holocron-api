"""User routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import users_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security
from app.schemas.v1 import UserV1Schema
from app.security import get_sanitized_id

schema = UserV1Schema()


def list_users() -> Tuple[Any, int]:
    """List users route.

    ---
    get:
      description: List users
      responses:
        200:
          description: List users
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/UserV1'
    """
    with generate_session() as session:
        raw_users = users_crud.get_entities(session)
        users = [schema.dump(user) for user in raw_users]
    result = {"result": users}
    return jsonify(result), 200


def get_user(user_id: str) -> Tuple[Any, int]:
    """Get user by id route.

    ---
    get:
      description: Get user
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
          required: true
          description: ID of the user
      responses:
        200:
          description: Get user
          content:
            application/json:
              schema: UserV1Schema
        404:
          description: User not found
    """
    with generate_session() as session:
        try:
            raw_user = users_crud.get_entity(session, get_sanitized_id(user_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_user)
    return jsonify(result), 200


@requires_security([requires_admin])
def delete_user(user_id: str) -> Tuple[Any, int]:
    """Delete user route.

    ---
    delete:
      description: Delete user
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
          required: true
          description: ID of the user
      responses:
        204:
          description: The user was successfully deleted
    """
    with generate_session() as session:
        users_crud.delete_entity(session, get_sanitized_id(user_id))
    return "", 204


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("users", __name__, url_prefix="/users")
    router.route("", methods=["GET"])(list_users)
    router.route("/<user_id>", methods=["GET"])(get_user)
    router.route("/<user_id>", methods=["DELETE"])(delete_user)
    return router
