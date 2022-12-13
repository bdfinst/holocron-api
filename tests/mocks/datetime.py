"""Mock datetime."""
from datetime import timezone


class MockDateTime:
    """Mock datetime."""

    def __init__(self, datetime):
        """Initialize with datetime."""
        self.datetime = datetime

    def now(self, timezone=timezone.utc):
        """Mock now function."""
        return self.datetime
