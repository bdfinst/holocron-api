"""Schema for TicketBoard model."""
from typing import Tuple

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import CollectorTargetType, TicketBoard

from ._base import SchemaBase
from .collector_target_config import ConfigItemV2Schema


class TicketBoardV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for TicketBoard model."""

    class Meta:
        """Configuration."""

        model = TicketBoard
        include_relationships = True
        exclude: Tuple[str, ...] = ("tickets",)

    team_id = auto_field()
    type = fields.Enum(CollectorTargetType, by_value=True)
    config = fields.Nested(ConfigItemV2Schema, many=True)
