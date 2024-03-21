"""Schema for ValueStream model."""

from typing import Any, Dict

from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import ValueStream
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .team import ExistingTeamV2Schema
from .user import UserV2Schema


class ExistingValueStreamV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for existing value stream model."""

    class Meta:
        """Configuration."""

        model = ValueStream
        include_relationships = True

    organization_id = auto_field()
    teams = fields.Nested(ExistingTeamV2Schema, many=True)
    users = fields.Nested(UserV2Schema, many=True)


class NewValueStreamV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for new value stream model."""

    class Meta:
        """Configuration."""

        model = ValueStream

    name = fields.Str(required=True, validate=input_name_validator)
    organization_id = fields.Int(required=True)
    user_ids = fields.List(fields.Int(), required=True, validate=validate.Length(min=1))


class ValueStreamV2Schema:
    """Contain both existing and new schemas."""

    def __init__(self):
        """Initialize."""
        self.existing_schema = ExistingValueStreamV2Schema()
        self.new_schema = NewValueStreamV2Schema()

    def dump(self, data) -> Dict[str, Any]:
        """Dump using the existing schema."""
        return self.existing_schema.dump(data)

    def load(self, data) -> Dict[str, Any]:
        """Load using the new schema."""
        return self.new_schema.load(data)
