"""Schema for CollectorTarget models."""

from marshmallow import fields

from app.models import CollectorTargetType

from ._base import SchemaBase
from .collector_target_config import ConfigItemV3Schema


class CollectorTargetV3Schema(SchemaBase):
    """Schema for CollectorTarget models."""

    team_id = fields.Integer()
    type = fields.Enum(CollectorTargetType, by_value=True)
    config = fields.Nested(ConfigItemV3Schema, many=True)
    url = fields.String()
    name = fields.String(allow_none=True)
    collector_id = fields.Integer()
    resource_id = fields.String()
    last_collected = fields.Integer(allow_none=True)
    is_deleted = fields.Boolean()
