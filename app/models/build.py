"""Build instance model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

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
    jobs = relationship("Job", lazy="subquery")


class Job(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "holocron_jobs"

    build_id = Column(Integer, ForeignKey(Build.id, ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    stage = Column(String, nullable=False)
    job_id = Column(Integer, nullable=False)
    job_url = Column(String, unique=True, nullable=False)
