"""Holocron collector model."""
from sqlalchemy import Column, String

from ._base import MetadataBase, ModelBase


class Collector(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "collectors"

    name = Column(String, nullable=False, unique=True)
    target = Column(String, nullable=False)
