"""Ticket routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import tickets_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v1 import TicketV1Schema
from app.security import get_sanitized_id

schema = TicketV1Schema()


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
                      $ref: '#/components/schemas/TicketV1'
        404:
          description: Team or team view not found
    """
    with generate_session() as session:
        try:
            raw_tickets = tickets_crud.get_entities_for_team(
                session, get_sanitized_id(team_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        tickets = [schema.dump(ticket) for ticket in raw_tickets]
    result = {"result": tickets}
    return jsonify(result), 200


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
              schema: TicketV1Schema
        404:
          description: Ticket not found
    """
    with generate_session() as session:
        try:
            raw_ticket = tickets_crud.get_entity(session, get_sanitized_id(ticket_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_ticket)
    return jsonify(result), 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("tickets", __name__, url_prefix="/tickets")
    router.route("/team/<team_id>", methods=["GET"])(list_tickets_for_team)
    router.route("/<ticket_id>", methods=["GET"])(get_ticket)
    return router
