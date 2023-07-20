"""Mock for all cache modules."""
from typing import NamedTuple

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


class MetricsV2Tuple(NamedTuple):
    """Tuple for metrics object mock."""

    name: str
    id: int
    value_stream_name: str
    value_stream_id: int
    organization_name: str
    organization_id: int


result_v1 = {
    "name": "org_name_test",
    "valuestreams": [{"name": "vs_name_test", "teams": [{"name": "team_name_test"}]}],
}

result_v2 = [
    MetricsV2Schema().dump(
        MetricsV2Tuple(
            name="team_name_test",
            id=1,
            value_stream_name="vs_name_test",
            value_stream_id=1,
            organization_name="org_name_test",
            organization_id=1,
        )
    )
]

cache_v1 = MockCache(result_v1)
cache_v2 = MockCache(result_v2)
