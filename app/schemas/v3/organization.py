"""Schema for Organization model."""

from marshmallow import fields, validate

from app.config import SSO_ENABLED
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .user import UserV3Schema
from .value_stream import ValueStreamV3Schema


class OrganizationV3Schema(SchemaBase):
    """Schema for organization model."""

    value_streams = fields.Nested(ValueStreamV3Schema, many=True, dump_only=True)
    users = fields.Nested(UserV3Schema, many=True, dump_only=True)
    name = fields.String(required=True, validate=input_name_validator)
    user_ids = fields.List(
        fields.Integer(),
        required=SSO_ENABLED,
        validate=validate.Length(min=1),
        load_only=True,
    )
