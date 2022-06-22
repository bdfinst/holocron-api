"""Commit routes."""
from flask import Blueprint, jsonify

from app.crud import commits_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import CommitSchema

router = Blueprint("commits", __name__, url_prefix="/commits")

schema = CommitSchema()


@router.route("/team/<team_id>", methods=["GET"])
def list_commits_for_team(team_id: int):
    """Get commits for a given team id.

    ---
    get:
      description: Get commits belonging to a team
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team to get commits for
      responses:
        200:
          description: Get commits belonging to a team
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Commit'
        404:
          description: Team not found
    """
    with generate_session() as session:
        try:
            raw_commits = commits_crud.get_entities_for_team(session, team_id)
        except HolocronIntegrityError:
            return "Resource not found", 404
        commits = [schema.dump(commit) for commit in raw_commits]
    result = {"result": commits}
    return jsonify(result), 200


@router.route("/<commit_id>", methods=["GET"])
def get_commit(commit_id: int):
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
              schema: CommitSchema
        404:
          description: Commit not found
    """
    with generate_session() as session:
        try:
            raw_commit = commits_crud.get_entity(session, commit_id)
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_commit)
    return jsonify(result), 200
