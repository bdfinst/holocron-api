"""Builds route tests."""


def test_list_builds_for_team(client, mock_crud):
    """Test GET /api/v1/builds/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/builds/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_build(client, mock_crud):
    """Test GET /api/v1/builds/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/builds/1")

    assert resp.json == expected
    assert resp.status_code == 200
