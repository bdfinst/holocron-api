"""Input validaton test for route schemas."""

from pytest import fixture

from app import security
from app.routes.v2 import organizations
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(organizations, "organizations_crud", crud)
    monkeypatch.setattr(security, "MAX_INPUT_CHAR_LEN", 50)


def test_input_validators(client, mock_crud, mock_request):
    """Test POST /api/v2/organizations for schema input validation."""
    test_cases = [
        (
            """should disallow characters that exceed max char""",
            "somereallylongorganizationnameeeeeeeeeeeeeeeeeeeeeee",
            (400, {"name": ["Exceeds max char limit."]}),
        ),
        (
            """should disallow all spaces""",
            "                              ",
            (400, {"name": ["String does not match expected pattern."]}),
        ),
        (
            """should disallow empty characters""",
            "",
            (400, {"name": ["String does not match expected pattern."]}),
        ),
        (
            """should disallow invalid regex characters""",
            "os.list()",
            (400, {"name": ["String does not match expected pattern."]}),
        ),
        (
            """should allow name with spaces and valid characters""",
            "49ers9- _Example",
            (201, {"name": "49ers9- _Example"}),
        ),
    ]
    for test_case in test_cases:
        description, organization_name, expected = test_case
        code, resp_json = expected
        json = {"name": organization_name, "userIds": [1]}

        resp = client.post("/api/v2/organizations", json=json)

        assert resp.status_code == code, description
        assert resp.json == resp_json, description
