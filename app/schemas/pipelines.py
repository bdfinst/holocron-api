"""Schema for Pipeline model."""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Pipeline

from ._base import SchemaBase
from .build import BuildSchema


class PipelineSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Pipeline model."""

    class Meta:
        """Configuration."""

        model = Pipeline
        include_relationships = True

    builds = fields.Nested(BuildSchema, many=True)
