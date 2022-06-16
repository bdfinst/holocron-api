"""Repository routes."""
from flask import Blueprint, jsonify

from app.crud import repositories_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import RepositorySchema

router = Blueprint("repositories", __name__, url_prefix="/repositories")

schema = RepositorySchema()


@router.route("", methods=["GET"])
def list_repositories():
    """Get repositories.

    ---
    get:
      description: Get repositories
      responses:
        200:
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


@router.route("/team/<id_>", methods=["GET"])
def list_repositories_for_team(id_: int):
    """Get repositories for a given team id.

    ---
    get:
      description: Get repositories belonging to a team
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the team to get repositories for
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Repository'
        404:
          content:
            text/plain:
              schema: string
    """
    with generate_session() as session:
        try:
            raw_repositories = repositories_crud.get_entities_for_team(session, id_)
        except HolocronIntegrityError:
            return "Resource not found", 404
        repositories = [schema.dump(repository) for repository in raw_repositories]
    result = {"result": repositories}
    return jsonify(result), 200


@router.route("/<id_>", methods=["GET"])
def get_repository(id_: int):
    """Get repository by id.

    ---
    get:
      description: Get single repository by id
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the repository
      responses:
        200:
          content:
            application/json:
              schema: RepositorySchema
        404:
          content:
            text/plain:
              schema: string
    """
    with generate_session() as session:
        try:
            raw_repository = repositories_crud.get_entity(session, id_)
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_repository)
    return jsonify(result), 200
