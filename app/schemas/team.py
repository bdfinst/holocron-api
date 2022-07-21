"""Schema for Team model."""
from typing import Any, Dict

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Team

from ._base import SchemaBase
from .pipelines import PipelineMetricsSchema
from .repository import RepositoryMetricsSchema
from .ticket_board import TicketBoardMetricsSchema


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
        exclude = ("collector_targets",)

    pipelines = fields.Nested(PipelineMetricsSchema, many=True)
    repositories = fields.Nested(RepositoryMetricsSchema, many=True)
    ticket_boards = fields.Nested(TicketBoardMetricsSchema, many=True)


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
