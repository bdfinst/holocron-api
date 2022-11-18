"""Cache tests."""
from unittest.mock import MagicMock

from marshmallow import Schema, fields
from pytest import raises

from app.middleware import SchemaCache, SchemaCacheNotReady
from tests.mocks import crud
from tests.utils import first_argument


class MockSchema(Schema):
    """Mock schema class."""

    id = fields.Int()


mock_cache = SchemaCache(MockSchema(), crud, MagicMock())


def test_get_entity():
    """Test get_entity method."""
    mock_cache.data[1] = "test"

    result = mock_cache.get_entity(1)

    assert result == "test"


def test_get_entity_not_found():
    """Test get_entity method not found case."""
    with raises(SchemaCacheNotReady) as _:
        mock_cache.get_entity(2)


def test_get_ids():
    """Test _get_ids method."""
    result = mock_cache._get_ids()

    assert list(result) == []


def test_set_cache():
    """Test _set_cache method."""
    mock_cache._set_cache(1)

    assert mock_cache.data[1] == {"id": 1}


def test_run_cache(monkeypatch):
    """Test run method."""
    mock_get_entities = MagicMock(return_value=[MagicMock(id=1)])
    mock_set_cache = MagicMock()
    monkeypatch.setattr(crud, "get_entities", mock_get_entities)
    monkeypatch.setattr(mock_cache, "_set_cache", mock_set_cache)

    mock_cache.run()

    assert first_argument(mock_set_cache) == 1
