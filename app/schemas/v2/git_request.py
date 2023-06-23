"""Schema for GitRequest model."""
from typing import Tuple

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import GitRequest
from app.schemas.v1._base import SchemaBase


class GitRequestV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for GitRequest model."""

    class Meta:
        """Configuration."""

        model = GitRequest
        exclude: Tuple[str, ...] = ("repository_id",)

    collector_target_id = auto_field("repository_id")
