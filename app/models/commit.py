"""SCM commit model."""
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

from ._base import MetadataBase, ModelBase
from .repository import Repository


class Commit(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "commits"

    repository_id = Column(Integer, ForeignKey(Repository.id), nullable=False)
    sha = Column(String(), nullable=False)
    is_merged = Column(Boolean)
    date = Column(DateTime(timezone=True), nullable=False)

    UniqueConstraint(repository_id, sha)
