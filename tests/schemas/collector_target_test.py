"""CollectorTargetSchema method tests."""
from app.models import Pipeline, Repository, TicketBoard
from app.schemas.collector_target import CollectorTargetSchema

schema = CollectorTargetSchema()


def test_dump_pipeline():
    """Test dump using a pipeline."""
    target = [Pipeline(pipeline_id=1)]

    [result] = schema.dump(target)

    assert result.get("pipelineId") == 1
    assert result.get("repositoryId") is None
    assert result.get("boardId") is None


def test_dump_repository():
    """Test dump using a repository."""
    target = [Repository(repository_id=1)]

    [result] = schema.dump(target)

    assert result.get("repositoryId") == 1
    assert result.get("pipelineId") is None
    assert result.get("boardId") is None


def test_dump_ticket_board():
    """Test dump using a ticket board."""
    target = [TicketBoard(board_id=1)]

    [result] = schema.dump(target)

    assert result.get("boardId") == 1
    assert result.get("pipelineId") is None
    assert result.get("repositoryId") is None
