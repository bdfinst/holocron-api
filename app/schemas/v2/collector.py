"""Schema for collector target config items."""

from marshmallow import fields

from ._base import SchemaBase


class CollectorV2Schema(SchemaBase):
    """Schema for Collector Target Config Item model."""

    target = fields.String(required=True)
    collector_interval_seconds = fields.Integer(allow_none=True)
    look_back_days = fields.Integer(allow_none=True)
    collector_targets_intrvl_secs = fields.Integer(allow_none=True)
    max_requests_per_minute = fields.Integer(allow_none=True)
    name = fields.String(required=True)
