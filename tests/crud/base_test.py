"""Tests for base CRUD classes."""
import pytest

from app.crud._base import BaseCRUD, BaseMetricCRUD
from app.models import MetadataBase, ModelBase, Pipeline, Repository, TicketBoard
from tests.utils import first_argument


class ValidModel(MetadataBase, ModelBase):
    """Mock model class."""

    __tablename__ = "models"

    repository_id = 0
    pipeline_id = 0
    board_id = 0


class InvalidModel(ModelBase):
    """Mock model class missing required fields."""


# BaseCRUD


class ModelCRUD(BaseCRUD[ValidModel]):
    """Mock CRUD class for mock model."""


test_crud = ModelCRUD(ValidModel)


def test_get_entities(mock_session):
    """Test get_entities method."""
    expected = "SELECT * FROM models"

    result = test_crud.get_entities(mock_session)

    assert result[0].statement == expected


def test_get_entity(mock_session):
    """Test get_entity method."""
    expected = "SELECT * FROM models WHERE models.id = :id_1"

    result = test_crud.get_entity(mock_session, 1)

    assert result.statement == expected


def test_delete_entity(mock_session):
    """Test delete_entity method."""
    expected = "DELETE FROM models WHERE models.id = :id_1"

    test_crud.delete_entity(mock_session, 1)

    assert first_argument(mock_session.execute).statement == expected


# BaseMetricCRUD


class CRUDClass(BaseMetricCRUD[ValidModel]):
    """Mock Metric CRUD class for mock model."""

    pass


def test_init_repository():
    """Test __init__ method with repository target."""
    try:
        instance = CRUDClass(ValidModel, Repository)
    except Exception as e:
        assert False, f"Exception raised during initialization: {e}"

    assert instance.id_field == "repository_id"


def test_init_pipeline():
    """Test __init__ method with pipeline target."""
    try:
        instance = CRUDClass(ValidModel, Pipeline)
    except Exception as e:
        assert False, f"Exception raised during initialization: {e}"

    assert instance.id_field == "pipeline_id"


def test_init_ticket_board():
    """Test __init__ method with ticket board target."""
    try:
        instance = CRUDClass(ValidModel, TicketBoard)
    except Exception as e:
        assert False, f"Exception raised during initialization: {e}"

    assert instance.id_field == "board_id"


def test_init_invalid_target():
    """Test __init__ method with invalid target."""
    with pytest.raises(ValueError) as e:
        CRUDClass(ValidModel, InvalidModel)
    assert "Target model is not a CollectorTarget type" in str(e.value)


def test_init_invalid_model():
    """Test __init__ method with invalid model."""
    with pytest.raises(TypeError) as e:
        CRUDClass(InvalidModel, Repository)
    assert "has no attribute repository_id" in str(e.value)


def test_get_entities_for_team(mock_session):
    """Test get_entities_for_team method."""
    expected = (
        "SELECT * FROM models JOIN collector_targets ON collector_targets.id = :id_1 "
        + "WHERE collector_targets.team_id = :team_id_1"
    )
    instance = CRUDClass(ValidModel, Repository)

    result = instance.get_entities_for_team(mock_session, 1)

    assert result[0].statement == expected
