"""Test fixtures and configuration."""
from unittest.mock import MagicMock

from pytest import MonkeyPatch, fixture

import app
from tests.mocks import config, crud, mock_delete, mock_select, request, session


@fixture(scope="session")
def session_patch():
    """Monkey patch at session scope."""
    monkey_patch = MonkeyPatch()
    yield monkey_patch
    monkey_patch.undo()


@fixture(scope="session", autouse=True)
def mock_sqlalchemy(session_patch):
    """Patch sqlalchemy functions."""
    session_patch.setattr(app.crud._base, "delete", mock_delete)
    session_patch.setattr(app.crud._base, "select", mock_select)


@fixture
def mock_session(monkeypatch):
    """Patch sqlalchemy and yield mock database session."""
    monkeypatch.setattr(app.crud.pay_rates, "select", mock_select)
    monkeypatch.setattr(app.crud.pipelines, "select", mock_select)
    monkeypatch.setattr(app.crud.repositories, "select", mock_select)
    monkeypatch.setattr(app.crud.ticket_boards, "select", mock_select)
    monkeypatch.setattr(app.crud.users, "select", mock_select)

    yield session
    session.reset()


@fixture
def mock_crud(monkeypatch):
    """Patch CRUD."""
    monkeypatch.setattr(app.middleware.auth, "users_crud", crud)
    monkeypatch.setattr(app.routes.branches, "branches_crud", crud)
    monkeypatch.setattr(app.routes.builds, "builds_crud", crud)
    monkeypatch.setattr(app.routes.commits, "commits_crud", crud)
    monkeypatch.setattr(app.routes.git_requests, "git_requests_crud", crud)
    monkeypatch.setattr(app.routes.organizations, "organizations_crud", crud)
    monkeypatch.setattr(app.routes.pay_rates, "pay_rates_crud", crud)
    monkeypatch.setattr(app.routes.pipelines, "pipelines_crud", crud)
    monkeypatch.setattr(app.routes.repositories, "repositories_crud", crud)
    monkeypatch.setattr(app.routes.ticket_boards, "ticket_boards_crud", crud)
    monkeypatch.setattr(app.routes.tickets, "tickets_crud", crud)
    monkeypatch.setattr(app.routes.teams, "teams_crud", crud)
    monkeypatch.setattr(app.routes.users, "users_crud", crud)
    monkeypatch.setattr(app.routes.valuestreams, "valuestreams_crud", crud)
    return crud


@fixture
def mock_config(monkeypatch):
    """Mock configuration."""
    monkeypatch.setattr(app.crud.users, "config", config)
    return config


@fixture
def mock_request(monkeypatch):
    """Mock request object."""
    monkeypatch.setattr(app.middleware.auth, "request", request)
    monkeypatch.setattr(app.middleware.log, "request", request)
    monkeypatch.setattr(app.middleware.circuit_breaker, "request", request)
    return request


@fixture
def application(monkeypatch):
    """Run application factory."""
    monkeypatch.setattr(app.app.Database, "establish_connection", MagicMock())
    monkeypatch.setattr(app.app, "set_user", MagicMock())
    application = app.create_app()
    application.config.update({"TESTING": True})
    return application


@fixture
def client(application):
    """Test client."""
    return application.test_client()
