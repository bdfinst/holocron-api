"""Schema for collector target config items."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Collector

from ._base import SchemaBase


class CollectorV3Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Collector Target Config Item model."""

    class Meta:
        """Configuration."""

        model = Collector
