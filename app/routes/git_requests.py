"""GitRequest routes."""
from flask import Blueprint, jsonify

from app.crud import git_requests_crud
from app.database import generate_session
from app.schemas import GitRequestSchema

router = Blueprint("gitrequests", __name__, url_prefix="/gitrequests")

schema = GitRequestSchema()


@router.route("/team/<id_>", methods=["GET"])
def list_git_requests_for_team(id_: int):
    """Get git requests for a given team id.

    ---
    get:
      description: Get git requests belonging to a team
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the team to get git requests for
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/GitRequest'
    """
    with generate_session() as session:
        raw_git_requests = git_requests_crud.get_entities_for_team(session, id_)
        git_requests = [schema.dump(commit) for commit in raw_git_requests]
    result = {"result": git_requests}
    return jsonify(result), 200


@router.route("/<id_>", methods=["GET"])
def get_git_request(id_: int):
    """Get git request by id.

    ---
    get:
      description: Get single git request by id
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the git request
      responses:
        200:
          content:
            application/json:
              schema: GitRequestSchema
    """
    with generate_session() as session:
        raw_git_request = git_requests_crud.get_entity(session, id_)
        result = schema.dump(raw_git_request)
    return jsonify(result), 200
