"""Schema for collector target config items."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.collector_target import ConfigItem

from ._base import SchemaBase


class ConfigItemV3Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Collector Target Config Item model."""

    class Meta:
        """Configuration."""

        model = ConfigItem
