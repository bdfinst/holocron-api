"""Holocron organization model."""

from typing import List

from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import MetadataBase, ModelBase
from .team import Team
from .user import User

association_table = Table(
    "valuestream_users",
    MetadataBase.metadata,
    Column(
        "valuestream_id", Integer, ForeignKey("valuestreams.id", ondelete="CASCADE")
    ),
    Column("user_id", Integer, ForeignKey(User.id)),
)


class Valuestream(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "valuestreams"
    __table_args__ = (UniqueConstraint("name", "organization_id"),)

    name: Mapped[str]

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), index=True
    )

    teams: Mapped[List["Team"]] = relationship(default_factory=list)
    users: Mapped[List["User"]] = relationship(
        secondary=association_table, default_factory=list
    )
