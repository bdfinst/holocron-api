"""Member route tests."""
from pytest import fixture

from app import security
from app.middleware import auth, log
from app.routes.v2 import members
from tests.mocks import crud, request


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(members, "members_crud", crud)
    monkeypatch.setattr(members, "teams_crud", crud)
    monkeypatch.setattr(members, "teams_members_crud", crud)


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(auth, "request", request)
    monkeypatch.setattr(log, "request", request)
    monkeypatch.setattr(security, "request", request)
    yield request
    request.reset()


@fixture
def mock_admin(monkeypatch, mock_request):
    """Mock an admin user."""
    monkeypatch.setattr(auth, "SSO_ENABLED", True)
    setattr(mock_request, "user", {"isAdmin": True, "id": 1, "username": "t"})


def test_list_members(client, mock_crud, mock_admin):
    """Test GET /api/v2/members."""
    expected = {"result": []}

    resp = client.get("/api/v2/members")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_member(client, mock_crud, mock_admin):
    """Test GET /api/v2/members/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v2/members/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_member_404(client, mock_crud, mock_admin):
    """Test GET /api/v2/members/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v2/members/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_update_team_members(client, mock_crud, mock_admin):
    """Test PUT /api/v2/members/team/:id endpoint."""
    json = {
        "teamMembers": [
            {
                "startDate": "2020-01-01T00:00:00.000Z",
                "member": {
                    "name": "test",
                    "username": "test",
                },
            }
        ]
    }
    expected = {"id": 1}

    resp = client.put("/api/v2/members/team/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_team_members_validation_error(client, mock_crud, mock_admin):
    """Test PUT /api/v2/members/team/:id endpoint."""
    json = {
        "teamMembers": [
            {
                "startDate": "2020-01-01",
                "extra": "field",
                "member": {"username": "test"},
            }
        ],
    }
    expected = {
        "extra": ["Unknown field."],
        "startDate": ["Not a valid datetime."],
        "member": {"name": ["Missing data for required field."]},
    }

    resp = client.put("/api/v2/members/team/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_team_members_database_error(client, mock_crud, mock_admin):
    """Test PUT /api/v2/members/team/:id endpoint."""
    json = {
        "teamMembers": [
            {
                "startDate": "2020-01-01T00:00:00.000Z",
                "member": {
                    "name": "test",
                    "username": "test",
                },
            }
        ]
    }
    expected = {"err": "err"}

    resp = client.put("/api/v2/members/team/-1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400
