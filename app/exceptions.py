"""Custom exceptions."""


class HolocronIntegrityError(Exception):
    """Error for SQL integrity exceptions."""

    def __init__(self, field, value):
        """Initialize with dict to match marshmallow validation."""
        self.messages = {}
        self.messages[field] = value
        super().__init__(f"{field} - {value}")
