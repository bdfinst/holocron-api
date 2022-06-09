"""Valuestream view tests."""


def test_list_valuestreams(client, mock_crud):
    """Test GET /api/v1/valuestreams endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/valuestreams")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_valuestream(client, mock_crud):
    """Teset GET /api/v1/teams/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/valuestreams/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_create_valuestream(client, mock_crud):
    """Test POST /api/v1/valuestreams endpoint."""
    json = {"name": "test", "organizationId": 1}

    resp = client.post("/api/v1/valuestreams", json=json)

    assert resp.json == json
    assert resp.status_code == 201


def test_create_valuestream_400(client, mock_crud):
    """Test POST /api/v1/valuestreams endpoint."""
    json = {"name": "test", "extra": "field"}
    expected = {
        "organizationId": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.post("/api/v1/valuestreams", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_update_valuestream(client, mock_crud):
    """Test PUT /api/v1/valuestreams/1 endpoint."""
    json = {"name": "test", "organizationId": 1}
    expected = dict(id=1, **json)

    resp = client.put("/api/v1/valuestreams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 200


def test_update_valuestream_400(client, mock_crud):
    """Test PUT /api/v1/valuestreams/1 endpoint."""
    json = {"name": "test", "extra": "field"}
    expected = {
        "organizationId": ["Missing data for required field."],
        "extra": ["Unknown field."],
    }

    resp = client.put("/api/v1/valuestreams/1", json=json)

    assert resp.json == expected
    assert resp.status_code == 400


def test_delete_valuestream(client, mock_crud):
    """Test DELETE /api/v1/valuestreams/1/endpoint."""
    resp = client.delete("/api/v1/valuestreams/1")

    assert resp.text == ""
    assert resp.status_code == 204
