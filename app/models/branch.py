"""SCM branch model."""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from ._base import MetadataBase, ModelBase
from .repository import Repository


class Branch(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "branches"

    repository_id = Column(
        Integer, ForeignKey(Repository.id, ondelete="CASCADE"), nullable=False
    )
    last_updated = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    is_default = Column(Boolean, server_default="False")
