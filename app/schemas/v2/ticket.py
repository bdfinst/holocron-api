"""Schema for Ticket model."""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import StatusHistory, Ticket, TicketPriority, TicketStatus, TicketType

from ._base import SchemaBase


class StatusHistoryV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Ticket StatusHistory model."""

    class Meta:
        """Configuration."""

        model = StatusHistory

    status = fields.Enum(TicketStatus, by_value=True)


class TicketV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Ticket model."""

    class Meta:
        """Configuration."""

        model = Ticket

    status_history = fields.Nested(StatusHistoryV2Schema, many=True)
    ticket_type = fields.Enum(TicketType, by_value=True)
    priority = fields.Enum(TicketPriority, by_value=True)
    status = fields.Enum(TicketStatus, by_value=True)
