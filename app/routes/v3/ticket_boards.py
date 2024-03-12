"""TicketBoard routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from app.crud import ticket_boards_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security, requires_team_access
from app.schemas.v3 import TicketBoardV3Schema
from app.security import get_sanitized_id
from app.utils.pagination import get_pagination_info, set_pagination_header

schema = TicketBoardV3Schema()


def list_ticket_boards() -> Tuple[Any, int]:
    """Get ticket_boards.

    ---
    get:
      description: Get ticket boards
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
          description: Get ticket boards
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/TicketBoardV3'
    """
    with generate_session() as session:
        page_info = get_pagination_info(
            request.args, ticket_boards_crud.get_count(session)
        )
        raw_ticket_boards = ticket_boards_crud.get_entities_paginated(
            session, limit=page_info.limit, offset=page_info.offset
        )  # type: ignore
        ticket_boards = [schema.dump(board) for board in raw_ticket_boards]
    result = {"result": ticket_boards}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
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
          description: Get ticket boards belonging to a team or team view
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/TicketBoardV3'
        404:
          description: Team or team view not found
    """
    db_id = get_sanitized_id(team_id)
    with generate_session() as session:
        try:
            page_info = get_pagination_info(
                request.args, ticket_boards_crud.get_count_for_team(session, db_id)
            )
            raw_ticket_boards = ticket_boards_crud.get_entities_for_team_paginated(
                session, db_id, limit=page_info.limit, offset=page_info.offset
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        ticket_boards = [schema.dump(board) for board in raw_ticket_boards]
    result = {"result": ticket_boards}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


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
              schema: TicketBoardV3Schema
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
    response = jsonify(result)
    return response, 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("ticketboards", __name__, url_prefix="/ticketboards")
    router.route("", methods=["GET"])(list_ticket_boards)
    router.route("/team/<team_id>", methods=["GET"])(list_ticket_boards_for_team)
    router.route("/<board_id>", methods=["GET"])(get_ticket_board)
    return router
