"""Branch routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from app.crud import branches_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v2 import BranchV2Schema
from app.security import get_sanitized_id
from app.utils.pagination import get_pagination_info, set_pagination_header

schema = BranchV2Schema()


@requires_security([requires_admin, requires_team_access])
def list_branches_for_team(team_id: str) -> Tuple[Any, int]:
    """Get branches for a given team id.

    ---
    get:
      description: Get branches belonging to a team
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team or team view to get branches for
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
          description: Get branches belonging to a team or team view
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/BranchV2'
        404:
          description: Team or team view not found
    """
    db_id = get_sanitized_id(team_id)
    with generate_session() as session:
        try:
            page_info = get_pagination_info(
                request.args, branches_crud.get_count_for_team(session, db_id)
            )
            raw_branches = branches_crud.get_entities_for_team_paginated(
                session, db_id, offset=page_info.offset, limit=page_info.limit
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        branches = [schema.dump(branch) for branch in raw_branches]
    result = {"result": branches}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


@requires_security([requires_admin])
def get_branch(branch_id: str) -> Tuple[Any, int]:
    """Get branch by id.

    ---
    get:
      description: Get single branch by id
      parameters:
        - in: path
          name: branch_id
          schema:
            type: integer
          required: true
          description: ID of the branch
      responses:
        200:
          description: Get single branch by id
          content:
            application/json:
              schema: BranchV2Schema
        404:
          description: Branch not found
    """
    with generate_session() as session:
        try:
            raw_branch = branches_crud.get_entity(session, get_sanitized_id(branch_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_branch)
    response = jsonify(result)
    return response, 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("branches", __name__, url_prefix="/branches")
    router.route("/team/<team_id>", methods=["GET"])(list_branches_for_team)
    router.route("/<branch_id>", methods=["GET"])(get_branch)
    return router
