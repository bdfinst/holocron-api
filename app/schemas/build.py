"""Schema for Build Model."""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Build, Job

from ._base import SchemaBase


class JobSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Job model."""

    class Meta:
        """Configuration."""

        model = Job


class BuildSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Build model."""

    class Meta:
        """Configuration."""

        model = Build

    jobs = fields.Nested(JobSchema, many=True)
