"""Tests for base CRUD classes."""
import pytest
from pytest import fixture

from app.crud import _base_metric
from app.crud._base import BaseCRUD
from app.crud._base_metric import BaseMetricCRUD
from app.exceptions import HolocronIntegrityError
from app.models import MetadataBase, ModelBase, Pipeline, Repository, TicketBoard
from tests.mocks import crud
from tests.utils import first_argument


@fixture
def mock_crud(monkeypatch):
    """Mock CRUDs."""
    monkeypatch.setattr(_base_metric, "teams_crud", crud)


class ValidModel(MetadataBase, ModelBase):
    """Mock model class."""

    __tablename__ = "models"

    repository_id = 0
    pipeline_id = 0
    board_id = 0


class InvalidModel(MetadataBase, ModelBase):
    """Mock model class missing required fields."""

    __tablename__ = "invalid_models"


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


def test_init_invalid_model():
    """Test __init__ method with invalid model."""
    with pytest.raises(TypeError) as e:
        CRUDClass(InvalidModel, Repository, "repository_id")
    assert "has no attribute repository_id" in str(e.value)


def test_get_entities_for_team_invalid_team(mock_session, mock_crud):
    """Test get_entities_for_team method with invalid team."""
    with pytest.raises(HolocronIntegrityError) as e:
        instance = CRUDClass(ValidModel, Repository, "repository_id")
        instance.get_entities_for_team(mock_session, -1)
    assert "err - err" in str(e.value)


def test_get_entities_for_team(mock_session):
    """Test get_entities_for_team method with valid team."""
    expected = (
        "SELECT * FROM models JOIN collector_targets ON collector_targets.id = :id_1 "
        + "WHERE collector_targets.team_id = :team_id_1"
    )
    instance = CRUDClass(ValidModel, Repository, "repository_id")

    result = instance.get_entities_for_team(mock_session, 1)

    assert result[0].statement == expected
