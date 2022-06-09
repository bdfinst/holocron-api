"""Holocron user model."""
from sqlalchemy import Boolean, Column, String

from ._base import MetadataBase, ModelBase


class User(MetadataBase, ModelBase):
    """Model class."""

    __tablename__ = "users"

    sso_id = Column(String, unique=True)
    username = Column(String, unique=True)
    is_org_leadership = Column(Boolean)
    is_admin = Column(Boolean)
