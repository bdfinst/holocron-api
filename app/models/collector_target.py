"""Holocron collector target model."""
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from ._base import MetadataBase, ModelBase
from .collector import Collector
from .team import Team


class CollectorTarget(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "collector_targets"

    collector_id = Column(Integer, ForeignKey(Collector.id), nullable=False)
    team_id = Column(Integer, ForeignKey(Team.id))
    name = Column(String)
    url = Column(String, nullable=False)
    api_url = Column(String)

    UniqueConstraint(collector_id, api_url)
