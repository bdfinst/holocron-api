"""Project model."""

from typing import List

from sqlalchemy.orm import Mapped, relationship

from .collector_target import CollectorTarget
from .project_issue import ProjectIssue


class Project(CollectorTarget):
    """Model class."""

    issues: Mapped[List["ProjectIssue"]] = relationship(default_factory=list)
