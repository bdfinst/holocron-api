"""Schema for Build Model."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Build

from ._base import SchemaBase


class BuildSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Build model."""

    class Meta:
        """Configuration."""

        model = Build
