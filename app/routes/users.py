"""User routes."""
from flask import Blueprint, jsonify

from app.crud import users_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin
from app.schemas import UserSchema

router = Blueprint("users", __name__, url_prefix="/users")

schema = UserSchema()


@router.route("", methods=["GET"])
def list_users():
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
                      $ref: '#/components/schemas/User'
    """
    with generate_session() as session:
        raw_users = users_crud.get_entities(session)
        users = [schema.dump(user) for user in raw_users]
    result = {"result": users}
    return jsonify(result), 200


@router.route("/<user_id>", methods=["GET"])
def get_user(user_id: str):
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
              schema: UserSchema
        404:
          description: User not found
    """
    with generate_session() as session:
        try:
            raw_user = users_crud.get_entity(session, int(user_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_user)
    return jsonify(result), 200


@router.route("/<user_id>", methods=["DELETE"])
@requires_admin
def delete_user(user_id: str):
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
        users_crud.delete_entity(session, int(user_id))
    return "", 204
