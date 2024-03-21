"""Schema for ValueStream model."""

from typing import Any, Dict

from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import ValueStream
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .team import ExistingTeamV3Schema
from .user import UserV3Schema


class ExistingValueStreamV3Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for existing value stream model."""

    class Meta:
        """Configuration."""

        model = ValueStream
        include_relationships = True

    organization_id = auto_field()
    teams = fields.Nested(ExistingTeamV3Schema, many=True)
    users = fields.Nested(UserV3Schema, many=True)


class NewValueStreamV3Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for new value stream model."""

    class Meta:
        """Configuration."""

        model = ValueStream

    name = fields.Str(required=True, validate=input_name_validator)
    organization_id = fields.Int(required=True)
    user_ids = fields.List(fields.Int(), required=True, validate=validate.Length(min=1))


class ValueStreamV3Schema:
    """Contain both existing and new schemas."""

    def __init__(self):
        """Initialize."""
        self.existing_schema = ExistingValueStreamV3Schema()
        self.new_schema = NewValueStreamV3Schema()

    def dump(self, data) -> Dict[str, Any]:
        """Dump using the existing schema."""
        return self.existing_schema.dump(data)

    def load(self, data) -> Dict[str, Any]:
        """Load using the new schema."""
        return self.new_schema.load(data)
