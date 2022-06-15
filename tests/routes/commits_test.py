"""Commit route tests."""


def test_list_commits_for_team(client, mock_crud):
    """Test GET /api/v1/commits/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/commits/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_commit(client, mock_crud):
    """Test GET /api/v1/commits/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/commits/1")

    assert resp.json == expected
    assert resp.status_code == 200
