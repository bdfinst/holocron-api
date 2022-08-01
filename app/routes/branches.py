"""Branch routes."""
from flask import Blueprint, jsonify

from app.crud import branches_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import BranchSchema

router = Blueprint("branches", __name__, url_prefix="/branches")

schema = BranchSchema()


@router.route("/team/<team_id>", methods=["GET"])
def list_branches_for_team(team_id: str):
    """Get branches for a given team id.

    ---
    get:
      description: Get branches belonging to a team
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team to get branches for
      responses:
        200:
          description: Get branches belonging to a team
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Branch'
        404:
          description: Team not found
    """
    with generate_session() as session:
        try:
            raw_branches = branches_crud.get_entities_for_team(session, int(team_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        branches = [schema.dump(branch) for branch in raw_branches]
    result = {"result": branches}
    return jsonify(result), 200


@router.route("/<branch_id>", methods=["GET"])
def get_branch(branch_id: str):
    """Get branch by id.

    ---
    get:
      description: Get single branch by id
      parameters:
        - in: path
          name: branch_id
          schema:
            type: integer
          required: true
          description: ID of the branch
      responses:
        200:
          description: Get single branch by id
          content:
            application/json:
              schema: BranchSchema
        404:
          description: Branch not found
    """
    with generate_session() as session:
        try:
            raw_branch = branches_crud.get_entity(session, int(branch_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_branch)
    return jsonify(result), 200
