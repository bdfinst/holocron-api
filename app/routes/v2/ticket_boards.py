"""TicketBoard routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import ticket_boards_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v2 import TicketBoardV2Schema
from app.security import get_sanitized_id

schema = TicketBoardV2Schema()


def list_ticket_boards() -> Tuple[Any, int]:
    """Get ticket_boards.

    ---
    get:
      description: Get ticket boards
      responses:
        200:
          description: Get ticket boards
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/TicketBoardV2'
    """
    with generate_session() as session:
        raw_ticket_boards = ticket_boards_crud.get_entities(session)
        ticket_boards = [schema.dump(board) for board in raw_ticket_boards]
    result = {"result": ticket_boards}
    return jsonify(result), 200


@requires_security([requires_admin, requires_team_access])
def list_ticket_boards_for_team(team_id: str) -> Tuple[Any, int]:
    """Get ticket_boards for a given team id.

    ---
    get:
      description: Get ticket boards belonging to a team or team view
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team or team view to get ticket_boards for
      responses:
        200:
          description: Get ticket boards belonging to a team or team view
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/TicketBoardV2'
        404:
          description: Team or team view not found
    """
    with generate_session() as session:
        try:
            raw_ticket_boards = ticket_boards_crud.get_entities_for_team(
                session, get_sanitized_id(team_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        ticket_boards = [schema.dump(board) for board in raw_ticket_boards]
    result = {"result": ticket_boards}
    return jsonify(result), 200


def get_ticket_board(board_id: str) -> Tuple[Any, int]:
    """Get ticket_board by id.

    ---
    get:
      description: Get single ticket board by id
      parameters:
        - in: path
          name: board_id
          schema:
            type: integer
          required: true
          description: ID of the ticket_board
      responses:
        200:
          description: Get single ticket board by id
          content:
            application/json:
              schema: TicketBoardV2Schema
        404:
          description: Ticket board not found
    """
    with generate_session() as session:
        try:
            raw_ticket_board = ticket_boards_crud.get_entity(
                session, get_sanitized_id(board_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_ticket_board)
    return jsonify(result), 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("ticketboards", __name__, url_prefix="/ticketboards")
    router.route("", methods=["GET"])(list_ticket_boards)
    router.route("/team/<team_id>", methods=["GET"])(list_ticket_boards_for_team)
    router.route("/<board_id>", methods=["GET"])(get_ticket_board)
    return router
