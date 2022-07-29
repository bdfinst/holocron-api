"""Schema for Organization model."""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Organization

from ._base import SchemaBase
from .valuestream import ValuestreamMetricsSchema, ValuestreamSchema


class OrganizationSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Organization model."""

    class Meta:
        """Configuration."""

        model = Organization
        include_relationships = True

    valuestreams = fields.Nested(ValuestreamSchema, many=True)


class OrganizationMetricsSchema(OrganizationSchema):
    """Schema for Organization model with metric objects."""

    valuestreams = fields.Nested(ValuestreamMetricsSchema, many=True)
