"""Schema for Commit model."""

from marshmallow import fields

from ._base import SchemaBase


class CommitV3Schema(SchemaBase):
    """Schema for Commit model."""

    sha = fields.String()
    is_merged = fields.Boolean()
    author_username = fields.String()
    collector_target_id = fields.Integer()
    date = fields.DateTime()
