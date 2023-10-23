"""SCM merge/pull request model."""
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase


class GitRequest(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "git_requests"

    title: Mapped[str]
    is_open: Mapped[bool]
    last_updated: Mapped[datetime]
    first_opened: Mapped[Optional[datetime]]
    merged_at: Mapped[Optional[datetime]]
    author_username: Mapped[Optional[str]]

    collector_target_id: Mapped[int] = mapped_column(
        ForeignKey("collector_targets.id", ondelete="CASCADE")
    )
    url: Mapped[str] = mapped_column(unique=True)
