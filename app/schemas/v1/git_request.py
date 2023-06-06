"""Schema for Git Request model."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import GitRequest

from ._base import SchemaBase


class GitRequestSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Git Request model."""

    class Meta:
        """Configuration."""

        model = GitRequest
