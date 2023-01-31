"""Holocron collector model."""
from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase


class Collector(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "collectors"

    target: Mapped[str]

    name: Mapped[str] = mapped_column(unique=True)
