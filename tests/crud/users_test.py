"""Users CRUD tests."""
from unittest.mock import MagicMock

from pytest import fixture
from sqlalchemy.exc import IntegrityError

from app.crud import users, users_crud
from tests.mocks import config, mock_select
from tests.utils import first_argument


def raise_error(call_tracker=[]):
    """Raise error on first call and not on second."""
    if len(call_tracker) == 0:
        call_tracker.append("called")
        raise IntegrityError(
            "psycopg2.errors.UniqueViolation users_username_key", "", ""
        )


@fixture
def mock_config(monkeypatch):
    """Mock configuration."""
    monkeypatch.setattr(users, "config", config)


@fixture
def mock_sqlalchemy(monkeypatch):
    """Patch sqlalchemy."""
    monkeypatch.setattr(users, "select", mock_select)


def test_upsert_sso_user(mock_sqlalchemy, mock_session, mock_config):
    """Test upsert_sso_user method."""
    token = {"sub": "1", "username": "test", "groups": ["admin"]}

    result = users_crud.upsert_sso_user(mock_session, token)
    user = first_argument(mock_session.add)

    assert result == user
    assert user.sso_id == "1"
    assert user.username == "test"
    assert user.is_admin
    assert not user.is_org_leadership


def test_upsert_sso_user_username_conflict(mock_sqlalchemy, mock_session, mock_config):
    """Test upsert_sso_user method."""
    mock_session.add = MagicMock(side_effect=lambda x: raise_error())
    token = {"sub": "1", "username": "test", "groups": ["admin"]}

    result = users_crud.upsert_sso_user(mock_session, token)
    user = first_argument(mock_session.add)

    assert result == user
    assert user.sso_id == "1"
    assert user.username == "test1"
    assert user.is_admin
    assert not user.is_org_leadership
