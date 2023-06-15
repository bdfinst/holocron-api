"""Build routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import builds_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v1 import BuildV1Schema
from app.security import get_sanitized_id

schema = BuildV1Schema()


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
                      $ref: '#/components/schemas/BuildV1'
        404:
          description: Team or team view not found
    """
    with generate_session() as session:
        try:
            raw_builds = builds_crud.get_entities_for_team(
                session, get_sanitized_id(team_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        build_models = [schema.dump(build) for build in raw_builds]
    result = {"result": build_models}
    return jsonify(result), 200


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
              schema: BuildV1Schema
        404:
          description: Build not found
    """
    with generate_session() as session:
        try:
            raw_build = builds_crud.get_entity(session, get_sanitized_id(build_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_build)
    return jsonify(result), 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("builds", __name__, url_prefix="/builds")
    router.route("/team/<team_id>", methods=["GET"])(list_builds_for_team)
    router.route("/<build_id>", methods=["GET"])(get_build)
    return router
