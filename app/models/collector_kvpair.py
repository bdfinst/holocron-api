"""Collector KV Pair model."""
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase
from .collector import Collector


# This is just a model
# that is used by the collectors only to
# store any information related to a collector.
class CollectorKVPair(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "collector_kv_pairs"
    __table_args__ = (UniqueConstraint("collector_id", "key"),)

    key: Mapped[str]
    value: Mapped[str]

    collector_id: Mapped[int] = mapped_column(
        ForeignKey(Collector.id, ondelete="CASCADE")
    )
