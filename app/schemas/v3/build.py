"""Schema for Build model."""

from marshmallow import fields

from app.models import BuildStatus

from ._base import SchemaBase


class BuildV3Schema(SchemaBase):
    """Schema for Build model."""

    is_deployed = fields.Boolean()
    build_status = fields.Enum(BuildStatus, by_value=True)
    collector_target_id = fields.Integer()
    build_url = fields.String()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
