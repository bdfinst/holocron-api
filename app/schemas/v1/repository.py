"""Schema for Repository model."""
from typing import Tuple

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Repository

from ._base import SchemaBase
from .collector_target_config import ConfigItemSchema


class RepositorySchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Repository model."""

    class Meta:
        """Configuration."""

        model = Repository
        include_relationships = True
        exclude: Tuple[str, ...] = ("branches", "commits", "git_requests")

    team_id = auto_field()
    config = fields.Nested(ConfigItemSchema, many=True)
