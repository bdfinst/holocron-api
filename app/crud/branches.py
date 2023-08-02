"""BaseCRUD extension and instance for Branch model."""
from app.models import Branch, Repository

from ._base_metric import BaseMetricCRUD


class BranchesCRUD(BaseMetricCRUD[Branch]):
    """Base CRUD extension for Branch model."""


branches_crud = BranchesCRUD(Branch, Repository)
