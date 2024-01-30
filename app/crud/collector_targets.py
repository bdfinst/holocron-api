"""BaseCRUD extension and instance for CollectorTarget model."""

from app.models import CollectorTarget

from ._base import BaseCRUD


class CollectorTargetsCRUD(BaseCRUD[CollectorTarget]):
    """Base CRUD extension for CollectorTarget model."""


collector_targets_crud = CollectorTargetsCRUD(CollectorTarget)
