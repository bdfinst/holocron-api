"""Business logic teams test."""
from unittest.mock import MagicMock

from pytest import fixture

from app import security
from app.crud import collector_targets_crud, ticket_boards_crud, valuestreams_crud
from app.exceptions import HolocronIntegrityError
from app.middleware import business_logic_teams
from app.middleware.business_logic_teams import (
    requires_valid_team_data,
    requires_valid_team_view_data,
)
from tests.mocks import request
from tests.testdata import (
    create_repository,
    create_team,
    create_ticket_board,
    create_valuestream,
)

team_json = {
    "name": "test",
    "teamSize": 1,
    "users": [],
    "collectorTargetIds": [21],
    "valuestreamId": 1,
}

team_view_json = {
    "name": "test",
    "collectorTargetIds": [21],
    "viewOwnerId": 1,
}


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(business_logic_teams, "request", request)
    monkeypatch.setattr(security, "request", request)
    yield request
    request.reset()


@fixture
def mock_collector_targets_crud(monkeypatch):
    """Mock collector target crud."""
    monkeypatch.setattr(
        collector_targets_crud,
        "get_entity",
        MagicMock(return_value=create_ticket_board()),
    )


@fixture
def mock_ticket_boards_crud(monkeypatch):
    """Mock ticket boards crud."""
    monkeypatch.setattr(
        ticket_boards_crud,
        "get_entity",
        MagicMock(return_value=create_ticket_board()),
    )


@fixture
def mock_valuestreams_crud(monkeypatch):
    """Mock valuestreams crud."""
    monkeypatch.setattr(
        valuestreams_crud,
        "get_entity",
        MagicMock(return_value=create_valuestream(teams=[create_team(name="foo-bar")])),
    )


def wrapped_test_func(*_, **__):
    """Mock function for wrapping decorators."""
    return "success"


def test_requires_valid_team_data_create(
    mock_request,
    mock_collector_targets_crud,
    mock_ticket_boards_crud,
    mock_valuestreams_crud,
):
    """Test requires_valid_team_data function create success."""
    setattr(mock_request, "json", team_json)
    assert requires_valid_team_data(wrapped_test_func)() == wrapped_test_func()


def test_requires_valid_team_data_404(
    mock_request, mock_collector_targets_crud, mock_ticket_boards_crud, monkeypatch
):
    """Test requires_valid_team_data function 404."""
    setattr(mock_request, "json", team_json)
    monkeypatch.setattr(
        valuestreams_crud,
        "get_entity",
        MagicMock(side_effect=HolocronIntegrityError("biz", "baz")),
    )
    assert requires_valid_team_data(wrapped_test_func)() == (
        "Resource not found",
        404,
    )


def test_requires_valid_team_data_create_invalid(mock_request, monkeypatch):
    """Test requires_valid_team_data with error cases."""
    setattr(mock_request, "json", team_json)

    test_cases = [
        (
            """should send 400 on collector targets already in use.""",
            (
                MagicMock(return_value=create_ticket_board(id=21, team_id=42)),
                MagicMock(return_value=create_ticket_board(id=21, team_id=42)),
                MagicMock(
                    return_value=create_valuestream(teams=[create_team(name="foo-bar")])
                ),
            ),
            ("collectorTargetIds - already in use", 400),
        ),
        (
            """should send 400 on team name already in use.""",
            (
                MagicMock(return_value=create_ticket_board()),
                MagicMock(return_value=create_ticket_board()),
                MagicMock(
                    return_value=create_valuestream(
                        teams=[create_team(name=team_json["name"])]
                    )
                ),
            ),
            ("name - already exists", 400),
        ),
    ]
    for test_case in test_cases:
        description, input_case, expected = test_case

        (
            get_entity_collector_targets_crud_mock,
            get_entity_ticket_boards_crud_mock,
            get_entity_valuestreams_crud_mock,
        ) = input_case
        monkeypatch.setattr(
            collector_targets_crud,
            "get_entity",
            get_entity_collector_targets_crud_mock,
        )
        monkeypatch.setattr(
            ticket_boards_crud,
            "get_entity",
            get_entity_ticket_boards_crud_mock,
        )
        monkeypatch.setattr(
            valuestreams_crud,
            "get_entity",
            get_entity_valuestreams_crud_mock,
        )

        assert requires_valid_team_data(wrapped_test_func)() == expected, description


def test_requires_valid_team_data_update(
    mock_request,
    mock_collector_targets_crud,
    mock_ticket_boards_crud,
    mock_valuestreams_crud,
):
    """Test requires_valid_team_data function update success."""
    setattr(mock_request, "json", team_json)
    assert (
        requires_valid_team_data(wrapped_test_func)(team_id="1") == wrapped_test_func()
    )


def test_requires_valid_team_data_update_invalid(mock_request, monkeypatch):
    """Test requires_valid_team_data function update invalid."""
    setattr(mock_request, "json", team_json)

    test_cases = [
        (
            """should send 400 on collector targets already in use.""",
            (
                MagicMock(return_value=create_ticket_board(id=21, team_id=42)),
                MagicMock(return_value=create_ticket_board(id=21, team_id=42)),
                MagicMock(
                    return_value=create_valuestream(teams=[create_team(name="foo-bar")])
                ),
            ),
            ("collectorTargetIds - already in use", 400),
        ),
        (
            """should send 400 on team name already in use.""",
            (
                MagicMock(return_value=create_ticket_board()),
                MagicMock(return_value=create_ticket_board()),
                MagicMock(
                    return_value=create_valuestream(
                        teams=[create_team(id=2, name=team_json["name"])]
                    )
                ),
            ),
            ("name - already exists", 400),
        ),
    ]
    for test_case in test_cases:
        description, input_case, expected = test_case

        (
            get_entity_collector_targets_crud_mock,
            get_entity_ticket_boards_crud_mock,
            get_entity_valuestreams_crud_mock,
        ) = input_case
        monkeypatch.setattr(
            collector_targets_crud,
            "get_entity",
            get_entity_collector_targets_crud_mock,
        )
        monkeypatch.setattr(
            ticket_boards_crud,
            "get_entity",
            get_entity_ticket_boards_crud_mock,
        )
        monkeypatch.setattr(
            valuestreams_crud,
            "get_entity",
            get_entity_valuestreams_crud_mock,
        )

        assert (
            requires_valid_team_data(wrapped_test_func)(team_id="1") == expected
        ), description


def test_requires_valid_team_view_data_create(
    mock_request,
    mock_collector_targets_crud,
    mock_ticket_boards_crud,
):
    """Test requires_valid_team_view_data function create success."""
    setattr(mock_request, "json", team_view_json)
    assert requires_valid_team_view_data(wrapped_test_func)() == wrapped_test_func()


def test_requires_valid_team_view_data_404(
    mock_request, mock_ticket_boards_crud, monkeypatch
):
    """Test requires_valid_team_view_data function 404."""
    setattr(mock_request, "json", team_view_json)
    monkeypatch.setattr(
        collector_targets_crud,
        "get_entity",
        MagicMock(side_effect=HolocronIntegrityError("id", "id not found")),
    )
    assert requires_valid_team_view_data(wrapped_test_func)() == (
        "Resource not found",
        404,
    )


def test_requires_valid_team_view_data_create_invalid(mock_request, monkeypatch):
    """Test requires_valid_team_view_data create with error cases."""
    setattr(mock_request, "json", team_view_json)
    test_cases = [
        (
            """should send 400 on collector targets already in use.""",
            (
                MagicMock(return_value=create_ticket_board(id=21, team_id=42)),
                MagicMock(return_value=create_ticket_board(id=21, team_id=42)),
            ),
            ("collectorTargetIds - already in use", 400),
        ),
    ]
    for test_case in test_cases:
        description, input_case, expected = test_case

        (
            get_entity_collector_targets_crud_mock,
            get_entity_ticket_boards_crud_mock,
        ) = input_case
        monkeypatch.setattr(
            collector_targets_crud,
            "get_entity",
            get_entity_collector_targets_crud_mock,
        )
        monkeypatch.setattr(
            ticket_boards_crud,
            "get_entity",
            get_entity_ticket_boards_crud_mock,
        )

        assert (
            requires_valid_team_view_data(wrapped_test_func)() == expected
        ), description


def test_requires_valid_team_view_data_update(
    mock_request,
    mock_collector_targets_crud,
    mock_ticket_boards_crud,
):
    """Test requires_valid_team_view_data function update success."""
    setattr(mock_request, "json", team_view_json)
    assert (
        requires_valid_team_view_data(wrapped_test_func)(team_view_id="1")
        == wrapped_test_func()
    )


def test_requires_valid_team_view_data_update_invalid(mock_request, monkeypatch):
    """Test requires_valid_team_view_data function update invalid."""
    setattr(mock_request, "json", team_view_json)

    test_cases = [
        (
            """should send 400 on collector targets already in use.""",
            (
                MagicMock(return_value=create_ticket_board(id=21, team_id=42)),
                MagicMock(return_value=create_ticket_board(id=21, team_id=42)),
            ),
            ("collectorTargetIds - already in use", 400),
        ),
    ]
    for test_case in test_cases:
        description, input_case, expected = test_case

        (
            get_entity_collector_targets_crud_mock,
            get_entity_ticket_boards_crud_mock,
        ) = input_case
        monkeypatch.setattr(
            collector_targets_crud,
            "get_entity",
            get_entity_collector_targets_crud_mock,
        )
        monkeypatch.setattr(
            ticket_boards_crud,
            "get_entity",
            get_entity_ticket_boards_crud_mock,
        )

        assert (
            requires_valid_team_view_data(wrapped_test_func)(team_view_id="1")
            == expected
        ), description
