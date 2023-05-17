"""Holocron team member model."""
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import MetadataBase, ModelBase

if TYPE_CHECKING:
    from .team import Team


class Member(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "members"

    name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)

    teams: Mapped[List["TeamsMembers"]] = relationship(
        default_factory=list, back_populates="member"
    )


class TeamsMembers(MetadataBase, ModelBase):
    """Table for members and teams many-to-many relationship."""

    __tablename__ = "teams_members"

    start_date: Mapped[datetime]

    end_date: Mapped[Optional[datetime]]
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))

    team: Mapped["Team"] = relationship(back_populates="members", init=False)
    member: Mapped["Member"] = relationship(back_populates="teams", init=False)
