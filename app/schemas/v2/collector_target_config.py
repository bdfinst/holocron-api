"""Schema for collector target config items."""

from marshmallow import fields

from ._base import SchemaBase


class ConfigItemV2Schema(SchemaBase):
    """Schema for Collector Target Config Item model."""

    key = fields.String()
    value = fields.String()
    collector_target_id = fields.Integer()
