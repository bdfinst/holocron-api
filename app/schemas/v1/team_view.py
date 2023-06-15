"""Schema for Team model."""
from typing import Any, Dict

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Team
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase


class ExistingTeamViewV1Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Existing team schema."""

    class Meta:
        """Configuration."""

        model = Team
        include_relationships = True
        exclude = (
            "pipelines",
            "repositories",
            "ticket_boards",
            "users",
            "team_history",
            "team_size",
            "members",
        )

    collector_targets = auto_field()
    view_owner_id = auto_field()


class NewTeamViewV1Schema(SQLAlchemyAutoSchema, SchemaBase):
    """New team schema."""

    class Meta:
        """Configuration."""

        model = Team
        exclude = (
            "is_workflow_only",
            "team_size",
        )

    name = fields.Str(required=True, validate=input_name_validator)
    collector_target_ids = fields.List(fields.Int())
    view_owner_id = fields.Int(required=True)


class TeamViewV1Schema:
    """Contain both existing and new schemas."""

    def __init__(self):
        """Initialize."""
        self.existing_schema = ExistingTeamViewV1Schema()
        self.new_schema = NewTeamViewV1Schema()

    def dump(self, data) -> Dict[str, Any]:
        """Dump using the existing schema."""
        return self.existing_schema.dump(data)

    def load(self, data) -> Dict[str, Any]:
        """Load using the new schema."""
        return self.new_schema.load(data)
