"""Schema for Member model."""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Member, TeamsMembers

from ._base import SchemaBase


class TeamMemberV1Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Team member schema."""

    class Meta:
        """Configuration."""

        model = TeamsMembers
        include_relationships = True

    member = fields.Nested("MemberV1Schema", exclude=("teams",))
    team = fields.Nested("ExistingTeamV1Schema", exclude=("members",), dump_only=True)


class MemberV1Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Existing member schema."""

    class Meta:
        """Configuration."""

        model = Member
        include_relationships = True

    teams = fields.Nested(TeamMemberV1Schema, many=True, exclude=("member",))
