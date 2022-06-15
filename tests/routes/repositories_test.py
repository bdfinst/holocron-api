"""Repository route tests."""


def test_list_repositories(client, mock_crud):
    """Test GET /api/v1/repositories endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/repositories")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_repositories_for_team(client, mock_crud):
    """Test GET /api/v1/repositories/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/repositories/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_repository(client, mock_crud):
    """Test GET /api/v1/repositories/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/repositories/1")

    assert resp.json == expected
    assert resp.status_code == 200
