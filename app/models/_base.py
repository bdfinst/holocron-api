"""Base classes for migration metadata and model inheritance."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class MetadataBase(DeclarativeBase):
    """Class to hold model metadata."""


class ModelBase:
    """Class for model inheritance."""

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="NOW()"
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_onupdate="NOW()"  # type: ignore
    )
