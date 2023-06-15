"""Mock for all cache modules."""
from app.exceptions import HolocronIntegrityError
from app.middleware import SchemaCacheNotReady
from app.schemas.v2 import MetricsV2Schema


class MockCache:
    """Mock cache class."""

    def __init__(self, result):
        """Initialize."""
        self.result = result

    def start(self):
        """Mock start method."""

    def get_entity(self, id):
        """Mock get_entity method."""
        if id == -1:
            raise HolocronIntegrityError("err", "err")
        if id == 42:
            raise SchemaCacheNotReady("oops.")
        return self.result


result_v1 = {
    "name": "org_name_test",
    "valuestreams": [{"name": "vs_name_test", "teams": [{"name": "team_name_test"}]}],
}

result_v2 = [
    MetricsV2Schema().load(
        {
            "name": "team_name_test",
            "id": 1,
            "valueStreamName": "vs_name_test",
            "valueStreamId": 1,
            "organizationName": "org_name_test",
            "organizationId": 1,
        }
    )
]

cache_v1 = MockCache(result_v1)
cache_v2 = MockCache(result_v2)
