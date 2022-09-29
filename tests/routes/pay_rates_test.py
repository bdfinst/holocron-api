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
    json = {"rates": [{"rate": 1, "email": "bob@somemail.com"}]}

    resp = client.post("/api/v1/payrates", json=json)

    assert resp.json == {"result": [{"rate": 1, "email": "bob@somemail.com"}]}
    assert resp.status_code == 201


def test_upsert_payrate_business_logic_error(client, mock_crud):
    """Test POST /api/v1/payrates endpoint business logic errors."""
    invalid_input_cases = [
        (
            "Invalid rates field",
            {"extra": []},
            (
                400,
                {
                    "rates": ["Missing data for required field."],
                    "extra": ["Unknown field."],
                },
            ),
        ),
        (
            """No pay rate payload""",
            {"rates": []},
            (400, {"rates": ["Shorter than minimum length 1."]}),
        ),
        (
            """Pay rate less than or equal to 0""",
            {"rates": [{"rate": -1, "email": "bob@somemail.com"}]},
            (400, {"rates": {"0": {"rate": ["Must be greater than or equal to 1."]}}}),
        ),
        (
            """Invalid email field""",
            {"rates": [{"rate": 52, "email": "1335jadsfa?@sldaf914"}]},
            (400, {"rates": {"0": {"email": ["Not a valid email address."]}}}),
        ),
        (
            """Invalid email field (empty string)""",
            {"rates": [{"rate": 52, "email": ""}]},
            (400, {"rates": {"0": {"email": ["Not a valid email address."]}}}),
        ),
        (
            """Missing rate field""",
            {"rates": [{"email": "bob@someemail.com"}]},
            (400, {"rates": {"0": {"rate": ["Missing data for required field."]}}}),
        ),
        (
            """Duplicate email.""",
            {
                "rates": [
                    {"email": "bob@someemail.com", "rate": 1},
                    {"email": "bob@someemail.com", "rate": 2},
                ]
            },
            (400, {"rates": ["Duplicate email found in rates."]}),
        ),
    ]
    for t_case in invalid_input_cases:
        description, input_json, expected = t_case
        code, expected_json = expected

        resp = client.post("/api/v1/payrates", json=input_json)

        assert resp.json == expected_json, description
        assert resp.status_code == code, description


def test_upsert_payrate_validation_error(client, mock_crud):
    """Test POST /api/v1/payrates endpoint."""
    json = {"rates": [{"rate": 1, "extra": "field"}]}
    expected = {
        "rates": {
            "0": {
                "email": ["Missing data for required field."],
                "extra": ["Unknown field."],
            }
        }
    }

    resp = client.post("/api/v1/payrates", json=json)

    assert resp.json == expected
    assert resp.status_code == 400
