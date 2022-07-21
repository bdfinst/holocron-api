"""Schema for Pipeline model."""
from typing import Tuple

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Pipeline

from ._base import SchemaBase
from .build import BuildSchema


class PipelineSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Pipeline model."""

    class Meta:
        """Configuration."""

        model = Pipeline
        include_relationships = True
        exclude: Tuple[str, ...] = ("builds",)

    team_id = auto_field()


class PipelineMetricsSchema(PipelineSchema):
    """Schema for Pipeline model with metric children."""

    class Meta(PipelineSchema.Meta):
        """Configuration."""

        exclude = ()

    builds = fields.Nested(BuildSchema, many=True)
