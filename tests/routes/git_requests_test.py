"""Git Request route tests."""


def test_list_git_requests_for_team(client, mock_crud):
    """Test GET /api/v1/gitrequests/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/gitrequests/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_git_request(client, mock_crud):
    """Test GET /api/v1/gitrequests/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/gitrequests/1")

    assert resp.json == expected
    assert resp.status_code == 200
