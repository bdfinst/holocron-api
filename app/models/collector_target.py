"""Holocron collector target model."""
from typing import List, Optional

from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import MetadataBase, ModelBase
from .collector import Collector


class CollectorTarget(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "collector_targets"
    __table_args__ = (UniqueConstraint("collector_id", "url"),)

    url: Mapped[str]
    name: Mapped[Optional[str]]

    collector_id: Mapped[int] = mapped_column(ForeignKey(Collector.id))
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
