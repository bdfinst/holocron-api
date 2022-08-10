"""Schema for TicketBoard model."""
from typing import Tuple

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import TicketBoard

from ._base import SchemaBase


class TicketBoardSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for TicketBoard model."""

    class Meta:
        """Configuration."""

        model = TicketBoard
        include_relationships = True
        exclude: Tuple[str, ...] = ("tickets",)

    team_id = auto_field()
