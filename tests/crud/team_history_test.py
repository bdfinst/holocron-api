"""Team History CRUD tests."""
from pytest import fixture

from app.crud import team_history
from app.crud.team_history import team_history_crud
from app.models import Team, TeamHistory
from tests.mocks import mock_select
from tests.utils import first_argument


@fixture
def mock_sqlalchemy(monkeypatch):
    """Patch sqlalchemy."""
    monkeypatch.setattr(team_history, "select", mock_select)


def test_create_entity(mock_session):
    """Test create entity."""
    team = Team(
        id=1,
        name="test",
        team_size=4,
        valuestream_id=1,
    )
    result: TeamHistory = team_history_crud.create_entity(mock_session, team)
    history = first_argument(mock_session.add)

    assert history.team_size == team.team_size
    assert history.team_id == team.id
    assert result == history


def test_get_entities_for_team(mock_sqlalchemy, mock_session):
    """Test get_entities_for_team method."""
    expected = "SELECT * FROM team_history " + "WHERE team_history.team_id = :team_id_1"

    result = team_history_crud.get_entities_for_team(mock_session, 1)

    assert result[0].statement == expected
