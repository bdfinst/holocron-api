"""Project routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from app.crud import projects_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v2 import ProjectV2Schema
from app.security import get_sanitized_id
from app.utils.pagination import construct_next_page_url, get_limit_offset_page

schema = ProjectV2Schema()


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
                      $ref: '#/components/schemas/ProjectV2'
    """
    limit, offset, page = get_limit_offset_page(request.args)
    with generate_session() as session:
        count = projects_crud.get_count(session)
        raw_projects = projects_crud.get_entities_paginated(
            session, limit=limit, offset=offset
        )
        projects = [schema.dump(project) for project in raw_projects]
    result = {"result": projects}
    response = jsonify(result)
    response.headers["next-page"] = construct_next_page_url(
        request.url, limit, offset, page, count
    )  # type: ignore
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
                      $ref: '#/components/schemas/ProjectV2'
        404:
          description: Team or team view not found
    """
    limit, offset, page = get_limit_offset_page(request.args)
    db_id = get_sanitized_id(team_id)
    with generate_session() as session:
        try:
            count = projects_crud.get_count_for_team(session, db_id)
            raw_projects = projects_crud.get_entities_for_team_paginated(
                session, db_id, limit=limit, offset=offset
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        projects = [schema.dump(project) for project in raw_projects]
    result = {"result": projects}
    response = jsonify(result)
    response.headers["next-page"] = construct_next_page_url(
        request.url, limit, offset, page, count
    )  # type: ignore
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
              schema: ProjectV2Schema
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
