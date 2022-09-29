"""Holocron payrate model."""
from sqlalchemy import Column, Float, String

from ._base import MetadataBase, ModelBase


class PayRate(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "pay_rates"

    rate = Column(Float, nullable=False)
    email = Column(String, unique=True, nullable=False)
