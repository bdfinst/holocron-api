"""Member routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud import members_crud, teams_crud, teams_members_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v3 import MemberV3Schema, TeamMemberV3Schema, TeamV3Schema
from app.security import MALFORMED_REQ_PARAMS_MSG, get_sanitized_id, log_security_event
from app.utils.pagination import get_pagination_info, set_pagination_header

member_schema = MemberV3Schema()
team_member_schema = TeamMemberV3Schema()
team_schema = TeamV3Schema()


@requires_security([requires_admin])
def list_members() -> Tuple[Any, int]:
    """List members route.

    ---
    get:
      description: List members
      responses:
        200:
          description: List members
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/MemberV3'
    """
    with generate_session() as session:
        page_info = get_pagination_info(request.args, members_crud.get_count(session))
        raw_members = members_crud.get_entities_paginated(
            session, offset=page_info.offset, limit=page_info.limit
        )
        members = [member_schema.dump(member) for member in raw_members]
    result = {"result": members}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


@requires_security([requires_admin])
def get_member(member_id: str) -> Tuple[Any, int]:
    """Get member by id.

    ---
    get:
      description: Get single member by id
      parameters:
        - in: path
          name: member_id
          schema:
            type: integer
          required: true
          description: ID of the member
      responses:
        200:
          description: Get single member by id
          content:
            application/json:
              schema: MemberV3Schema
        404:
          description: Member not found
    """
    with generate_session() as session:
        try:
            raw_member = members_crud.get_entity(session, get_sanitized_id(member_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = member_schema.dump(raw_member)
    response = jsonify(result)
    return response, 200


@requires_security([requires_admin, requires_team_access])
def update_team_members(team_id: str) -> Tuple[Any, int]:
    """Update members of team.

    ---
    put:
      description: Update members of team
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team
      requestBody:
        content:
          application/json:
            schema:
              properties:
                teamMembers:
                  type: array
                  items:
                    $ref: '#/components/schemas/TeamMemberV3'
      responses:
        200:
          description: Update members of team
          content:
            application/json:
              schema: ExistingTeamV3
        404:
          description: Team not found
    """
    try:
        json_items = [] if request.json is None else request.json["teamMembers"]
        data = [team_member_schema.load(item) for item in json_items]
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        database_id = get_sanitized_id(team_id)
        try:
            teams_members_crud.create_entities(session, data, database_id)
            raw_team = teams_crud.get_entity(session, database_id)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = team_schema.dump(raw_team)
    response = jsonify(result)
    return response, 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("members", __name__, url_prefix="/members")
    router.route("", methods=["GET"])(list_members)
    router.route("/<member_id>", methods=["GET"])(get_member)
    router.route("/team/<team_id>", methods=["PUT"])(update_team_members)
    return router
