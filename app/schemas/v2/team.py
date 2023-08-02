"""Schema for Team model."""
from typing import Any, Dict

from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app import config
from app.models import Team
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .member import TeamMemberV2Schema
from .user import UserV2Schema


class ExistingTeamV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Existing team schema."""

    class Meta:
        """Configuration."""

        model = Team
        include_relationships = True
        exclude = ("pipelines", "projects", "repositories", "ticket_boards")

    if config.FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        members = fields.Nested(TeamMemberV2Schema, many=True, exclude=("team",))
    users = fields.Nested(UserV2Schema, many=True)
    collector_targets = auto_field()
    valuestream_id = auto_field()


class NewTeamV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """New team schema."""

    class Meta:
        """Configuration."""

        model = Team
        exclude = ("is_workflow_only",)

    name = fields.Str(required=True, validate=input_name_validator)
    user_ids = fields.List(fields.Int(), required=True, validate=validate.Length(min=1))
    collector_target_ids = fields.List(fields.Int())
    team_size = fields.Int(required=True, validate=validate.Range(min=1))
    valuestream_id = auto_field()


class TeamV2Schema:
    """Contain both existing and new schemas."""

    def __init__(self):
        """Initialize."""
        self.existing_schema = ExistingTeamV2Schema()
        self.new_schema = NewTeamV2Schema()

    def dump(self, data) -> Dict[str, Any]:
        """Dump using the existing schema."""
        return self.existing_schema.dump(data)

    def load(self, data) -> Dict[str, Any]:
        """Load using the new schema."""
        return self.new_schema.load(data)
