"""Holocron collector target model."""
import enum
from typing import List, Optional

from sqlalchemy import BigInteger, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import MetadataBase, ModelBase
from .collector import Collector


class CollectorTargetType(enum.Enum):
    """Enum for 'type' field of CollectorTarget."""

    BUILD = "BUILD"
    PROJECT_ANALYSIS = "PROJECT_ANALYSIS"
    SCM = "SCM"
    WORKFLOW = "WORKFLOW"


class CollectorTarget(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "collector_targets"
    __table_args__ = (
        UniqueConstraint("collector_id", "url"),
        UniqueConstraint("collector_id", "resource_id"),
    )

    url: Mapped[str]
    name: Mapped[Optional[str]]

    type: Mapped[CollectorTargetType] = mapped_column(
        Enum(CollectorTargetType, create_constraint=True, name="collectortargettype"),
    )
    collector_id: Mapped[int] = mapped_column(ForeignKey(Collector.id))
    resource_id: Mapped[str] = mapped_column(index=True)
    last_collected: Mapped[Optional[int]] = mapped_column(BigInteger)
    team_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL")
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)

    config: Mapped[List["ConfigItem"]] = relationship(default_factory=list)


class ConfigItem(MetadataBase, ModelBase):
    """Config model class."""

    __tablename__ = "collector_target_config_items"
    __table_args__ = (UniqueConstraint("collector_target_id", "key"),)

    key: Mapped[str]
    value: Mapped[str]

    collector_target_id: Mapped[int] = mapped_column(
        ForeignKey(CollectorTarget.id, ondelete="CASCADE")
    )
