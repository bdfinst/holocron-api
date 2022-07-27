"""SCM merge/pull request model."""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from ._base import MetadataBase, ModelBase
from .repository import Repository


class GitRequest(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "git_requests"

    repository_id = Column(
        Integer, ForeignKey(Repository.id, ondelete="CASCADE"), nullable=False
    )
    title = Column(String(), nullable=False)
    is_open = Column(Boolean)
    last_updated = Column(DateTime, nullable=False)
    url = Column(String, nullable=False, unique=True)
