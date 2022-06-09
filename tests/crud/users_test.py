"""Users CRUD tests."""
from app.crud import users_crud
from tests.utils import first_argument


def test_upsert_sso_user(mock_session, mock_config):
    """Test upsert_sso_user method."""
    token = {"sub": "1", "username": "test", "groups": ["admin"]}

    result = users_crud.upsert_sso_user(mock_session, token)
    user = first_argument(mock_session.add)

    assert result == user
    assert user.sso_id == "1"
    assert user.username == "test"
    assert user.is_admin
    assert not user.is_org_leadership
