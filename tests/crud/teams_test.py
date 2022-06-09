"""Team CRUD tests."""
from app.crud import teams_crud
from tests.utils import first_argument


def test_create_entity(mock_session):
    """Test create_entity method."""
    json = {
        "name": "test",
        "team_size": 1,
        "user_ids": [],
        "collector_target_ids": [],
        "valuestream_id": 1,
    }

    result = teams_crud.create_entity(mock_session, json)
    team = first_argument(mock_session.add)

    assert team.name == "test"
    assert team.team_size == 1
    assert team.users == []
    assert team.collector_targets == []
    assert team.valuestream_id == 1
    assert result == team


def test_update_entity(mock_session):
    """Test update_entity method."""
    expected = "SELECT * FROM teams WHERE teams.id = :id_1"
    json = {
        "name": "test",
        "team_size": 1,
        "user_ids": [],
        "collector_target_ids": [],
        "valuestream_id": 1,
    }

    result = teams_crud.update_entity(mock_session, json, 1)
    team = first_argument(mock_session.add)

    assert team.name == "test"
    assert team.team_size == 1
    assert team.users == []
    assert team.collector_targets == []
    assert team.valuestream_id == 1
    assert first_argument(mock_session.scalars).statement == expected
    assert result == team
