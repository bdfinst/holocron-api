"""Schema for Organization model."""
from typing import Any, Dict

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Organization
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .valuestream import ExistingValuestreamSchema


class ExistingOrganizationSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for existing organization model."""

    class Meta:
        """Configuration."""

        model = Organization
        include_relationships = True

    valuestreams = fields.Nested(ExistingValuestreamSchema, many=True)


class NewOrganizationSchema(SQLAlchemyAutoSchema, SchemaBase):
    """New organization schema."""

    class Meta:
        """Configuration."""

        model = Organization

    name = fields.Str(required=True, validate=input_name_validator)


class OrganizationSchema:
    """Contain both existing and new schemas."""

    def __init__(self):
        """Initialize."""
        self.existing_schema = ExistingOrganizationSchema()
        self.new_schema = NewOrganizationSchema()

    def dump(self, data) -> Dict[str, Any]:
        """Dump using the existing schema."""
        return self.existing_schema.dump(data)

    def load(self, data) -> Dict[str, Any]:
        """Load using the new schema."""
        return self.new_schema.load(data)
