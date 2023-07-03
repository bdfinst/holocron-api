"""Schema for ProjectIssue Model."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import ProjectIssue

from ._base import SchemaBase


class ProjectIssueV1Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for ProjectIssue model."""

    class Meta:
        """Configuration."""

        model = ProjectIssue
