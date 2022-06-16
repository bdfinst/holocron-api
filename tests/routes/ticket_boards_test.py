"""TicketBoard route tests."""


def test_list_ticket_boards(client, mock_crud):
    """Test GET /api/v1/ticketboards endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/ticketboards")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_ticket_boards_for_team(client, mock_crud):
    """Test GET /api/v1/ticketboards/team/:id endpoint."""
    expected = {"result": []}

    resp = client.get("/api/v1/ticketboards/team/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_list_ticket_boards_for_team_404(client, mock_crud):
    """Test GET /api/v1/ticketboards/team/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/ticketboards/team/-1")

    assert resp.text == expected
    assert resp.status_code == 404


def test_get_ticket_board(client, mock_crud):
    """Test GET /api/v1/ticketboards/:id endpoint."""
    expected = {"id": 1}

    resp = client.get("/api/v1/ticketboards/1")

    assert resp.json == expected
    assert resp.status_code == 200


def test_get_ticket_board_404(client, mock_crud):
    """Test GET /api/v1/ticketboards/:id endpoint."""
    expected = "Resource not found"

    resp = client.get("/api/v1/ticketboards/-1")

    assert resp.text == expected
    assert resp.status_code == 404
