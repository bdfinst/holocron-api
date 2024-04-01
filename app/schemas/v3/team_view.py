"""Schema for Team model."""

from marshmallow import fields

from app.utils.input_validation import input_name_validator

from ._base import SchemaBase


class TeamViewV3Schema(SchemaBase):
    """Team view schema."""

    collector_targets = fields.List(fields.Integer(), dump_only=True)
    collector_target_ids = fields.List(fields.Integer(), required=True, load_only=True)
    view_owner_id = fields.Integer(required=True)
    name = fields.String(required=True, validate=input_name_validator)
    is_workflow_only = fields.Boolean(dump_only=True)
