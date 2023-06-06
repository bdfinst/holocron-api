"""Schemas for non-model based responses."""
from marshmallow import Schema, fields


class ValidationErrorSchema(Schema):
    """Schema for returning schema validation errors."""

    fieldName = fields.List(fields.String())
