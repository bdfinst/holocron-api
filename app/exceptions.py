"""Custom exceptions."""


class HolocronError(Exception):
    """Error for generic exceptions."""


class HolocronIntegrityError(Exception):
    """Error for SQL integrity exceptions."""

    def __init__(self, field: str, value: str):
        """Initialize with dict to match marshmallow validation."""
        self.messages = {field: value}
        super().__init__(f"{field} - {value}")
