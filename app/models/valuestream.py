"""Holocron organization model."""
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from ._base import MetadataBase, ModelBase
from .organization import Organization


class Valuestream(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "valuestreams"

    name = Column(String, nullable=False)
    organization_id = Column(
        Integer, ForeignKey(Organization.id), nullable=False, index=True
    )
    teams = relationship("Team")

    UniqueConstraint(name, organization_id)
