"""Team routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.config import FEATURE_FLAGS
from app.crud.team_history import team_history_crud
from app.crud.team_views import team_views_crud
from app.crud.teams import teams_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import (
    requires_admin,
    requires_security,
    requires_team_access,
    requires_valid_team_data,
    requires_valid_team_view_data,
    requires_vs_access,
)
from app.schemas.v3 import TeamV3Schema, TeamViewV3Schema
from app.security import MALFORMED_REQ_PARAMS_MSG, get_sanitized_id, log_security_event
from app.utils.pagination import get_pagination_info, set_pagination_header

schema = TeamV3Schema()
schema_view = TeamViewV3Schema()


def list_teams() -> Tuple[Any, int]:
    """List teams route.

    ---
    get:
      description: List teams
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
          description: List teams
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/ExistingTeamV3'
    """
    with generate_session() as session:
        page_info = get_pagination_info(request.args, teams_crud.get_count(session))
        raw_teams = (
            teams_crud.get_entities_without_team_views_paginated(
                session, limit=page_info.limit, offset=page_info.offset
            )
            if FEATURE_FLAGS["FEATURE_TEAM_VIEWS"]
            else teams_crud.get_entities_paginated(
                session, limit=page_info.limit, offset=page_info.offset
            )
        )
        teams = [schema.dump(team) for team in raw_teams]
    result = {"result": teams}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return jsonify(result), 200


@requires_security([requires_admin, requires_vs_access])
@requires_valid_team_data
def create_team() -> Tuple[Any, int]:
    """Create team route.

    ---
    post:
      description: Create team
      requestBody:
        content:
          application/json:
            schema: NewTeamV3Schema
      responses:
        201:
          description: The team was successfully created
          content:
            application/json:
              schema: ExistingTeamV3Schema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorV2Schema
    """
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_team = teams_crud.create_entity(session, data)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_team)

        try:
            team_history_crud.create_entity(session, raw_team)
        except HolocronIntegrityError as err:
            return err.messages, 400

    response = jsonify(result)
    return response, 201


def get_team(team_id: str) -> Tuple[Any, int]:
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
              schema: ExistingTeamV3Schema
        404:
          description: Team not found
    """
    with generate_session() as session:
        try:
            raw_team = (
                teams_crud.get_entity_no_team_view(session, get_sanitized_id(team_id))
                if FEATURE_FLAGS["FEATURE_TEAM_VIEWS"]
                else teams_crud.get_entity(session, get_sanitized_id(team_id))
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_team)
    response = jsonify(result)
    return response, 200


@requires_security([requires_admin, requires_team_access])
@requires_valid_team_data
def update_team(team_id: str) -> Tuple[Any, int]:
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
            schema: NewTeamV3Schema
      responses:
        200:
          description: The team was successfully updated
          content:
            application/json:
              schema: ExistingTeamV3Schema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorV2Schema
    """
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        db_team_id = get_sanitized_id(team_id)

        try:
            old_team_data = teams_crud.get_entity(session, db_team_id)
            old_team_team_size = old_team_data.team_size
            raw_team = teams_crud.update_entity(session, data, db_team_id)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_team)

        if raw_team.team_size != old_team_team_size:
            try:
                team_history_crud.create_entity(session, raw_team)
            except HolocronIntegrityError as err:
                return err.messages, 400

    response = jsonify(result)
    return response, 200


@requires_security([requires_admin, requires_team_access])
def delete_team(team_id: str) -> Tuple[Any, int]:
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


def list_team_views() -> Tuple[Any, int]:
    """List team views route.

    ---
    get:
      description: List team views
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
          description: List team views
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/ExistingTeamViewV3'
    """
    with generate_session() as session:
        page_info = get_pagination_info(
            request.args, team_views_crud.get_count(session)
        )
        raw_teams = team_views_crud.get_entities_paginated(
            session, limit=page_info.limit, offset=page_info.offset
        )
        teams = [schema_view.dump(team) for team in raw_teams]
    result = {"result": teams}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


@requires_security([requires_admin, requires_team_access])
@requires_valid_team_view_data
def create_team_view() -> Tuple[Any, int]:
    """Create team view route.

    ---
    post:
      description: Create team view
      requestBody:
        content:
          application/json:
            schema: NewTeamViewV3Schema
      responses:
        201:
          description: The team view was successfully created
          content:
            application/json:
              schema: ExistingTeamViewV3Schema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorV2Schema
    """
    try:
        data = schema_view.load(request.json)
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_team_view = team_views_crud.create_entity(session, data)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema_view.dump(raw_team_view)

    response = jsonify(result)
    return response, 201


def get_team_view(team_view_id: str) -> Tuple[Any, int]:
    """Get team view by id route.

    ---
    get:
      description: Get team view
      parameters:
        - in: path
          name: team_view_id
          schema:
            type: integer
          required: true
          description: ID of the team view
      responses:
        200:
          description: Get team view
          content:
            application/json:
              schema: ExistingTeamViewV3Schema
        404:
          description: Team not found
    """
    with generate_session() as session:
        try:
            raw_team_view = team_views_crud.get_entity(
                session, get_sanitized_id(team_view_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema_view.dump(raw_team_view)
    response = jsonify(result)
    return response, 200


@requires_security([requires_admin, requires_team_access])
@requires_valid_team_view_data
def update_team_view(team_view_id: str) -> Tuple[Any, int]:
    """Update team route.

    ---
    put:
      description: Update team view
      parameters:
        - in: path
          name: team_view_id
          schema:
            type: integer
          required: true
          description: ID of the team view
      requestBody:
        content:
          application/json:
            schema: NewTeamViewV3Schema
      responses:
        200:
          description: The team view was successfully updated
          content:
            application/json:
              schema: ExistingTeamViewV3Schema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorV2Schema
    """
    try:
        data = schema_view.load(request.json)
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        db_team_view_id = get_sanitized_id(team_view_id)
        try:
            raw_team_view = team_views_crud.update_entity(
                session, data, db_team_view_id
            )
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema_view.dump(raw_team_view)
    response = jsonify(result)
    return response, 200


@requires_security([requires_admin, requires_team_access])
def delete_team_view(team_view_id: str) -> Tuple[Any, int]:
    """Delete team route.

    ---
    delete:
      description: Delete team view
      parameters:
        - in: path
          name: team_view_id
          schema:
            type: integer
          required: true
          description: ID of the team view
      responses:
        204:
          description: The team was successfully deleted
    """
    with generate_session() as session:
        team_views_crud.delete_entity(session, get_sanitized_id(team_view_id))
    return "", 204


def create_router() -> Blueprint:
    """Router factory."""
    team_id_route = "/<team_id>"
    router = Blueprint("teams", __name__, url_prefix="/teams")
    router.route("", methods=["GET"])(list_teams)
    router.route("", methods=["POST"])(create_team)
    router.route(team_id_route, methods=["GET"])(get_team)
    router.route(team_id_route, methods=["PUT"])(update_team)
    router.route(team_id_route, methods=["DELETE"])(delete_team)

    if FEATURE_FLAGS["FEATURE_TEAM_VIEWS"]:
        team_view_id_route = "/views/<team_view_id>"
        router.route("/views", methods=["GET"])(list_team_views)
        router.route("/views", methods=["POST"])(create_team_view)
        router.route(team_view_id_route, methods=["GET"])(get_team_view)
        router.route(team_view_id_route, methods=["PUT"])(update_team_view)
        router.route(team_view_id_route, methods=["DELETE"])(delete_team_view)
    return router
