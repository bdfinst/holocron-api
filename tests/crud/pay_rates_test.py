"""PayRates CRUD tests."""
from unittest.mock import MagicMock

from pytest import fixture

from app.crud import pay_rates, pay_rates_crud
from tests.mocks import mock_select
from tests.utils import first_argument

json = {"rate": 1, "email": "bob@somemail.com"}


@fixture
def mock_sqlalchemy(monkeypatch):
    """Patch sqlalchemy."""
    monkeypatch.setattr(pay_rates, "select", mock_select)


def test_upsert_entity_create(mock_sqlalchemy, mock_session):
    """Test upsert_entity method create."""
    mock_scalars_return = MagicMock(first=lambda *_, **__: None)
    mock_session.scalars = MagicMock(return_value=mock_scalars_return)

    result = pay_rates_crud.upsert_entity(mock_session, json)
    pay_rate = first_argument(mock_session.add)

    assert result == pay_rate
    assert pay_rate.rate == 1
    assert pay_rate.email == "bob@somemail.com"


def test_upsert_entity_update(mock_sqlalchemy, mock_session):
    """Test upsert_entity method update."""
    result = pay_rates_crud.upsert_entity(mock_session, json)
    pay_rate = first_argument(mock_session.add)

    assert result == pay_rate
    assert pay_rate.rate == 1
    assert pay_rate.email == "bob@somemail.com"
