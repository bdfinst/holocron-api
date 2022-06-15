"""TicketBoard routes."""
from flask import Blueprint, jsonify

from app.crud import ticket_boards_crud
from app.database import generate_session
from app.schemas import TicketBoardSchema

router = Blueprint("ticketboards", __name__, url_prefix="/ticketboards")

schema = TicketBoardSchema()


@router.route("", methods=["GET"])
def list_ticket_boards():
    """Get ticket_boards.

    ---
    get:
      description: Get ticket_boards
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/TicketBoard'
    """
    with generate_session() as session:
        raw_ticket_boards = ticket_boards_crud.get_entities(session)
        ticket_boards = [schema.dump(board) for board in raw_ticket_boards]
    result = {"result": ticket_boards}
    return jsonify(result), 200


@router.route("/team/<id_>", methods=["GET"])
def list_ticket_boards_for_team(id_: int):
    """Get ticket_boards for a given team id.

    ---
    get:
      description: Get ticket_boards belonging to a team
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the team to get ticket_boards for
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/TicketBoard'
    """
    with generate_session() as session:
        raw_ticket_boards = ticket_boards_crud.get_entities_for_team(session, id_)
        ticket_boards = [schema.dump(board) for board in raw_ticket_boards]
    result = {"result": ticket_boards}
    return jsonify(result), 200


@router.route("/<id_>", methods=["GET"])
def get_ticket_board(id_: int):
    """Get ticket_board by id.

    ---
    get:
      description: Get single ticket_board by id
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the ticket_board
      responses:
        200:
          content:
            application/json:
              schema: TicketBoardSchema
    """
    with generate_session() as session:
        raw_ticket_board = ticket_boards_crud.get_entity(session, id_)
        result = schema.dump(raw_ticket_board)
    return jsonify(result), 200
