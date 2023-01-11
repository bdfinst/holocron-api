"""Build instance model."""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.models.pipeline import Pipeline

from ._base import MetadataBase, ModelBase


class Build(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "builds"

    pipeline_id = Column(
        Integer, ForeignKey(Pipeline.id, ondelete="CASCADE"), nullable=False
    )
    build_url = Column(String, nullable=False, unique=True)
    build_status = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    is_deployed = Column(Boolean, server_default="False")
    passed_with_warnings = Column(Boolean, server_default="False")
