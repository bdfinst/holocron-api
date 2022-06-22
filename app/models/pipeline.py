"""Build pipeline model."""
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .collector_target import CollectorTarget


class Pipeline(CollectorTarget):
    """Model class."""

    pipeline_id = Column(Integer, index=True)
    builds = relationship("Build")
