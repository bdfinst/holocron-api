"""Build pipeline model."""

from typing import List

from sqlalchemy.orm import Mapped, relationship

from .build import Build
from .collector_target import CollectorTarget


class Pipeline(CollectorTarget):
    """Model class."""

    builds: Mapped[List["Build"]] = relationship(default_factory=list)
