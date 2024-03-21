"""Holocron team model."""

from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import MetadataBase, ModelBase
from .collector_target import CollectorTarget
from .member import TeamsMembers
from .pipeline import Pipeline
from .project import Project
from .repository import Repository
from .ticket_board import TicketBoard
from .user import User

association_table = Table(
    "team_users",
    MetadataBase.metadata,
    Column("team_id", Integer, ForeignKey("teams.id", ondelete="CASCADE")),
    Column("user_id", Integer, ForeignKey(User.id)),
)


class Team(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("name", "value_stream_id", "view_owner_id"),)

    name: Mapped[str]
    team_size: Mapped[int]

    value_stream_id: Mapped[int] = mapped_column(ForeignKey("value_streams.id"))
    is_workflow_only: Mapped[bool] = mapped_column(default=False)

    collector_targets: Mapped[List["CollectorTarget"]] = relationship(
        default_factory=list
    )
    team_history: Mapped[List["TeamHistory"]] = relationship(default_factory=list)
    users: Mapped[List["User"]] = relationship(
        secondary=association_table, default_factory=list
    )
    members: Mapped[List["TeamsMembers"]] = relationship(
        default_factory=list, back_populates="team"
    )
    pipelines: Mapped[List["Pipeline"]] = relationship(
        overlaps="collector_targets", default_factory=list
    )
    projects: Mapped[List["Project"]] = relationship(
        overlaps="collector_targets", default_factory=list
    )
    repositories: Mapped[List["Repository"]] = relationship(
        overlaps="collector_targets", default_factory=list
    )
    ticket_boards: Mapped[List["TicketBoard"]] = relationship(
        overlaps="collector_targets", default_factory=list
    )
    view_owner_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"),
        default=None,
    )


class TeamHistory(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "team_history"

    team_size: Mapped[int]

    team_id: Mapped[int] = mapped_column(ForeignKey(Team.id, ondelete="CASCADE"))
