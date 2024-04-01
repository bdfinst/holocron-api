"""Schema for GitRequest model."""

from marshmallow import fields

from ._base import SchemaBase


class GitRequestV2Schema(SchemaBase):
    """Schema for GitRequest model."""

    title = fields.String()
    is_open = fields.Boolean()
    last_updated = fields.DateTime()
    first_opened = fields.DateTime(allow_none=True)
    merged_at = fields.DateTime(allow_none=True)
    author_username = fields.String(allow_none=True)
    collector_target_id = fields.Integer()
    url = fields.String()
