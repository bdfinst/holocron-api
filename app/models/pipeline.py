"""Build pipeline model."""
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .build import Build
from .collector_target import CollectorTarget


class Pipeline(CollectorTarget):
    """Model class."""

    pipeline_id: Mapped[Optional[int]] = mapped_column(index=True)
    builds: Mapped[List["Build"]] = relationship()
