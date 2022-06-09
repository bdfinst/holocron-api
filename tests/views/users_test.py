"""User view tests."""


def test_list_users(client, mock_crud):
    """Test GET /api/v1/users endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/users")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_user(client, mock_crud):
    """Test GET /api/v1/users/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/users/1")

    assert resp.json == expected
    assert resp.status_code == 200
