"""Holocron payrate model."""
from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase


class PayRate(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "pay_rates"

    rate: Mapped[float]

    email: Mapped[str] = mapped_column(unique=True)
