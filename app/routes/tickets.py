"""Ticket routes."""
from flask import Blueprint, jsonify

from app.crud import tickets_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import TicketSchema

router = Blueprint("tickets", __name__, url_prefix="/tickets")

schema = TicketSchema()


@router.route("/team/<id_>", methods=["GET"])
def list_tickets_for_team(id_: int):
    """Get tickets for a given team id.

    ---
    get:
      description: Get tickets belonging to a team
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the team to get tickets for
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Ticket'
        404:
          content:
            text/plain:
              schema: string
    """
    with generate_session() as session:
        try:
            raw_tickets = tickets_crud.get_entities_for_team(session, id_)
        except HolocronIntegrityError:
            return "Resource not found", 404
        tickets = [schema.dump(ticket) for ticket in raw_tickets]
    result = {"result": tickets}
    return jsonify(result), 200


@router.route("/<id_>", methods=["GET"])
def get_ticket(id_: int):
    """Get ticket by id.

    ---
    get:
      description: Get single ticket by id
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the ticket
      responses:
        200:
          content:
            application/json:
              schema: TicketSchema
        404:
          content:
            text/plain:
              schema: string
    """
    with generate_session() as session:
        try:
            raw_ticket = tickets_crud.get_entity(session, id_)
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_ticket)
    return jsonify(result), 200
