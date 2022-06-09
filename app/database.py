"""Establish database connection."""
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app import config


def build_connection_string():
    """Build database connection string."""
    return (
        f"postgresql://{config.DB_USER}:{config.DB_PASS}"
        + f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )


class Database:
    """Database static class."""

    engine: Engine = None

    @classmethod
    def establish_connection(cls):
        """Create database connection."""
        cls.engine = create_engine(build_connection_string())


@contextmanager
def generate_session():
    """Generate database session."""
    session = Session(Database.engine)
    try:
        yield session
    finally:
        session.close()
