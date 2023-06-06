"""Schema for Member model."""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Member, TeamsMembers

from ._base import SchemaBase


class TeamMemberSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Team member schema."""

    class Meta:
        """Configuration."""

        model = TeamsMembers
        include_relationships = True

    member = fields.Nested("MemberSchema", exclude=("teams",))
    team = fields.Nested("ExistingTeamSchema", exclude=("members",), dump_only=True)


class MemberSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Existing member schema."""

    class Meta:
        """Configuration."""

        model = Member
        include_relationships = True

    teams = fields.Nested(TeamMemberSchema, many=True, exclude=("member",))
