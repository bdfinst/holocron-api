"""Schema for TicketBoard model."""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import TicketBoard

from ._base import SchemaBase
from .ticket import TicketSchema


class TicketBoardSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for TicketBoard model."""

    class Meta:
        """Configuration."""

        model = TicketBoard
        include_relationships = True

    tickets = fields.Nested(TicketSchema, many=True)
    team_id = auto_field()
