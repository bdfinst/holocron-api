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

    class MemberNoTeamV1Schema(SQLAlchemyAutoSchema, SchemaBase):
        """Member schema with teams excluded."""

        class Meta:
            """Configuration."""

            model = Member
            include_relationships = True
            exclude = ("teams",)

    member = fields.Nested("MemberNoTeamV1Schema")
    team = fields.Nested("ExistingTeamV1Schema", exclude=("members",), dump_only=True)


class MemberV1Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Existing member schema."""

    class Meta:
        """Configuration."""

        model = Member
        include_relationships = True

    class TeamMemberNoMemberV1Schema(SQLAlchemyAutoSchema, SchemaBase):
        """Team member with member excluded."""

        class Meta:
            """Configuration."""

            model = TeamsMembers
            include_relationships = True
            exclude = ("member",)

    teams = fields.Nested("TeamMemberNoMemberV1Schema", many=True)
