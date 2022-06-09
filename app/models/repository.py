"""Repository model."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .collector_target import CollectorTarget


class Repository(CollectorTarget):
    """Model class."""

    trunk_branch = Column(String)
    repository_id = Column(Integer, index=True)
    branches = relationship("Branch")
    commits = relationship("Commit")
    git_requests = relationship("GitRequest")
