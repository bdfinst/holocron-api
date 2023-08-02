"""SCM repository model."""
from typing import List, Optional

from sqlalchemy.orm import Mapped, relationship

from .branch import Branch
from .collector_target import CollectorTarget
from .commit import Commit
from .git_request import GitRequest


class Repository(CollectorTarget):
    """Model class."""

    trunk_branch: Mapped[Optional[str]]

    branches: Mapped[List["Branch"]] = relationship(default_factory=list)
    commits: Mapped[List["Commit"]] = relationship(default_factory=list)
    git_requests: Mapped[List["GitRequest"]] = relationship(default_factory=list)
