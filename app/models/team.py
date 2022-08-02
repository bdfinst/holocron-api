"""Holocron team model."""
from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from ._base import MetadataBase, ModelBase
from .user import User
from .valuestream import Valuestream

association_table = Table(
    "team_users",
    MetadataBase.metadata,
    Column("team_id", ForeignKey("teams.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey(User.id)),
)


class Team(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "teams"

    name = Column(String, nullable=False)
    team_size = Column(Integer, nullable=False)
    users = relationship("User", secondary=association_table)
    collector_targets = relationship("CollectorTarget")
    pipelines = relationship("Pipeline", overlaps="collector_targets")
    repositories = relationship("Repository", overlaps="collector_targets")
    ticket_boards = relationship("TicketBoard", overlaps="collector_targets")
    valuestream_id = Column(Integer, ForeignKey(Valuestream.id), nullable=False)

    UniqueConstraint(name, valuestream_id)
