"""Repository routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import repositories_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import RepositorySchema
from app.security import get_sanitized_id

router = Blueprint("repositories", __name__, url_prefix="/repositories")

schema = RepositorySchema()


@router.route("", methods=["GET"])
def list_repositories() -> Tuple[Any, int]:
    """Get repositories.

    ---
    get:
      description: Get repositories
      responses:
        200:
          description: Get repositories
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Repository'
    """
    with generate_session() as session:
        raw_repositories = repositories_crud.get_entities(session)
        repositories = [schema.dump(repository) for repository in raw_repositories]
    result = {"result": repositories}
    return jsonify(result), 200


@router.route("/team/<team_id>", methods=["GET"])
def list_repositories_for_team(team_id: str) -> Tuple[Any, int]:
    """Get repositories for a given team id.

    ---
    get:
      description: Get repositories belonging to a team
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team to get repositories for
      responses:
        200:
          description: Get repositories belonging to a team
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Repository'
        404:
          description: Team not found
    """
    with generate_session() as session:
        try:
            raw_repositories = repositories_crud.get_entities_for_team(
                session, get_sanitized_id(team_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        repositories = [schema.dump(repository) for repository in raw_repositories]
    result = {"result": repositories}
    return jsonify(result), 200


@router.route("/<repo_id>", methods=["GET"])
def get_repository(repo_id: str) -> Tuple[Any, int]:
    """Get repository by id.

    ---
    get:
      description: Get single repository by id
      parameters:
        - in: path
          name: repo_id
          schema:
            type: integer
          required: true
          description: ID of the repository
      responses:
        200:
          description: Get single repository by id
          content:
            application/json:
              schema: RepositorySchema
        404:
          description: Repository not found
    """
    with generate_session() as session:
        try:
            raw_repository = repositories_crud.get_entity(
                session, get_sanitized_id(repo_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_repository)
    return jsonify(result), 200
