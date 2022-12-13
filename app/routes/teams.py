"""Team routes."""
from typing import Any

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud.team_history import team_history_crud
from app.crud.teams import teams_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin_or_member
from app.models import Team
from app.schemas import TeamSchema
from app.security import MALFORMED_REQ_PARAMS_MSG, get_sanitized_id, log_security_event

router = Blueprint("teams", __name__, url_prefix="/teams")

schema = TeamSchema()


@router.route("", methods=["GET"])
def list_teams():
    """List teams route.

    ---
    get:
      description: List teams
      responses:
        200:
          description: List teams
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/ExistingTeam'
    """
    with generate_session() as session:
        raw_teams = teams_crud.get_entities(session)
        teams = [schema.dump(team) for team in raw_teams]
    result = {"result": teams}
    return jsonify(result), 200


@router.route("", methods=["POST"])
def create_team():
    """Create team route.

    ---
    post:
      description: Create team
      requestBody:
        content:
          application/json:
            schema: NewTeamSchema
      responses:
        201:
          description: The team was successfully created
          content:
            application/json:
              schema: ExistingTeamSchema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorSchema
    """
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_team: Team = teams_crud.create_entity(session, data)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result: dict[str, Any] = schema.dump(raw_team)

        try:
            team_history_crud.create_entity(session, raw_team)
        except HolocronIntegrityError as err:
            return err.messages, 400

    return jsonify(result), 201


@router.route("/<team_id>", methods=["GET"])
def get_team(team_id: str):
    """Get team by id route.

    ---
    get:
      description: Get team
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team
      responses:
        200:
          description: Get team
          content:
            application/json:
              schema: ExistingTeamSchema
        404:
          description: Team not found
    """
    with generate_session() as session:
        try:
            raw_team = teams_crud.get_entity(session, get_sanitized_id(team_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_team)
    return jsonify(result), 200


@router.route("/<team_id>", methods=["PUT"])
@requires_admin_or_member
def update_team(team_id: str):
    """Update team route.

    ---
    put:
      description: Update team
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
            schema: NewTeamSchema
      responses:
        200:
          description: The team was successfully updated
          content:
            application/json:
              schema: ExistingTeamSchema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorSchema
    """
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:

        db_team_id = get_sanitized_id(team_id)

        old_team_data = teams_crud.get_entity(session, db_team_id)

        try:
            raw_team = teams_crud.update_entity(session, data, db_team_id)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_team)

        if raw_team.team_size != old_team_data.team_size:
            try:
                team_history_crud.create_entity(session, raw_team)
            except HolocronIntegrityError as err:
                return err.messages, 400

    return jsonify(result), 200


@router.route("/<team_id>", methods=["DELETE"])
@requires_admin_or_member
def delete_team(team_id: str):
    """Delete team route.

    ---
    delete:
      description: Delete team
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team
      responses:
        204:
          description: The team was successfully deleted
    """
    with generate_session() as session:
        teams_crud.delete_entity(session, get_sanitized_id(team_id))
    return "", 204
