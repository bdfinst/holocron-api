"""Organization CRUD tests."""
from app.crud import organizations_crud
from tests.utils import first_argument


def test_create_entity(mock_session):
    """Test create_entity method."""
    json = {"name": "test"}

    result = organizations_crud.create_entity(mock_session, json)
    organization = first_argument(mock_session.add)

    assert organization.name == "test"
    assert result == organization


def test_update_entity(mock_session):
    """Test update_entity method."""
    expected = "SELECT * FROM organizations WHERE organizations.id = :id_1"
    json = {"name": "test"}

    result = organizations_crud.update_entity(mock_session, json, 1)
    organization = first_argument(mock_session.add)

    assert organization.name == "test"
    assert first_argument(mock_session.scalars).statement == expected
    assert result == organization
