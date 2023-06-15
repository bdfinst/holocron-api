"""Schema for Commit model."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Commit

from ._base import SchemaBase


class CommitV1Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Commit model."""

    class Meta:
        """Configuration."""

        model = Commit
