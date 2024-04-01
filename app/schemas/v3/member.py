"""Schema for Member model."""

from marshmallow import fields

from app import config

from ._base import SchemaBase


class TeamMemberV3Schema(SchemaBase):
    """Team member schema."""

    start_date = fields.DateTime()
    end_date = fields.DateTime(allow_none=True)
    member = fields.Nested("MemberV3Schema", exclude=("teams",))
    if config.FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        team = fields.Nested("TeamV3Schema", exclude=("members",), dump_only=True)


class MemberV3Schema(SchemaBase):
    """Member schema."""

    name = fields.String(required=True)
    username = fields.String(required=True)
    teams = fields.Nested("TeamMemberV3Schema", many=True, dump_only=True)
