"""Schema for Branch model."""

from marshmallow import fields

from ._base import SchemaBase


class BranchV3Schema(SchemaBase):
    """Schema for Branch model."""

    last_updated = fields.DateTime()
    name = fields.String()
    is_default = fields.Boolean()
    collector_target_id = fields.Integer()
    url = fields.String()
