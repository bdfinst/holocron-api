"""Schema for Repository model."""

from marshmallow import fields

from .collector_target import CollectorTargetV2Schema


class RepositoryV2Schema(CollectorTargetV2Schema):
    """Schema for Repository model."""

    trunk_branch = fields.String(allow_none=True)
