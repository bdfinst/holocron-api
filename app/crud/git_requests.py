"""BaseCRUD extension and instance for GitRequest model."""

from app.models import GitRequest, Repository

from ._base_metric import BaseMetricCRUD


class GitRequestsCRUD(BaseMetricCRUD[GitRequest]):
    """Base CRUD extension for GitRequest model."""


git_requests_crud = GitRequestsCRUD(GitRequest, Repository)
