"""Holocron collector model."""

from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase


class Collector(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "collectors"

    target: Mapped[str]
    target_url: Mapped[Optional[str]]
    collector_interval_seconds: Mapped[Optional[int]]
    look_back_days: Mapped[Optional[int]]
    collector_targets_intrvl_secs: Mapped[Optional[int]]
    max_requests_per_minute: Mapped[Optional[int]]

    name: Mapped[str] = mapped_column(unique=True)
