"""Git branch model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from ._base import MetadataBase, ModelBase
from .repository import Repository


class Branch(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "branches"

    repository_id = Column(Integer, ForeignKey(Repository.id), nullable=False)
    last_updated = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
