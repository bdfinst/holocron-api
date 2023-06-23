"""Schema for Ticket model."""
from typing import Tuple

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Ticket
from app.schemas.v1._base import SchemaBase
from app.schemas.v1.ticket import StatusHistoryV1Schema


class TicketV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Ticket model."""

    class Meta:
        """Configuration."""

        model = Ticket
        exclude: Tuple[str, ...] = ("board_id", "ticket_id")

    collector_target_id = auto_field("board_id")
    status_history = fields.Nested(StatusHistoryV1Schema, many=True)
