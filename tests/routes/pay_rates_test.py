"""PayRates route tests."""
from pytest import fixture

from app.routes import pay_rates
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(pay_rates, "pay_rates_crud", crud)


def test_list_pay_rates(client, mock_crud):
    """Test GET /api/v1/payrates endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/payrates")

    assert resp.json == expected
    assert resp.status_code == 200


def test_upsert_payrate(client, mock_crud):
    """Test POST /api/v1/payrates endpoint."""
    json = {"rate": 1, "persona": "bob"}

    resp = client.post("/api/v1/payrates", json=json)

    assert resp.json == json
    assert resp.status_code == 201


def test_upsert_payrate_validation_error(client, mock_crud):
    """Test POST /api/v1/payrates endpoint."""
    json = {"rate": 1, "extra": "field"}
    expected = {
        "persona": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.post("/api/v1/payrates", json=json)

    assert resp.json == expected
    assert resp.status_code == 400
