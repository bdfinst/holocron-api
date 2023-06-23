"""Schema for Commit model."""
from typing import Tuple

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Commit
from app.schemas.v1._base import SchemaBase


class CommitV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Commit model."""

    class Meta:
        """Configuration."""

        model = Commit
        exclude: Tuple[str, ...] = ("repository_id",)

    collector_target_id = auto_field("repository_id")
