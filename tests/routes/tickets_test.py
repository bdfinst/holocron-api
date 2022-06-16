"""Ticket route tests."""


def test_list_tickets_for_team(client, mock_crud):
    """Test GET /api/v1/tickets/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/tickets/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_tickets_for_team_404(client, mock_crud):
    """Test GET /api/v1/tickets/team/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/tickets/team/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_ticket(client, mock_crud):
    """Test GET /api/v1/tickets/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/tickets/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_ticket_404(client, mock_crud):
    """Test GET /api/v1/tickets/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/tickets/-1")

    assert resp.text == expected
    assert resp.status_code == 404
