"""Build instance model."""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase


class Build(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "builds"

    build_status: Mapped[str]
    is_deployed: Mapped[bool]
    passed_with_warnings: Mapped[bool]

    pipeline_id: Mapped[int] = mapped_column(
        ForeignKey("collector_targets.id", ondelete="CASCADE")
    )
    build_url: Mapped[str] = mapped_column(unique=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
