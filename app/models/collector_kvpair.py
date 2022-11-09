"""Collector KV Pair model."""
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from ._base import MetadataBase, ModelBase
from .collector import Collector


# This is just a model
# that is used by the collectors only to
# store any information related to a collector.
class CollectorKVPair(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "collector_kv_pairs"

    collector_id = Column(
        Integer, ForeignKey(Collector.id, ondelete="CASCADE"), nullable=False
    )
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    UniqueConstraint(collector_id, key)
