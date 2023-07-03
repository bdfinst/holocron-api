"""BaseCRUD extension and instance for Build model."""
from app.models import Build, Pipeline

from ._base_metric import BaseMetricCRUD


class BuildCRUD(BaseMetricCRUD[Build]):
    """Base CRUD extension for Build model."""


builds_crud = BuildCRUD(Build, Pipeline, "pipeline_id")
