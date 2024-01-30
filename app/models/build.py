"""Build instance model."""

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase


class BuildStatus(enum.Enum):
    """Enum for 'build_status' field of Build."""

    PASSED = "PASSED"
    FAILED = "FAILED"
    PASSED_WITH_WARNINGS = "PASSED_WITH_WARNINGS"


class Build(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "builds"

    is_deployed: Mapped[bool]

    build_status: Mapped[BuildStatus] = mapped_column(
        Enum(BuildStatus, create_constraint=True, name="buildstatus")
    )
    collector_target_id: Mapped[int] = mapped_column(
        ForeignKey("collector_targets.id", ondelete="CASCADE")
    )
    build_url: Mapped[str] = mapped_column(unique=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
