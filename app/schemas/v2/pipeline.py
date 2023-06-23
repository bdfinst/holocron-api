"""Schema for Pipeline model."""
from typing import Tuple

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Pipeline
from app.schemas.v1._base import SchemaBase
from app.schemas.v1.collector_target_config import ConfigItemV1Schema


class PipelineV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Pipeline model."""

    class Meta:
        """Configuration."""

        model = Pipeline
        include_relationships = True
        exclude: Tuple[str, ...] = ("builds", "pipeline_id")

    team_id = auto_field()
    config = fields.Nested(ConfigItemV1Schema, many=True)
