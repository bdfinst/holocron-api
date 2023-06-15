"""Schema for Ticket model."""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import StatusHistory, Ticket

from ._base import SchemaBase


class StatusHistoryV1Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Ticket StatusHistory model."""

    class Meta:
        """Configuration."""

        model = StatusHistory


class TicketV1Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Ticket model."""

    class Meta:
        """Configuration."""

        model = Ticket

    status_history = fields.Nested(StatusHistoryV1Schema, many=True)
