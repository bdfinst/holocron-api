"""Commit routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import commits_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v2 import CommitV2Schema
from app.security import get_sanitized_id

schema = CommitV2Schema()


@requires_security([requires_admin, requires_team_access])
def list_commits_for_team(team_id: str) -> Tuple[Any, int]:
    """Get commits for a given team id.

    ---
    get:
      description: Get commits belonging to a team or team view
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team or team view to get commits for
      responses:
        200:
          description: Get commits belonging to a team or team view
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/CommitV2'
        404:
          description: Team or team view not found
    """
    with generate_session() as session:
        try:
            raw_commits = commits_crud.get_entities_for_team(
                session, get_sanitized_id(team_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        commits = [schema.dump(commit) for commit in raw_commits]
    result = {"result": commits}
    return jsonify(result), 200


@requires_security([requires_admin])
def get_commit(commit_id: str) -> Tuple[Any, int]:
    """Get commit by id.

    ---
    get:
      description: Get single commit by id
      parameters:
        - in: path
          name: commit_id
          schema:
            type: integer
          required: true
          description: ID of the commit
      responses:
        200:
          description: Get single commit by id
          content:
            application/json:
              schema: CommitV2Schema
        404:
          description: Commit not found
    """
    with generate_session() as session:
        try:
            raw_commit = commits_crud.get_entity(session, get_sanitized_id(commit_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_commit)
    return jsonify(result), 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("commits", __name__, url_prefix="/commits")
    router.route("/team/<team_id>", methods=["GET"])(list_commits_for_team)
    router.route("/<commit_id>", methods=["GET"])(get_commit)
    return router
