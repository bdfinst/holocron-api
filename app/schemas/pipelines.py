"""Schema for Pipeline model."""
from typing import Tuple

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Pipeline

from ._base import SchemaBase


class PipelineSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Pipeline model."""

    class Meta:
        """Configuration."""

        model = Pipeline
        include_relationships = True
        exclude: Tuple[str, ...] = ("builds",)

    team_id = auto_field()
