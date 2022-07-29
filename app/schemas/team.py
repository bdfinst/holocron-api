"""Schema for Team model."""
from typing import Any, Dict

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Team

from ._base import SchemaBase
from .collector_target import CollectorTargetSchema
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
        exclude = ("collector_targets", "pipelines", "repositories", "ticket_boards")

    users = fields.Nested(UserSchema, many=True)


class TeamMetricsSchema(TeamSchemaBase):
    """Team schema with metric objects."""

    class Meta:
        """Configuration."""

        model = Team
        include_relationships = True
        exclude = ("collector_targets", "users")

    pipelines = fields.Nested(CollectorTargetSchema, many=True)
    repositories = fields.Nested(CollectorTargetSchema, many=True)
    ticket_boards = fields.Nested(CollectorTargetSchema, many=True)


class NewTeamSchema(TeamSchemaBase):
    """New team schema."""

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
