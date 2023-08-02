"""SCM branch model."""
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase


class Branch(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "branches"

    last_updated: Mapped[datetime]
    name: Mapped[str]
    is_default: Mapped[bool]

    collector_target_id: Mapped[int] = mapped_column(
        ForeignKey("collector_targets.id", ondelete="CASCADE")
    )
    url: Mapped[str] = mapped_column(unique=True)
