"""GitRequest routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from app.crud import git_requests_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v2 import GitRequestV2Schema
from app.security import get_sanitized_id
from app.utils.pagination import construct_next_page_url, get_limit_offset_page

schema = GitRequestV2Schema()


@requires_security([requires_admin, requires_team_access])
def list_git_requests_for_team(team_id: str) -> Tuple[Any, int]:
    """Get git requests for a given team id.

    ---
    get:
      description: Get git requests belonging to a team or team view
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team or team view to get git requests for
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
          description: Get git requests belonging to a team or team view
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/GitRequestV2'
        404:
          description: Team or team view not found
    """
    limit, offset, page = get_limit_offset_page(request.args)
    db_id = get_sanitized_id(team_id)
    with generate_session() as session:
        try:
            count = git_requests_crud.get_count_for_team(session, db_id)
            raw_git_requests = git_requests_crud.get_entities_for_team_paginated(
                session, db_id, offset=offset, limit=limit
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        git_requests = [schema.dump(commit) for commit in raw_git_requests]
    result = {"result": git_requests}
    response = jsonify(result)
    response.headers["next-page"] = construct_next_page_url(
        request.url, limit, offset, page, count
    )  # type: ignore
    return response, 200


@requires_security([requires_admin])
def get_git_request(git_request_id: str) -> Tuple[Any, int]:
    """Get git request by id.

    ---
    get:
      description: Get single git request by id
      parameters:
        - in: path
          name: git_request_id
          schema:
            type: integer
          required: true
          description: ID of the git request
      responses:
        200:
          description: Get single git request by id
          content:
            application/json:
              schema: GitRequestV2Schema
        404:
          description: Git request not found
    """
    with generate_session() as session:
        try:
            raw_git_request = git_requests_crud.get_entity(
                session, get_sanitized_id(git_request_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_git_request)
    response = jsonify(result)
    return response, 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("git-requests", __name__, url_prefix="/git-requests")
    router.route("/team/<team_id>", methods=["GET"])(list_git_requests_for_team)
    router.route("/<git_request_id>", methods=["GET"])(get_git_request)
    return router
