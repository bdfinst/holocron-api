"""Schema for Pipeline model."""
from typing import Tuple

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import CollectorTargetType, Pipeline

from ._base import SchemaBase
from .collector_target_config import ConfigItemV2Schema


class PipelineV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Pipeline model."""

    class Meta:
        """Configuration."""

        model = Pipeline
        include_relationships = True
        exclude: Tuple[str, ...] = ("builds",)

    team_id = auto_field()
    type = fields.Enum(CollectorTargetType, by_value=True)
    config = fields.Nested(ConfigItemV2Schema, many=True)
