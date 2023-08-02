"""BaseCRUD extension and instance for Commit model."""
from app.models import Commit, Repository

from ._base_metric import BaseMetricCRUD


class CommitsCRUD(BaseMetricCRUD[Commit]):
    """Base CRUD extension for Commit model."""


commits_crud = CommitsCRUD(Commit, Repository)
