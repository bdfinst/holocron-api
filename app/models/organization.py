"""Holocron organization model."""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ._base import MetadataBase, ModelBase


class Organization(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "organizations"

    name = Column(String, nullable=False, unique=True)
    valuestreams = relationship("Valuestream")
