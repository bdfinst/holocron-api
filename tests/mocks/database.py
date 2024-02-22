"""Database mocks."""

from unittest.mock import MagicMock


class MockQuery:
    """Mock class to represent a query."""

    def __init__(self, statement):
        """Initialize with a statement."""
        self.statement = statement

    def where(self, condition):
        """Add a condition to the statement."""
        self.statement += f" WHERE {condition}"
        return self

    def offset(self, number):
        """Add an offset to the statement."""
        self.statement += f" OFFSET {number}"
        return self

    def limit(self, number):
        """Add a limit to the statement."""
        self.statement += f" LIMIT {number}"
        return self

    def all(self):
        """Return an array of MagicMocks with the statements."""
        mock = MagicMock()
        mock.statement = self.statement
        return [mock]

    def first(self):
        """Return statement."""
        mock = MagicMock()
        mock.statement = self.statement
        return mock

    def join(self, target_model, condition):
        """Mock for sqlalchemy join function."""
        self.statement += " " + f"JOIN {target_model.__tablename__} ON {condition}"
        return self


def mock_select(model):
    """Mock for sqlalchemy select function."""
    return MockQuery(f"SELECT * FROM {model.__tablename__}")


def mock_delete(model):
    """Mock for sqlalchemy delete function."""
    return MockQuery(f"DELETE FROM {model.__tablename__}")


class MockFunc:
    """Mock class to represent sqlalchemy.func class."""

    def count(self, column):
        """Mock for count method."""
        return MockQuery(f"SELECT COUNT(*) FROM {column}")


class MockDatabase:
    """Mock class to represent the database session."""

    scalars = MagicMock(side_effect=lambda x: x)
    execute = MagicMock(side_effect=lambda x: x)
    add = MagicMock()
    commit = MagicMock()
    refresh = MagicMock()
    close = MagicMock()
    rollback = MagicMock()

    def reset(self):
        """Reset the mocks."""
        self.scalars = MagicMock(side_effect=lambda x: x)
        self.execute = MagicMock(side_effect=lambda x: x)
        self.add = MagicMock()
        self.commit = MagicMock()
        self.refresh = MagicMock()
        self.close = MagicMock()
        self.rollback = MagicMock()


session = MockDatabase()
mock_func = MockFunc()
