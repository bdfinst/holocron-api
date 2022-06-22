"""PayRate routes."""
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud import pay_rates_crud
from app.database import generate_session
from app.middleware import requires_leadership
from app.schemas import PayRateSchema

router = Blueprint("payrates", __name__, url_prefix="/payrates")

schema = PayRateSchema()


@router.route("", methods=["GET"])
@requires_leadership
def list_pay_rates():
    """List pay rates route."""
    with generate_session() as session:
        raw_pay_rates = pay_rates_crud.get_entities(session)
        pay_rates = [schema.dump(pay_rate) for pay_rate in raw_pay_rates]
    result = {"result": pay_rates}
    return jsonify(result), 200


@router.route("", methods=["POST"])
@requires_leadership
def upsert_pay_rate():
    """Upsert pay rate route."""
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return err.messages, 400
    with generate_session() as session:
        raw_pay_rate = pay_rates_crud.upsert_entity(session, data)
        result = schema.dump(raw_pay_rate)
    return jsonify(result), 201
