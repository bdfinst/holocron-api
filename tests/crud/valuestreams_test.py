"""Valuestream CRUD tests."""
from app.crud import valuestreams_crud
from tests.utils import first_argument


def test_create_entity(mock_session):
    """Test create_entity method."""
    json = {"name": "test", "organization_id": 1}

    result = valuestreams_crud.create_entity(mock_session, json)
    valuestream = first_argument(mock_session.add)

    assert valuestream.name == "test"
    assert valuestream.organization_id == 1
    assert result == valuestream


def test_update_entity(mock_session):
    """Test update_entity method."""
    expected = "SELECT * FROM valuestreams WHERE valuestreams.id = :id_1"
    json = {"name": "test", "organization_id": 1}

    result = valuestreams_crud.update_entity(mock_session, json, 1)
    valuestream = first_argument(mock_session.add)

    assert valuestream.name == "test"
    assert valuestream.organization_id == 1
    assert first_argument(mock_session.scalars).statement == expected
    assert result == valuestream
