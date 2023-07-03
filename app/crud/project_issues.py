"""BaseCRUD extension and instance for ProjectIssue model."""
from app.models import Project, ProjectIssue

from ._base_metric import BaseMetricCRUD


class ProjectIssueCRUD(BaseMetricCRUD[ProjectIssue]):
    """Base CRUD extension for ProjectIssue model."""


project_issues_crud = ProjectIssueCRUD(ProjectIssue, Project, "resource_id")
