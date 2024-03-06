"""Valuestream routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.config import FEATURE_FLAGS
from app.crud import valuestreams_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import (
    requires_admin,
    requires_org_access,
    requires_security,
    requires_vs_access,
)
from app.schemas.v2 import ValuestreamV2Schema
from app.security import MALFORMED_REQ_PARAMS_MSG, get_sanitized_id, log_security_event
from app.utils.pagination import construct_next_page_url, get_limit_offset_page

schema = ValuestreamV2Schema()


def list_valuestreams() -> Tuple[Any, int]:
    """List valuestreams route.

    ---
    get:
      description: List valuestreams
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
          description: List valuestreams
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/ExistingValuestreamV2'
    """
    limit, offset, page = get_limit_offset_page(request.args)
    with generate_session() as session:
        count = valuestreams_crud.get_count(session)
        raw_valuestreams = (
            valuestreams_crud.get_entities_without_team_views_paginated(
                session, limit=limit, offset=offset
            )
            if FEATURE_FLAGS["FEATURE_TEAM_VIEWS"]
            else valuestreams_crud.get_entities_paginated(
                session, limit=limit, offset=offset
            )
        )
        valuestreams = [schema.dump(valuestream) for valuestream in raw_valuestreams]
    result = {"result": valuestreams}
    response = jsonify(result)
    response.headers["next-page"] = construct_next_page_url(
        request.url, limit, offset, page, count
    )  # type: ignore
    return response, 200


@requires_security([requires_admin, requires_org_access])
def create_valuestream() -> Tuple[Any, int]:
    """Create valuestream route.

    ---
    post:
      description: Create valuestream
      requestBody:
        content:
          application/json:
            schema: NewValuestreamV2Schema
      responses:
        201:
          description: The valuestream was successfully created
          content:
            application/json:
              schema: ExistingValuestreamV2Schema
        400:
          description: Failure due to invalid request
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
            raw_valuestream = valuestreams_crud.create_entity(session, data)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_valuestream)
    response = jsonify(result)
    return response, 201


def get_valuestream(valuestream_id: str) -> Tuple[Any, int]:
    """Get valuestream by id route.

    ---
    get:
      description: Get valuestream
      parameters:
        - in: path
          name: valuestream_id
          schema:
            type: integer
          required: true
          description: ID of the valuestream
      responses:
        200:
          description: Get valuestream
          content:
            application/json:
              schema: ExistingValuestreamV2Schema
        404:
          description: Valuestream not found
    """
    with generate_session() as session:
        try:
            raw_valuestream = (
                valuestreams_crud.get_entity_without_team_views(
                    session, get_sanitized_id(valuestream_id)
                )
                if FEATURE_FLAGS["FEATURE_TEAM_VIEWS"]
                else valuestreams_crud.get_entity(
                    session, get_sanitized_id(valuestream_id)
                )
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_valuestream)
    response = jsonify(result)
    return response, 200


@requires_security([requires_admin, requires_vs_access])
def update_valuestream(valuestream_id: str) -> Tuple[Any, int]:
    """Update valuestream route.

    ---
    put:
      description: Update valuestream
      parameters:
        - in: path
          name: valuestream_id
          schema:
            type: integer
          required: true
          description: ID of the valuestream
      requestBody:
        content:
          application/json:
            schema: NewValuestreamV2Schema
      responses:
        200:
          description: The valuestream was successfully updated
          content:
            application/json:
              schema: ExistingValuestreamV2Schema
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
            raw_valuestream = valuestreams_crud.update_entity(
                session, data, get_sanitized_id(valuestream_id)
            )
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_valuestream)
    response = jsonify(result)
    return response, 200


@requires_security([requires_admin, requires_vs_access])
def delete_valuestream(valuestream_id: str) -> Tuple[Any, int]:
    """Delete valuestream route.

    ---
    delete:
      description: Delete valuestream
      parameters:
        - in: path
          name: valuestream_id
          schema:
            type: integer
          required: true
          description: ID of the valuestream
      responses:
        204:
          description: The valuestream was successfully deleted
    """
    with generate_session() as session:
        valuestreams_crud.delete_entity(session, get_sanitized_id(valuestream_id))
    return "", 204


def create_router() -> Blueprint:
    """Router factory."""
    valuestream_id_route = "/<valuestream_id>"
    router = Blueprint("valuestreams", __name__, url_prefix="/valuestreams")
    router.route("", methods=["GET"])(list_valuestreams)
    router.route("", methods=["POST"])(create_valuestream)
    router.route(valuestream_id_route, methods=["GET"])(get_valuestream)
    router.route(valuestream_id_route, methods=["PUT"])(update_valuestream)
    router.route(valuestream_id_route, methods=["DELETE"])(delete_valuestream)
    return router
