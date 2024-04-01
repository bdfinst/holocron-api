"""Schema for Member model."""

from marshmallow import fields

from app import config

from ._base import SchemaBase


class TeamMemberV2Schema(SchemaBase):
    """Team member schema."""

    start_date = fields.DateTime()
    end_date = fields.DateTime(allow_none=True)
    member = fields.Nested("MemberV2Schema", exclude=("teams",))
    if config.FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        team = fields.Nested("TeamV2Schema", exclude=("members",), dump_only=True)


class MemberV2Schema(SchemaBase):
    """Member schema."""

    name = fields.String(required=True)
    username = fields.String(required=True)
    teams = fields.Nested("TeamMemberV2Schema", many=True, dump_only=True)
