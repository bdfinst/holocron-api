"""Valuestream routes."""
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud import valuestreams_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import ValuestreamSchema

router = Blueprint("valuestreams", __name__, url_prefix="/valuestreams")

schema = ValuestreamSchema()


@router.route("", methods=["GET"])
def list_valuestreams():
    """List valuestreams route.

    ---
    get:
      description: List valuestreams
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Valuestream'
    """
    with generate_session() as session:
        raw_valuestreams = valuestreams_crud.get_entities(session)
        valuestreams = [schema.dump(valuestream) for valuestream in raw_valuestreams]
    result = {"result": valuestreams}
    return jsonify(result), 200


@router.route("", methods=["POST"])
def create_valuestream():
    """Create valuestream route.

    ---
    post:
      description: Create valuestream
      requestBody:
        content:
          application/json:
            schema: ValuestreamSchema
      responses:
        201:
          content:
            application/json:
              schema: ValuestreamSchema
        400:
          content:
            application/json:
              schema: ValidationErrorSchema
    """
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_valuestream = valuestreams_crud.create_entity(session, data)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_valuestream)
    return jsonify(result), 201


@router.route("/<id_>", methods=["GET"])
def get_valuestream(id_: int):
    """Get valuestream by id route.

    ---
    get:
      description: Get valuestream
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the valuestream
      responses:
        200:
          content:
            application/json:
              schema: ValuestreamSchema
    """
    with generate_session() as session:
        raw_valuestream = valuestreams_crud.get_entity(session, id_)
        result = schema.dump(raw_valuestream)
    return jsonify(result), 200


@router.route("/<id_>", methods=["PUT"])
def update_valuestream(id_: int):
    """Update valuestream route.

    ---
    put:
      description: Update valuestream
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the valuestream
      requestBody:
        content:
          application/json:
            schema: ValuestreamSchema
      responses:
        200:
          content:
            application/json:
              schema: ValuestreamSchema
        400:
          content:
            application/json:
              schema: ValidationErrorSchema
    """
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_valuestream = valuestreams_crud.update_entity(session, data, id_)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_valuestream)
    return jsonify(result), 200


@router.route("/<id_>", methods=["DELETE"])
def delete_valuestream(id_: int):
    """Delete valuestream route.

    ---
    delete:
      description: Delete valuestream
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the valuestream
      responses:
        204:
          description: The valuestream was successfully deleted
    """
    with generate_session() as session:
        valuestreams_crud.delete_entity(session, id_)
    return "", 204
