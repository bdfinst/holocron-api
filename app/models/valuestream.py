"""Holocron organization model."""
from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from ._base import MetadataBase, ModelBase
from .organization import Organization
from .user import User

association_table = Table(
    "valuestream_users",
    MetadataBase.metadata,
    Column("valuestream_id", ForeignKey("valuestreams.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey(User.id)),
)


class Valuestream(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "valuestreams"

    name = Column(String, nullable=False)
    organization_id = Column(
        Integer, ForeignKey(Organization.id), nullable=False, index=True
    )
    teams = relationship("Team")
    users = relationship("User", secondary=association_table)

    UniqueConstraint(name, organization_id)
