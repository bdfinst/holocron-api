"""Schema for Team model."""
from typing import Any, Dict

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Team
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .user import UserSchema


class TeamSchemaBase(SQLAlchemyAutoSchema, SchemaBase):
    """Base schema for Team model."""

    class Meta:
        """Configuration."""

        model = Team

    valuestream_id = auto_field()


class ExistingTeamSchema(TeamSchemaBase):
    """Existing team schema."""

    class Meta:
        """Configuration."""

        model = Team
        include_relationships = True
        exclude = ("pipelines", "repositories", "ticket_boards")

    users = fields.Nested(UserSchema, many=True)
    collector_targets = auto_field()


class NewTeamSchema(TeamSchemaBase):
    """New team schema."""

    name = fields.Str(required=True, validate=input_name_validator)
    user_ids = fields.List(fields.Int())
    collector_target_ids = fields.List(fields.Int())


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
