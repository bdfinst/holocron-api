"""Schema for TicketBoard model."""
from typing import Tuple

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import TicketBoard

from ._base import SchemaBase
from .collector_target_config import ConfigItemSchema


class TicketBoardSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for TicketBoard model."""

    class Meta:
        """Configuration."""

        model = TicketBoard
        include_relationships = True
        exclude: Tuple[str, ...] = ("tickets",)

    team_id = auto_field()
    config = fields.Nested(ConfigItemSchema, many=True)
