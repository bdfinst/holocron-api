"""PayRate routes."""

from typing import Any, Mapping, Tuple, cast

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud import pay_rates_crud
from app.database import generate_session
from app.middleware import requires_org_leadership, requires_security
from app.schemas.v2 import MultiplePayRateV2Schema, PayRateV2Schema
from app.security import MALFORMED_REQ_PARAMS_MSG, log_security_event
from app.utils.pagination import get_pagination_info, set_pagination_header

schema = PayRateV2Schema()
many_schema = MultiplePayRateV2Schema()


@requires_security([requires_org_leadership])
def list_pay_rates() -> Tuple[Any, int]:
    """List pay rates route.

    ---
    get:
      description: Get pay rates
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
          description: Get pay rates
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/PayRateV2'
    """
    with generate_session() as session:
        page_info = get_pagination_info(request.args, pay_rates_crud.get_count(session))
        raw_pay_rates = pay_rates_crud.get_entities_paginated(
            session, limit=page_info.limit, offset=page_info.offset
        )
        pay_rates = [schema.dump(pay_rate) for pay_rate in raw_pay_rates]
    result = {"result": pay_rates}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


@requires_security([requires_org_leadership])
def upsert_pay_rates() -> Tuple[Any, int]:
    """Upsert pay rates route.

    ---
    post:
      description: Create or update pay rates
      requestBody:
        content:
          application/json:
            schema: MultiplePayRateV2Schema
      responses:
        201:
          description: The pay rates successfuly set.
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/PayRateV2'
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorV2Schema
    """
    try:
        data = many_schema.load(cast(Mapping[str, Any], request.json))
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        rates = data.get("rates")
        upserted_rates = iter(
            pay_rates_crud.upsert_entity(session, rate) for rate in rates
        )
        result = {"result": [schema.dump(rate) for rate in upserted_rates]}
    response = jsonify(result)
    return response, 201


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("pay-rates", __name__, url_prefix="/pay-rates")
    router.route("", methods=["GET"])(list_pay_rates)
    router.route("", methods=["POST"])(upsert_pay_rates)
    return router
