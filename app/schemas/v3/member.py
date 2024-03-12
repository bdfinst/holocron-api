"""Schema for Member model."""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Member, TeamsMembers

from ._base import SchemaBase


class TeamMemberV3Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Team member schema."""

    class Meta:
        """Configuration."""

        model = TeamsMembers
        include_relationships = True

    class MemberNoTeamV3Schema(SQLAlchemyAutoSchema, SchemaBase):
        """Member schema with teams excluded."""

        class Meta:
            """Configuration."""

            model = Member
            include_relationships = True
            exclude = ("teams",)

    member = fields.Nested("MemberNoTeamV2Schema")
    team = fields.Nested("ExistingTeamV2Schema", exclude=("members",), dump_only=True)


class MemberV3Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Existing member schema."""

    class Meta:
        """Configuration."""

        model = Member
        include_relationships = True

    class TeamMemberNoMemberV3Schema(SQLAlchemyAutoSchema, SchemaBase):
        """Team member with member excluded."""

        class Meta:
            """Configuration."""

            model = TeamsMembers
            include_relationships = True
            exclude = ("member",)

    teams = fields.Nested("TeamMemberNoMemberV2Schema", many=True)
