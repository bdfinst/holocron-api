"""Schema for Valuestream model."""
from typing import Any, Dict

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Valuestream
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .team import ExistingTeamSchema


class ExistingValuestreamSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for existing valuestream model."""

    class Meta:
        """Configuration."""

        model = Valuestream
        include_relationships = True

    organization_id = auto_field()
    teams = fields.Nested(ExistingTeamSchema, many=True)


class NewValuestreamSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for new valuestream model."""

    class Meta:
        """Configuration."""

        model = Valuestream

    name = fields.Str(required=True, validate=input_name_validator)
    organization_id = fields.Int(required=True)


class ValuestreamSchema:
    """Contain both existing and new schemas."""

    def __init__(self):
        """Initialize."""
        self.existing_schema = ExistingValuestreamSchema()
        self.new_schema = NewValuestreamSchema()

    def dump(self, data) -> Dict[str, Any]:
        """Dump using the existing schema."""
        return self.existing_schema.dump(data)

    def load(self, data) -> Dict[str, Any]:
        """Load using the new schema."""
        return self.new_schema.load(data)
