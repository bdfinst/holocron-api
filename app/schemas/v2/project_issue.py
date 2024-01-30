"""Schema for ProjectIssue Model."""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import ProjectIssue, ProjectIssueSeverity, ProjectIssueType

from ._base import SchemaBase


class ProjectIssueV2Schema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for ProjectIssue model."""

    class Meta:
        """Configuration."""

        model = ProjectIssue

    type = fields.Enum(ProjectIssueType, by_value=True)
    severity = fields.Enum(ProjectIssueSeverity, by_value=True)
