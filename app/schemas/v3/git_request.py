"""Schema for GitRequest model."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import GitRequest

from ._base import SchemaBase


class GitRequestV3Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for GitRequest model."""

    class Meta:
        """Configuration."""

        model = GitRequest
