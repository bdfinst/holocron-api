"""Holocron collector target model."""
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from ._base import MetadataBase, ModelBase
from .collector import Collector
from .team import Team


class CollectorTarget(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "collector_targets"

    collector_id = Column(Integer, ForeignKey(Collector.id), nullable=False)
    team_id = Column(Integer, ForeignKey(Team.id, ondelete="SET NULL"))
    name = Column(String)
    url = Column(String, nullable=False)
    is_deleted = Column(Boolean, server_default="False")
    config = relationship("ConfigItem")
    last_collected = Column(BigInteger)

    UniqueConstraint(collector_id, url)


class ConfigItem(MetadataBase, ModelBase):
    """Config model class."""

    __tablename__ = "collector_target_config_items"

    collector_target_id = Column(
        Integer,
        ForeignKey(CollectorTarget.id, ondelete="CASCADE"),
        nullable=False,
    )
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    UniqueConstraint(collector_target_id, key)
