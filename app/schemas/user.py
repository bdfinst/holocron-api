"""Schema for User model."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import User

from ._base import SchemaBase


class UserSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for User model."""

    class Meta:
        """Configuration."""

        model = User
        include_relationships = True
