"""Schema for Branch model."""
from typing import Tuple

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Branch
from app.schemas.v1._base import SchemaBase


class BranchV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Branch model."""

    class Meta:
        """Configuration."""

        model = Branch
        exclude: Tuple[str, ...] = ("repository_id",)

    collector_target_id = auto_field("repository_id")
