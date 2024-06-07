"""Schema for ValueStream model."""

from marshmallow import fields, validate

from app.config import SSO_ENABLED
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .team import TeamV3Schema
from .user import UserV3Schema


class ValueStreamV3Schema(SchemaBase):
    """Schema for value stream model."""

    organization_id = fields.Integer(required=True)
    teams = fields.Nested(TeamV3Schema, many=True, dump_only=True)
    users = fields.Nested(UserV3Schema, many=True, dump_only=True)
    user_ids = fields.List(
        fields.Integer(),
        required=SSO_ENABLED,
        validate=validate.Length(min=1),
        load_only=True,
    )
    name = fields.String(required=True, validate=input_name_validator)
