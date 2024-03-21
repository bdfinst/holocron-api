"""Holocron organization model."""

from typing import List

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import MetadataBase, ModelBase
from .user import User
from .value_stream import ValueStream

association_table = Table(
    "organization_users",
    MetadataBase.metadata,
    Column(
        "organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE")
    ),
    Column("user_id", Integer, ForeignKey(User.id)),
)


class Organization(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[List["User"]] = relationship(
        secondary=association_table, default_factory=list
    )
    value_streams: Mapped[List["ValueStream"]] = relationship(default_factory=list)
