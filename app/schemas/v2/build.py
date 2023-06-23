"""Schema for Build model."""
from typing import Tuple

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Build
from app.schemas.v1._base import SchemaBase


class BuildV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Build model."""

    class Meta:
        """Configuration."""

        model = Build
        exclude: Tuple[str, ...] = ("pipeline_id",)

    collector_target_id = auto_field("pipeline_id")
