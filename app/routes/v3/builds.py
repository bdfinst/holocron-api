"""Build routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from app.crud import builds_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v2 import BuildV2Schema
from app.security import get_sanitized_id
from app.utils.pagination import construct_next_page_url, get_limit_offset_page

schema = BuildV2Schema()


@requires_security([requires_admin, requires_team_access])
def list_builds_for_team(team_id: str) -> Tuple[Any, int]:
    """Get builds for a given team id.

    ---
    get:
      description: Get builds belonging to a team or team view
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team or team view to get builds for
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
          description: Get builds belonging to a team or team view
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/BuildV2'
        404:
          description: Team or team view not found
    """
    limit, offset, page = get_limit_offset_page(request.args)
    db_id = get_sanitized_id(team_id)
    with generate_session() as session:
        try:
            count = builds_crud.get_count_for_team(session, db_id)
            raw_builds = builds_crud.get_entities_for_team_paginated(
                session, db_id, offset=offset, limit=limit
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        build_models = [schema.dump(build) for build in raw_builds]
    result = {"result": build_models}
    response = jsonify(result)
    response.headers["next-page"] = construct_next_page_url(
        request.url, limit, offset, page, count
    )  # type: ignore
    return response, 200


@requires_security([requires_admin])
def get_build(build_id: str) -> Tuple[Any, int]:
    """Get Build by id.

    ---
    get:
      description: Get single build by id
      parameters:
        - in: path
          name: build_id
          schema:
            type: integer
          required: true
          description: ID of the build
      responses:
        200:
          description: Get single build by id
          content:
            application/json:
              schema: BuildV2Schema
        404:
          description: Build not found
    """
    with generate_session() as session:
        try:
            raw_build = builds_crud.get_entity(session, get_sanitized_id(build_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_build)
    response = jsonify(result)
    return response, 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("builds", __name__, url_prefix="/builds")
    router.route("/team/<team_id>", methods=["GET"])(list_builds_for_team)
    router.route("/<build_id>", methods=["GET"])(get_build)
    return router
