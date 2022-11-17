"""Mock for all cache modules."""
from app.exceptions import HolocronIntegrityError
from app.middleware import SchemaCacheNotReady


class MockCache:
    """Mock cache class."""

    def start(self):
        """Mock start method."""

    def get_entity(self, id):
        """Mock get_entity method."""
        if id == -1:
            raise HolocronIntegrityError("err", "err")
        if id == 42:
            raise SchemaCacheNotReady("oops.")
        return {"id": id}


cache = MockCache()
