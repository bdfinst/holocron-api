"""Schema for Team model."""
from typing import Any, Dict

from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app import config
from app.models import Team
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .member import TeamMemberSchema
from .user import UserSchema


class ExistingTeamSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Existing team schema."""

    class Meta:
        """Configuration."""

        model = Team
        include_relationships = True
        exclude = ("pipelines", "repositories", "ticket_boards")

    if config.FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        members = fields.Nested(TeamMemberSchema, many=True, exclude=("team",))
    users = fields.Nested(UserSchema, many=True)
    collector_targets = auto_field()
    valuestream_id = auto_field()


class NewTeamSchema(SQLAlchemyAutoSchema, SchemaBase):
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


class TeamSchema:
    """Contain both existing and new schemas."""

    def __init__(self):
        """Initialize."""
        self.existing_schema = ExistingTeamSchema()
        self.new_schema = NewTeamSchema()

    def dump(self, data) -> Dict[str, Any]:
        """Dump using the existing schema."""
        return self.existing_schema.dump(data)

    def load(self, data) -> Dict[str, Any]:
        """Load using the new schema."""
        return self.new_schema.load(data)
