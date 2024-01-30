"""Repository routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import repositories_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v2 import RepositoryV2Schema
from app.security import get_sanitized_id

schema = RepositoryV2Schema()


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
                      $ref: '#/components/schemas/RepositoryV2'
    """
    with generate_session() as session:
        raw_repositories = repositories_crud.get_entities(session)
        repositories = [schema.dump(repository) for repository in raw_repositories]
    result = {"result": repositories}
    return jsonify(result), 200


@requires_security([requires_admin, requires_team_access])
def list_repositories_for_team(team_id: str) -> Tuple[Any, int]:
    """Get repositories for a given team id.

    ---
    get:
      description: Get repositories belonging to a team or team view
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team or team view to get repositories for
      responses:
        200:
          description: Get repositories belonging to a team or team view
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/RepositoryV2'
        404:
          description: Team or team view not found
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
              schema: RepositoryV2Schema
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


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("repositories", __name__, url_prefix="/repositories")
    router.route("", methods=["GET"])(list_repositories)
    router.route("/team/<team_id>", methods=["GET"])(list_repositories_for_team)
    router.route("/<repo_id>", methods=["GET"])(get_repository)
    return router
