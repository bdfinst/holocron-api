"""Value stream routes."""

from typing import Any, Mapping, Tuple, cast

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud import value_streams_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import (
    requires_admin,
    requires_org_access,
    requires_security,
    requires_vs_access,
)
from app.schemas.v2 import ValueStreamV2Schema
from app.security import MALFORMED_REQ_PARAMS_MSG, get_sanitized_id, log_security_event

schema = ValueStreamV2Schema()


def list_value_streams() -> Tuple[Any, int]:
    """List value streams route.

    ---
    get:
      description: List value streams
      responses:
        200:
          description: List value streams
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/ValueStreamV2'
    """
    with generate_session() as session:
        raw_value_streams = value_streams_crud.get_entities(session)
        value_streams = [
            schema.dump(value_stream) for value_stream in raw_value_streams
        ]
    result = {"result": value_streams}
    return jsonify(result), 200


@requires_security([requires_admin, requires_org_access])
def create_value_stream() -> Tuple[Any, int]:
    """Create value stream route.

    ---
    post:
      description: Create value stream
      requestBody:
        content:
          application/json:
            schema: ValueStreamV2Schema
      responses:
        201:
          description: The value stream was successfully created
          content:
            application/json:
              schema: ValueStreamV2Schema
        400:
          description: Failure due to invalid request
          content:
            application/json:
              schema: ValidationErrorV2Schema
    """
    try:
        data = schema.load(cast(Mapping[str, Any], request.json))
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_value_stream = value_streams_crud.create_entity(session, data)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_value_stream)
    return jsonify(result), 201


def get_value_stream(value_stream_id: str) -> Tuple[Any, int]:
    """Get value stream by id route.

    ---
    get:
      description: Get value stream
      parameters:
        - in: path
          name: value_stream_id
          schema:
            type: integer
          required: true
          description: ID of the value stream
      responses:
        200:
          description: Get value stream
          content:
            application/json:
              schema: ValueStreamV2Schema
        404:
          description: Value stream not found
    """
    with generate_session() as session:
        try:
            raw_value_stream = value_streams_crud.get_entity(
                session, get_sanitized_id(value_stream_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_value_stream)
    return jsonify(result), 200


@requires_security([requires_admin, requires_vs_access])
def update_value_stream(value_stream_id: str) -> Tuple[Any, int]:
    """Update value stream route.

    ---
    put:
      description: Update value stream
      parameters:
        - in: path
          name: value_stream_id
          schema:
            type: integer
          required: true
          description: ID of the value stream
      requestBody:
        content:
          application/json:
            schema: ValueStreamV2Schema
      responses:
        200:
          description: The value stream was successfully updated
          content:
            application/json:
              schema: ValueStreamV2Schema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorV2Schema
    """
    try:
        data = schema.load(cast(Mapping[str, Any], request.json))
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_value_stream = value_streams_crud.update_entity(
                session, data, get_sanitized_id(value_stream_id)
            )
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_value_stream)
    return jsonify(result), 200


@requires_security([requires_admin, requires_vs_access])
def delete_value_stream(value_stream_id: str) -> Tuple[Any, int]:
    """Delete value stream route.

    ---
    delete:
      description: Delete value stream
      parameters:
        - in: path
          name: value_stream_id
          schema:
            type: integer
          required: true
          description: ID of the value stream
      responses:
        204:
          description: The value stream was successfully deleted
    """
    with generate_session() as session:
        value_streams_crud.delete_entity(session, get_sanitized_id(value_stream_id))
    return "", 204


def create_router() -> Blueprint:
    """Router factory."""
    value_stream_id_route = "/<value_stream_id>"
    router = Blueprint("valuestreams", __name__, url_prefix="/valuestreams")
    router.route("", methods=["GET"])(list_value_streams)
    router.route("", methods=["POST"])(create_value_stream)
    router.route(value_stream_id_route, methods=["GET"])(get_value_stream)
    router.route(value_stream_id_route, methods=["PUT"])(update_value_stream)
    router.route(value_stream_id_route, methods=["DELETE"])(delete_value_stream)
    return router
