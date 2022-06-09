"""Commit routes."""
from flask import Blueprint, jsonify

from app.crud import commits_crud
from app.database import generate_session
from app.schemas import CommitSchema

router = Blueprint("commits", __name__, url_prefix="/commits")

schema = CommitSchema()


@router.route("/team/<id_>", methods=["GET"])
def list_commits_for_team(id_: int):
    """Get commits for a given team id.

    ---
    get:
      description: Get commits belonging to a team
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the team to get commits for
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Commit'
    """
    with generate_session() as session:
        raw_commits = commits_crud.get_entities_for_team(session, id_)
        commits = [schema.dump(commit) for commit in raw_commits]
    result = {"result": commits}
    return jsonify(result), 200


@router.route("/<id_>", methods=["GET"])
def get_commit(id_: int):
    """Get commit by id.

    ---
    get:
      description: Get single commit by id
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the commit
      responses:
        200:
          content:
            application/json:
              schema: CommitSchema
    """
    with generate_session() as session:
        raw_commit = commits_crud.get_entity(session, id_)
        result = schema.dump(raw_commit)
    return jsonify(result), 200
