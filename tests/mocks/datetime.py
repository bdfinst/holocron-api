"""Mock datetime."""


class MockDateTime:
    """Mock datetime."""

    def __init__(self, datetime):
        """Initialize with datetime."""
        self.datetime = datetime

    def now(self):
        """Mock now function."""
        return self.datetime
