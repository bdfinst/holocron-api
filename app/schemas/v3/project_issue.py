"""Schema for ProjectIssue Model."""

from marshmallow import fields

from app.models import ProjectIssueSeverity, ProjectIssueType

from ._base import SchemaBase


class ProjectIssueV3Schema(SchemaBase):
    """Schema for ProjectIssue model."""

    type = fields.Enum(ProjectIssueType, by_value=True)
    severity = fields.Enum(ProjectIssueSeverity, by_value=True)
    resource_id = fields.String()
    package = fields.String()
    collector_target_id = fields.Integer()
    issue_url = fields.String()
    created_date = fields.DateTime()
    closed_date = fields.DateTime(allow_none=True)
