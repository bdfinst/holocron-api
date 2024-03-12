"""ProjectIssue routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from app.crud import project_issues_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v3 import ProjectIssueV3Schema
from app.security import get_sanitized_id
from app.utils.pagination import get_pagination_info, set_pagination_header

schema = ProjectIssueV3Schema()


@requires_security([requires_admin, requires_team_access])
def list_project_issues_for_team(team_id: str) -> Tuple[Any, int]:
    """Get project issues for a given team id.

    ---
    get:
      description: Get project_issues belonging to a team or team view
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team or team view to get project_issues for
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
          description: Get project_issues belonging to a team or team view
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/ProjectIssueV3'
        404:
          description: Team or team view not found
    """
    db_id = get_sanitized_id(team_id)
    with generate_session() as session:
        try:
            page_info = get_pagination_info(
                request.args, project_issues_crud.get_count_for_team(session, db_id)
            )
            raw_project_issues = project_issues_crud.get_entities_for_team_paginated(
                session, db_id, limit=page_info.limit, offset=page_info.offset
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        project_issue_models = [
            schema.dump(project_issue) for project_issue in raw_project_issues
        ]
    result = {"result": project_issue_models}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


@requires_security([requires_admin])
def get_project_issue(project_issue_id: str) -> Tuple[Any, int]:
    """Get project issue by id.

    ---
    get:
      description: Get single project_issue by id
      parameters:
        - in: path
          name: project_issue_id
          schema:
            type: integer
          required: true
          description: ID of the project_issue
      responses:
        200:
          description: Get single project_issue by id
          content:
            application/json:
              schema: ProjectIssueV3Schema
        404:
          description: ProjectIssue not found
    """
    with generate_session() as session:
        try:
            raw_project_issue = project_issues_crud.get_entity(
                session, get_sanitized_id(project_issue_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_project_issue)
    response = jsonify(result)
    return response, 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("project-issues", __name__, url_prefix="/project-issues")
    router.route("/team/<team_id>", methods=["GET"])(list_project_issues_for_team)
    router.route("/<project_issue_id>", methods=["GET"])(get_project_issue)
    return router
