"""User routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from app.crud import users_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security
from app.schemas.v2 import UserV2Schema
from app.security import get_sanitized_id
from app.utils.pagination import construct_next_page_url, get_limit_offset_page

schema = UserV2Schema()


def list_users() -> Tuple[Any, int]:
    """List users route.

    ---
    get:
      description: List users
      parameters:
        - in: query
          name: per_page
          schema:
            type: integer
          required: false
          description: The maximum number of items to return
        - in: query
          name: page
          schema:
            type: integer
          required: false
          description: The page of the data set to retrieve
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
                      $ref: '#/components/schemas/UserV2'
    """
    limit, offset, page = get_limit_offset_page(request.args)
    with generate_session() as session:
        count = users_crud.get_count(session)
        raw_users = users_crud.get_entities_paginated(
            session, limit=limit, offset=offset
        )
        users = [schema.dump(user) for user in raw_users]
    result = {"result": users}
    response = jsonify(result)
    response.headers["next-page"] = construct_next_page_url(
        request.url, limit, offset, page, count
    )  # type: ignore
    return response, 200


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
              schema: UserV2Schema
        404:
          description: User not found
    """
    with generate_session() as session:
        try:
            raw_user = users_crud.get_entity(session, get_sanitized_id(user_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_user)
    response = jsonify(result)
    return response, 200


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
