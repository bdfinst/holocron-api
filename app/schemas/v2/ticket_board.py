"""Schema for TicketBoard model."""
from typing import Tuple

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import TicketBoard
from app.schemas.v1._base import SchemaBase
from app.schemas.v1.collector_target_config import ConfigItemV1Schema


class TicketBoardV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for TicketBoard model."""

    class Meta:
        """Configuration."""

        model = TicketBoard
        include_relationships = True
        exclude: Tuple[str, ...] = ("tickets", "board_id")

    team_id = auto_field()
    config = fields.Nested(ConfigItemV1Schema, many=True)
