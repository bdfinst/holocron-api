"""Schema for Repository model."""
from typing import Tuple

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Repository

from ._base import SchemaBase


class RepositorySchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Repository model."""

    class Meta:
        """Configuration."""

        model = Repository
        include_relationships = True
        exclude: Tuple[str, ...] = ("branches", "commits", "git_requests")

    team_id = auto_field()
