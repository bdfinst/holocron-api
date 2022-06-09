"""Base classes for migration metadata and model inheritance."""
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

MetadataBase = declarative_base()


class ModelBase:
    """Class for model inheritance."""

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
