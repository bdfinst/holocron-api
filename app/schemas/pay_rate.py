"""Schema for PayRate model."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import PayRate

from ._base import SchemaBase


class PayRateSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for PayRate model."""

    class Meta:
        """Configuration."""

        model = PayRate
