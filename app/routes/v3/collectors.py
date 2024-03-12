"""Collector routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud import collectors_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_security
from app.schemas.v3 import CollectorV3Schema
from app.security import MALFORMED_REQ_PARAMS_MSG, get_sanitized_id, log_security_event
from app.utils.pagination import get_pagination_info, set_pagination_header

schema = CollectorV3Schema()


def list_collectors() -> Tuple[Any, int]:
    """Get all collectors.

    ---
    get:
      description: Get all collectors
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
          description: Get all collectors
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/CollectorV3'
    """
    with generate_session() as session:
        page_info = get_pagination_info(
            request.args, collectors_crud.get_count(session)
        )
        raw_collectors = collectors_crud.get_entities_paginated(
            session, offset=page_info.offset, limit=page_info.limit
        )
        collector_models = [schema.dump(collector) for collector in raw_collectors]
    result = {"result": collector_models}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


def get_collector(collector_id: str) -> Tuple[Any, int]:
    """Get collector by id route.

    ---
    get:
      description: Get collector
      parameters:
        - in: path
          name: collector_id
          schema:
            type: integer
          required: true
          description: ID of the collector
      responses:
        200:
          description: Get collector
          content:
            application/json:
              schema: CollectorV3Schema
        404:
          description: Collector not found
    """
    with generate_session() as session:
        try:
            raw_collector = collectors_crud.get_entity(
                session, get_sanitized_id(collector_id)
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_collector)
    response = jsonify(result)
    return response, 200


@requires_security([requires_admin])
def update_collector(collector_id: str) -> Tuple[Any, int]:
    """Update collector route.

    ---
    put:
      description: Update collector
      parameters:
        - in: path
          name: collector_id
          schema:
            type: integer
          required: true
          description: ID of the collector
      requestBody:
        content:
          application/json:
            schema: CollectorV3Schema
      responses:
        200:
          description: The collector was successfully updated
          content:
            application/json:
              schema: CollectorV3Schema
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
            raw_collector = collectors_crud.update_entity(
                session, data, get_sanitized_id(collector_id)
            )
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_collector)
    response = jsonify(result)
    return response, 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("collectors", __name__, url_prefix="/collectors")
    router.route("", methods=["GET"])(list_collectors)
    router.route("/<collector_id>", methods=["GET"])(get_collector)
    router.route("/<collector_id>", methods=["PUT"])(update_collector)
    return router
