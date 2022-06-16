"""Git Request route tests."""


def test_list_git_requests_for_team(client, mock_crud):
    """Test GET /api/v1/gitrequests/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/gitrequests/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_get_requests_for_team_404(client, mock_crud):
    """Test GET /api/v1/gitrequests/team/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/gitrequests/team/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_git_request(client, mock_crud):
    """Test GET /api/v1/gitrequests/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/gitrequests/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_git_request_404(client, mock_crud):
    """Test GET /api/v1/gitrequests/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/gitrequests/-1")

    assert resp.text == expected
    assert resp.status_code == 404
