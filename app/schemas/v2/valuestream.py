"""Schema for Valuestream model."""

from typing import Any, Dict

from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Valuestream
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .team import ExistingTeamV2Schema
from .user import UserV2Schema


class ExistingValuestreamV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for existing valuestream model."""

    class Meta:
        """Configuration."""

        model = Valuestream
        include_relationships = True

    organization_id = auto_field()
    teams = fields.Nested(ExistingTeamV2Schema, many=True)
    users = fields.Nested(UserV2Schema, many=True)


class NewValuestreamV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for new valuestream model."""

    class Meta:
        """Configuration."""

        model = Valuestream

    name = fields.Str(required=True, validate=input_name_validator)
    organization_id = fields.Int(required=True)
    user_ids = fields.List(fields.Int(), required=True, validate=validate.Length(min=1))


class ValuestreamV2Schema:
    """Contain both existing and new schemas."""

    def __init__(self):
        """Initialize."""
        self.existing_schema = ExistingValuestreamV2Schema()
        self.new_schema = NewValuestreamV2Schema()

    def dump(self, data) -> Dict[str, Any]:
        """Dump using the existing schema."""
        return self.existing_schema.dump(data)

    def load(self, data) -> Dict[str, Any]:
        """Load using the new schema."""
        return self.new_schema.load(data)
