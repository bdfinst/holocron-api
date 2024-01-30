"""Schema for PayRate model."""

from typing import Any, Dict, List

from marshmallow import Schema, ValidationError, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import PayRate

from ._base import SchemaBase


class PayRateV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for PayRate model."""

    class Meta:
        """Configuration."""

        model = PayRate

    email = fields.Email(required=True)
    rate = fields.Float(required=True, validate=validate.Range(min=1))


def unique_emails(rates: List[Dict[str, Any]]):
    """Validate unique emails in rates check."""
    unique_email_items = set(iter(rate["email"] for rate in rates))
    if len(unique_email_items) != len(rates):
        raise ValidationError("Duplicate email found in rates.")


class MultiplePayRateV2Schema(Schema):
    """Schema for multiple PayRate."""

    rates = fields.List(
        fields.Nested("PayRateV2Schema", only=("rate", "email")),
        validate=validate.And(validate.Length(min=1), unique_emails),
        required=True,
    )
