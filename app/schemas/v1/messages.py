"""Schemas for non-model based responses."""
from marshmallow import Schema, fields


class ValidationErrorV1Schema(Schema):
    """Schema for returning schema validation errors."""

    fieldName = fields.List(fields.String())
