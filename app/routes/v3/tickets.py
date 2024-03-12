"""Ticket routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from app.crud import tickets_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v3 import TicketV3Schema
from app.security import get_sanitized_id
from app.utils.pagination import get_pagination_info, set_pagination_header

schema = TicketV3Schema()


@requires_security([requires_admin, requires_team_access])
def list_tickets_for_team(team_id: str) -> Tuple[Any, int]:
    """Get tickets for a given team id.

    ---
    get:
      description: Get tickets belonging to a team or team view
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team or team view to get tickets for
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
          description: Get tickets belonging to a team or team view
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/TicketV3'
        404:
          description: Team or team view not found
    """
    db_id = get_sanitized_id(team_id)
    with generate_session() as session:
        try:
            page_info = get_pagination_info(
                request.args, tickets_crud.get_count_for_team(session, db_id)
            )
            raw_tickets = tickets_crud.get_entities_for_team_paginated(
                session, db_id, limit=page_info.limit, offset=page_info.offset
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        tickets = [schema.dump(ticket) for ticket in raw_tickets]
    result = {"result": tickets}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


@requires_security([requires_admin])
def get_ticket(ticket_id: str) -> Tuple[Any, int]:
    """Get ticket by id.

    ---
    get:
      description: Get single ticket by id
      parameters:
        - in: path
          name: ticket_id
          schema:
            type: integer
          required: true
          description: ID of the ticket
      responses:
        200:
          description: Get single ticket by id
          content:
            application/json:
              schema: TicketV3Schema
        404:
          description: Ticket not found
    """
    with generate_session() as session:
        try:
            raw_ticket = tickets_crud.get_entity(session, get_sanitized_id(ticket_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_ticket)
    response = jsonify(result)
    return response, 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("tickets", __name__, url_prefix="/tickets")
    router.route("/team/<team_id>", methods=["GET"])(list_tickets_for_team)
    router.route("/<ticket_id>", methods=["GET"])(get_ticket)
    return router
