"""Branch routes."""
from flask import Blueprint, jsonify

from app.crud import branches_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import BranchSchema

router = Blueprint("branches", __name__, url_prefix="/branches")

schema = BranchSchema()


@router.route("/team/<id_>", methods=["GET"])
def list_branches_for_team(id_: int):
    """Get branches for a given team id.

    ---
    get:
      description: Get branches belonging to a team
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the team to get branches for
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Branch'
        404:
          content:
            text/plain:
              schema: string
    """
    with generate_session() as session:
        try:
            raw_branches = branches_crud.get_entities_for_team(session, id_)
        except HolocronIntegrityError:
            return "Resource not found", 404
        branches = [schema.dump(branch) for branch in raw_branches]
    result = {"result": branches}
    return jsonify(result), 200


@router.route("/<id_>", methods=["GET"])
def get_branch(id_: int):
    """Get branch by id.

    ---
    get:
      description: Get single branch by id
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the branch
      responses:
        200:
          content:
            application/json:
              schema: BranchSchema
        404:
          content:
            text/plain:
              schema: string
    """
    with generate_session() as session:
        try:
            raw_branch = branches_crud.get_entity(session, id_)
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_branch)
    return jsonify(result), 200
