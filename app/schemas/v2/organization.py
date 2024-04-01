"""Schema for Organization model."""

from marshmallow import fields, validate

from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .user import UserV2Schema
from .value_stream import ValueStreamV2Schema


class OrganizationV2Schema(SchemaBase):
    """Schema for organization model."""

    value_streams = fields.Nested(
        ValueStreamV2Schema, many=True, dump_only=True, data_key="valuestreams"
    )
    users = fields.Nested(UserV2Schema, many=True, dump_only=True)
    name = fields.String(required=True, validate=input_name_validator)
    user_ids = fields.List(
        fields.Integer(), required=True, validate=validate.Length(min=1), load_only=True
    )
