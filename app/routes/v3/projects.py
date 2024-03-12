"""Project routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from app.crud import projects_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v3 import ProjectV3Schema
from app.security import get_sanitized_id
from app.utils.pagination import get_pagination_info, set_pagination_header

schema = ProjectV3Schema()


def list_projects() -> Tuple[Any, int]:
    """Get projects.

    ---
    get:
      description: Get projects
      parameters:
        - in: query
          name: per_page
          schema:
            type: integer
          required: false
          description: The maximum number of items to return
        - in: query
          name: page
          schema:
            type: integer
          required: false
          description: The page of the data set to retrieve
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
                      $ref: '#/components/schemas/ProjectV3'
    """
    with generate_session() as session:
        page_info = get_pagination_info(request.args, projects_crud.get_count(session))
        raw_projects = projects_crud.get_entities_paginated(
            session, limit=page_info.limit, offset=page_info.offset
        )
        projects = [schema.dump(project) for project in raw_projects]
    result = {"result": projects}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


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
        - in: query
          name: per_page
          schema:
            type: integer
          required: false
          description: The maximum number of items to return
        - in: query
          name: page
          schema:
            type: integer
          required: false
          description: The page of the data set to retrieve
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
                      $ref: '#/components/schemas/ProjectV3'
        404:
          description: Team or team view not found
    """
    db_id = get_sanitized_id(team_id)
    with generate_session() as session:
        try:
            page_info = get_pagination_info(
                request.args, projects_crud.get_count_for_team(session, db_id)
            )
            raw_projects = projects_crud.get_entities_for_team_paginated(
                session, db_id, limit=page_info.limit, offset=page_info.offset
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        projects = [schema.dump(project) for project in raw_projects]
    result = {"result": projects}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


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
              schema: ProjectV3Schema
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
    response = jsonify(result)
    return response, 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("projects", __name__, url_prefix="/projects")
    router.route("", methods=["GET"])(list_projects)
    router.route("/team/<team_id>", methods=["GET"])(list_projects_for_team)
    router.route("/<project_id>", methods=["GET"])(get_project)
    return router
