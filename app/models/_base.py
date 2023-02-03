"""Base classes for migration metadata and model inheritance."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column
from sqlalchemy.sql.expression import func


class MetadataBase(DeclarativeBase):
    """Class to hold model metadata."""


class ModelBase(MappedAsDataclass, kw_only=True):
    """Class for model inheritance."""

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="NOW()", init=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        # false positive
        # pylint: disable-next=not-callable
        onupdate=func.current_timestamp(),
        init=False,
    )
