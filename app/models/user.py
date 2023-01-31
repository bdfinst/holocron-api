"""Holocron user model."""
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from ._base import MetadataBase, ModelBase


class User(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "users"

    is_org_leadership: Mapped[bool]
    is_admin: Mapped[bool]

    sso_id: Mapped[Optional[str]] = mapped_column(unique=True)
    username: Mapped[Optional[str]] = mapped_column(unique=True)
