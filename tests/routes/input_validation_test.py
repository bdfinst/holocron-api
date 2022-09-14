"""Input validaton test for route schemas."""
from pytest import fixture

from app import config
from app.config import SECURITY_SETTINGS
from app.routes import organizations
from tests.mocks import crud


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(organizations, "organizations_crud", crud)
    mock_settings = SECURITY_SETTINGS.copy()
    mock_settings["MAX_INPUT_CHAR_LEN"] = 50
    monkeypatch.setattr(config, "SECURITY_SETTINGS", mock_settings)


def test_input_validators(client, mock_crud):
    """Test DELETE /api/v1/organizations for schema input validation."""
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
        json = {"name": organization_name}

        resp = client.post("/api/v1/organizations", json=json)

        assert resp.status_code == code, description
        assert resp.json == resp_json, description
