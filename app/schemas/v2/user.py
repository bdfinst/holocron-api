"""Schema for User model."""
from typing import Tuple

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import User

from ._base import SchemaBase


class UserV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for User model."""

    class Meta:
        """Configuration."""

        model = User
        include_relationships = True
        exclude: Tuple[str, ...] = ("sso_id",)
