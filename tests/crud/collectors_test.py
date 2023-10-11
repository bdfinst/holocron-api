"""Collector CRUD tests."""
from unittest.mock import MagicMock

from pytest import fixture, raises
from sqlalchemy.exc import IntegrityError

from app.crud import collectors_crud
from app.exceptions import HolocronIntegrityError
from app.models import Collector
from tests.utils import first_argument

json = {
    "target": "targetvalue",
    "access_token": "accesstoken",
    "target_url": "targeturl",
    "collector_name": "collectorname",
    "collector_interval_seconds": "collectorintervalseconds",
    "look_back_days": "lookbackdays",
    "collector_targets_intrvl_secs": "collectortargetsintrvlsecs",
    "max_requests_per_minute": "maxrequestsperminute",
}


@fixture
def mock_collector_crud(monkeypatch):
    """Mock collector crud."""
    monkeypatch.setattr(
        collectors_crud,
        "get_entity",
        MagicMock(
            return_value=Collector(
                target="",
                access_token="",
                target_url="",
                collector_name="",
                collector_interval_seconds="",
                look_back_days="",
                collector_targets_intrvl_secs="",
                max_requests_per_minute="",
                name="name",
            )
        ),
    )


def test_update_entity(mock_session, mock_collector_crud):
    """Test update_entity method."""
    expected_value = Collector(
        target="targetvalue",
        access_token="accesstoken",
        target_url="targeturl",
        collector_name="collectorname",
        collector_interval_seconds="collectorintervalseconds",
        look_back_days="lookbackdays",
        collector_targets_intrvl_secs="collectortargetsintrvlsecs",
        max_requests_per_minute="maxrequestsperminute",
        name="name",
    )

    collector_result = collectors_crud.update_entity(mock_session, json, 1)
    collector = first_argument(mock_session.add)

    assert collector == expected_value
    assert collector_result == expected_value


def test_update_entity_unknown_error(mock_session):
    """Test update_entity with an unknown error."""

    def raise_integrity_error(*args, **kwargs):
        raise IntegrityError("unknown", None, None)

    mock_session.add = MagicMock(side_effect=raise_integrity_error)
    expected = "unknown - unknown, see logs"

    with raises(HolocronIntegrityError) as e:
        collectors_crud.update_entity(mock_session, json, 1)

    assert expected == str(e.value)
