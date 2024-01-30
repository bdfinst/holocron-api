"""SCM commit model."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase


class Commit(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "commits"
    __table_args__ = (UniqueConstraint("collector_target_id", "sha"),)

    sha: Mapped[str]
    is_merged: Mapped[bool]
    author_username: Mapped[str]

    collector_target_id: Mapped[int] = mapped_column(
        ForeignKey("collector_targets.id", ondelete="CASCADE")
    )
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
