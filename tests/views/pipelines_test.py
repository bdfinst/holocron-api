"""Pipeline view tests."""


def test_list_pipelines(client, mock_crud):
    """Test GET /api/v1/pipelines endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/pipelines")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_pipelines_for_team(client, mock_crud):
    """Test GET /api/v1/pipelines/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/pipelines/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_pipeline(client, mock_crud):
    """Test GET /api/v1/pipelines/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/pipelines/1")

    assert resp.json == expected
    assert resp.status_code == 200
