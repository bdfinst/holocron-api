"""Pipelines CRUD tests."""
from app.crud import pipelines_crud


def test_get_entities(mock_session):
    """Test get_entities method."""
    expected = (
        "SELECT * FROM collector_targets "
        + "WHERE collector_targets.pipeline_id IS NOT NULL"
    )

    result = pipelines_crud.get_entities(mock_session)

    assert result[0].statement == expected


def test_get_entities_for_team(mock_session):
    """Test get_entities_for_team method."""
    expected = (
        "SELECT * FROM collector_targets "
        + "WHERE collector_targets.team_id = :team_id_1 "
        + "WHERE collector_targets.pipeline_id IS NOT NULL"
    )

    result = pipelines_crud.get_entities_for_team(mock_session, 1)

    assert result[0].statement == expected
