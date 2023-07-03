"""Project routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import projects_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v1 import ProjectV1Schema
from app.security import get_sanitized_id

schema = ProjectV1Schema()


def list_projects() -> Tuple[Any, int]:
    """Get projects.

    ---
    get:
      description: Get projects
      responses:
        200:
          description: Get projects
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/ProjectV1'
    """
    with generate_session() as session:
        raw_projects = projects_crud.get_entities(session)
        projects = [schema.dump(project) for project in raw_projects]
    result = {"result": projects}
    return jsonify(result), 200


@requires_security([requires_admin, requires_team_access])
def list_projects_for_team(team_id: str) -> Tuple[Any, int]:
    """Get projects for a given team id.

    ---
    get:
      description: Get projects belonging to a team or team view
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team or team view to get projects for
      responses:
        200:
          description: Get projects belonging to a team or team view
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/ProjectV1'
        404:
          description: Team or team view not found
    """
    with generate_session() as session:
        try:
            raw_projects = projects_crud.get_entities_for_team(
                session, get_sanitized_id(team_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        projects = [schema.dump(project) for project in raw_projects]
    result = {"result": projects}
    return jsonify(result), 200


def get_project(project_id: str) -> Tuple[Any, int]:
    """Get project by id.

    ---
    get:
      description: Get single project by id
      parameters:
        - in: path
          name: project_id
          schema:
            type: integer
          required: true
          description: ID of the project
      responses:
        200:
          description: Get single project by id
          content:
            application/json:
              schema: ProjectV1Schema
        404:
          description: Project not found
    """
    with generate_session() as session:
        try:
            raw_project = projects_crud.get_entity(
                session, get_sanitized_id(project_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_project)
    return jsonify(result), 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("projects", __name__, url_prefix="/projects")
    router.route("", methods=["GET"])(list_projects)
    router.route("/team/<team_id>", methods=["GET"])(list_projects_for_team)
    router.route("/<project_id>", methods=["GET"])(get_project)
    return router
