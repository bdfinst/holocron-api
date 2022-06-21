"""PayRates CRUD tests."""
from app.crud import pay_rates_crud
from tests.utils import first_argument


def test_upsert_entity(mock_session, mock_config):
    """Test upsert_entity method."""
    data = {"rate": 1, "persona": "bob"}

    result = pay_rates_crud.upsert_entity(mock_session, data)
    pay_rate = first_argument(mock_session.add)

    assert result == pay_rate
    assert pay_rate.rate == 1
    assert pay_rate.persona == "bob"
