"""Valuestream routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud import valuestreams_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin
from app.schemas import ValuestreamSchema
from app.security import MALFORMED_REQ_PARAMS_MSG, get_sanitized_id, log_security_event

router = Blueprint("valuestreams", __name__, url_prefix="/valuestreams")

schema = ValuestreamSchema()


@router.route("", methods=["GET"])
def list_valuestreams() -> Tuple[Any, int]:
    """List valuestreams route.

    ---
    get:
      description: List valuestreams
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
                      $ref: '#/components/schemas/ExistingValuestream'
    """
    with generate_session() as session:
        raw_valuestreams = valuestreams_crud.get_entities(session)
        valuestreams = [schema.dump(valuestream) for valuestream in raw_valuestreams]
    result = {"result": valuestreams}
    return jsonify(result), 200


@router.route("", methods=["POST"])
def create_valuestream() -> Tuple[Any, int]:
    """Create valuestream route.

    ---
    post:
      description: Create valuestream
      requestBody:
        content:
          application/json:
            schema: NewValuestreamSchema
      responses:
        201:
          description: The valuestream was successfully created
          content:
            application/json:
              schema: ExistingValuestreamSchema
        400:
          description: Failure due to invalid request
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
            raw_valuestream = valuestreams_crud.create_entity(session, data)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_valuestream)
    return jsonify(result), 201


@router.route("/<valuestream_id>", methods=["GET"])
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
              schema: ExistingValuestreamSchema
        404:
          description: Valuestream not found
    """
    with generate_session() as session:
        try:
            raw_valuestream = valuestreams_crud.get_entity(
                session, get_sanitized_id(valuestream_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_valuestream)
    return jsonify(result), 200


@router.route("/<valuestream_id>", methods=["PUT"])
@requires_admin
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
            schema: NewValuestreamSchema
      responses:
        200:
          description: The valuestream was successfully updated
          content:
            application/json:
              schema: ExistingValuestreamSchema
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
            raw_valuestream = valuestreams_crud.update_entity(
                session, data, get_sanitized_id(valuestream_id)
            )
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_valuestream)
    return jsonify(result), 200


@router.route("/<valuestream_id>", methods=["DELETE"])
@requires_admin
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
