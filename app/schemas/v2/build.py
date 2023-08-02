"""Schema for Build model."""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Build, BuildStatus

from ._base import SchemaBase


class BuildV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Build model."""

    class Meta:
        """Configuration."""

        model = Build

    build_status = fields.Enum(BuildStatus, by_value=True)
