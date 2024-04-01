"""Schema for User model."""

from marshmallow import fields

from ._base import SchemaBase


class UserV2Schema(SchemaBase):
    """Schema for User model."""

    is_org_leadership = fields.Boolean()
    is_admin = fields.Boolean()
    username = fields.String(allow_none=True)
