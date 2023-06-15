"""Schema for Branch model."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Branch

from ._base import SchemaBase


class BranchV1Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Branch model."""

    class Meta:
        """Configuration."""

        model = Branch
