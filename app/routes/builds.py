"""Build routes."""
from flask import Blueprint, jsonify

from app.crud import builds_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import BuildSchema

router = Blueprint("builds", __name__, url_prefix="/builds")
schema = BuildSchema()


@router.route("/team/<id_>", methods=["GET"])
def list_builds_for_team(id_: int):
    """Get builds for a given team id.

    ---
    get:
      description: Get builds belonging to a team
      parameters:
        - in: path
          name: id_
          schema:
            type: integer
          required: true
          description: ID of the team to get builds for
      responses:
        200:
          description: Get builds belonging to a team
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Build'
        404:
          description: Team not found
    """
    with generate_session() as session:
        try:
            raw_builds = builds_crud.get_entities_for_team(session, id_)
        except HolocronIntegrityError:
            return "Resource not found", 404
        build_models = [schema.dump(build) for build in raw_builds]
    result = {"result": build_models}
    return jsonify(result), 200


@router.route("/<id_>", methods=["GET"])
def get_build(id_):
    """Get Build by id.

    ---
    get:
      description: Get single build by id
      parameters:
        - in: path
          name: id_
          schema:
            type: integer
          required: true
          description: ID of the build
      responses:
        200:
          description: Get single build by id
          content:
            application/json:
              schema: BuildSchema
        404:
          description: Build not found
    """
    with generate_session() as session:
        try:
            raw_build = builds_crud.get_entity(session, id_)
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_build)
    return jsonify(result), 200
