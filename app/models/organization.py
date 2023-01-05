"""Holocron organization model."""
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from ._base import MetadataBase, ModelBase
from .user import User

association_table = Table(
    "organization_users",
    MetadataBase.metadata,
    Column("organization_id", ForeignKey("organizations.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey(User.id)),
)


class Organization(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "organizations"

    name = Column(String, nullable=False, unique=True)
    valuestreams = relationship("Valuestream")
    users = relationship("User", secondary=association_table)
