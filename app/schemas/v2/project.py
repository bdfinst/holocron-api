"""Schema for Project model."""
from typing import Tuple

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import CollectorTargetType, Project

from ._base import SchemaBase
from .collector_target_config import ConfigItemV2Schema


class ProjectV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Project model."""

    class Meta:
        """Configuration."""

        model = Project
        include_relationships = True
        exclude: Tuple[str, ...] = ("issues",)

    team_id = auto_field()
    type = fields.Enum(CollectorTargetType, by_value=True)
    config = fields.Nested(ConfigItemV2Schema, many=True)
