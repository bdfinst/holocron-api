"""Schema for Repository model."""

from marshmallow import fields

from .collector_target import CollectorTargetV3Schema


class RepositoryV3Schema(CollectorTargetV3Schema):
    """Schema for Repository model."""

    trunk_branch = fields.String(allow_none=True)
