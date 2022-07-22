"""PayRates CRUD tests."""
from pytest import fixture

from app.crud import pay_rates, pay_rates_crud
from tests.mocks import mock_select
from tests.utils import first_argument


@fixture
def mock_sqlalchemy(monkeypatch):
    """Patch sqlalchemy."""
    monkeypatch.setattr(pay_rates, "select", mock_select)


def test_upsert_entity(mock_sqlalchemy, mock_session):
    """Test upsert_entity method."""
    data = {"rate": 1, "persona": "bob"}

    result = pay_rates_crud.upsert_entity(mock_session, data)
    pay_rate = first_argument(mock_session.add)

    assert result == pay_rate
    assert pay_rate.rate == 1
    assert pay_rate.persona == "bob"
