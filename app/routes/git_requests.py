"""GitRequest routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import git_requests_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import GitRequestSchema
from app.security import get_sanitized_id

router = Blueprint("gitrequests", __name__, url_prefix="/gitrequests")

schema = GitRequestSchema()


@router.route("/team/<team_id>", methods=["GET"])
def list_git_requests_for_team(team_id: str) -> Tuple[Any, int]:
    """Get git requests for a given team id.

    ---
    get:
      description: Get git requests belonging to a team
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team to get git requests for
      responses:
        200:
          description: Get git requests belonging to a team
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/GitRequest'
        404:
          description: Team not found
    """
    with generate_session() as session:
        try:
            raw_git_requests = git_requests_crud.get_entities_for_team(
                session, get_sanitized_id(team_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        git_requests = [schema.dump(commit) for commit in raw_git_requests]
    result = {"result": git_requests}
    return jsonify(result), 200


@router.route("/<git_request_id>", methods=["GET"])
def get_git_request(git_request_id: str) -> Tuple[Any, int]:
    """Get git request by id.

    ---
    get:
      description: Get single git request by id
      parameters:
        - in: path
          name: git_request_id
          schema:
            type: integer
          required: true
          description: ID of the git request
      responses:
        200:
          description: Get single git request by id
          content:
            application/json:
              schema: GitRequestSchema
        404:
          description: Git request not found
    """
    with generate_session() as session:
        try:
            raw_git_request = git_requests_crud.get_entity(
                session, get_sanitized_id(git_request_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_git_request)
    return jsonify(result), 200
