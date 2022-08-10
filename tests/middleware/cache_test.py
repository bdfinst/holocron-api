"""Cache tests."""
from unittest.mock import MagicMock

from marshmallow import Schema, fields

from app.middleware.cache import cache
from tests.mocks import crud
from tests.utils import first_argument


class MockSchema(Schema):
    """Mock schema class."""

    id = fields.Int()


mock_cache = cache.Cache(MockSchema(), crud, 0, MagicMock())  # type: ignore


def test_start(monkeypatch):
    """Test start method."""
    mock_thread = MagicMock()
    monkeypatch.setattr(cache, "Thread", mock_thread)

    mock_cache.start()

    mock_thread.assert_called_with(target=mock_cache._run_cache)


def test_get_entity():
    """Test get_entity method."""
    mock_cache.data[1] = "test"

    result = mock_cache.get_entity(1)

    assert result == "test"


def test_get_ids():
    """Test _get_ids method."""
    result = mock_cache._get_ids()

    assert list(result) == []


def test_set_cache():
    """Test _set_cache method."""
    mock_cache._set_cache(1)

    assert mock_cache.data[1] == {"id": 1}


def test_update_cache(monkeypatch):
    """Test _update_cache method."""
    mock_get_entities = MagicMock(return_value=[MagicMock(id=1)])
    mock_set_cache = MagicMock()
    monkeypatch.setattr(crud, "get_entities", mock_get_entities)
    monkeypatch.setattr(mock_cache, "_set_cache", mock_set_cache)

    mock_cache._update_cache()

    assert first_argument(mock_set_cache) == 1
