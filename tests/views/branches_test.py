"""Branch view tests."""


def test_list_branches_for_team(client, mock_crud):
    """Test GET /api/v1/branches/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/branches/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_branch(client, mock_crud):
    """Test GET /api/v1/branches/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/branches/1")

    assert resp.json == expected
    assert resp.status_code == 200
