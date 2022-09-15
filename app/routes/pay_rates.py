"""PayRate routes."""
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud import pay_rates_crud
from app.database import generate_session
from app.middleware import requires_leadership
from app.schemas import PayRateSchema
from app.security import MALFORMED_REQ_PARAMS_MSG, log_security_event

router = Blueprint("payrates", __name__, url_prefix="/payrates")

schema = PayRateSchema()


@router.route("", methods=["GET"])
@requires_leadership
def list_pay_rates():
    """List pay rates route.

    ---
    get:
      description: Get pay rates
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
                      $ref: '#/components/schemas/PayRate'
    """
    with generate_session() as session:
        raw_pay_rates = pay_rates_crud.get_entities(session)
        pay_rates = [schema.dump(pay_rate) for pay_rate in raw_pay_rates]
    result = {"result": pay_rates}
    return jsonify(result), 200


@router.route("", methods=["POST"])
@requires_leadership
def upsert_pay_rate():
    """Upsert pay rate route.

    ---
    post:
      description: Create or update a pay rate
      requestBody:
        content:
          application/json:
            schema: PayRateSchema
      responses:
        201:
          description: The pay rate was successfully set
          content:
            application/json:
              schema: PayRateSchema
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
        raw_pay_rate = pay_rates_crud.upsert_entity(session, data)
        result = schema.dump(raw_pay_rate)
    return jsonify(result), 201
