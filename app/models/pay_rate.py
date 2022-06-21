"""Holocron payrate model."""
from sqlalchemy import Column, Integer, String

from ._base import MetadataBase, ModelBase


class PayRate(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "pay_rates"

    rate = Column(Integer, nullable=False)
    persona = Column(String, unique=True, nullable=False)
