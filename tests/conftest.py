"""Test fixtures and configuration."""

from unittest.mock import MagicMock

from pytest import MonkeyPatch, fixture

import app
from app import security, spec
from app.middleware import auth, circuit_breaker, log, rate_limiter, text_validator
from tests.mocks import mock_delete, mock_func, mock_select, request, session


@fixture(scope="session")
def session_patch():
    """Monkey patch at session scope."""
    monkey_patch = MonkeyPatch()
    yield monkey_patch
    monkey_patch.undo()


@fixture(scope="session", autouse=True)
def mock_sqlalchemy_base(session_patch):
    """Patch sqlalchemy."""
    session_patch.setattr(app.crud._base, "delete", mock_delete)
    session_patch.setattr(app.crud._base, "select", mock_select)
    session_patch.setattr(app.crud._base, "func", mock_func)
    session_patch.setattr(app.crud._base_metric, "select", mock_select)
    session_patch.setattr(app.crud._base_metric, "func", mock_func)


@fixture
def mock_session():
    """Yield mock database session."""
    yield session
    session.reset()


@fixture
def mock_request(monkeypatch):
    """Patch and yield mock request object."""
    monkeypatch.setattr(auth, "request", request)
    monkeypatch.setattr(log, "request", request)
    monkeypatch.setattr(security, "request", request)
    monkeypatch.setattr(rate_limiter, "request", request)
    monkeypatch.setattr(circuit_breaker, "request", request)
    monkeypatch.setattr(text_validator, "request", request)
    yield request
    request.reset()


@fixture
def application(monkeypatch):
    """Run application factory."""
    monkeypatch.setattr(app.app.Database, "establish_connection", MagicMock())
    monkeypatch.setattr(app.app, "organizations_cache_v2", MagicMock())
    monkeypatch.setattr(app.app, "set_user", MagicMock())
    monkeypatch.setattr(app.app, "atexit", MagicMock())
    monkeypatch.setattr(app.app, "BackgroundScheduler", MagicMock())
    monkeypatch.setattr(app.app.config, "FEATURE_FLAGS", {"FEATURE_API_V3": True})
    monkeypatch.setattr(
        app.routes.v2.teams, "FEATURE_FLAGS", {"FEATURE_TEAM_VIEWS": True}
    )
    monkeypatch.setattr(
        app.routes.v3.teams, "FEATURE_FLAGS", {"FEATURE_TEAM_VIEWS": True}
    )
    monkeypatch.setattr(
        app.routes.v2,
        "FEATURE_FLAGS",
        {
            "FEATURE_COST_METRICS": True,
            "FEATURE_EXTERNAL_CONTRIBUTORS": True,
            "FEATURE_COLLECTOR_CONFIGURATION": True,
        },
    )
    monkeypatch.setattr(
        app.routes.v3,
        "FEATURE_FLAGS",
        {
            "FEATURE_COST_METRICS": True,
            "FEATURE_EXTERNAL_CONTRIBUTORS": True,
            "FEATURE_COLLECTOR_CONFIGURATION": True,
        },
    )
    monkeypatch.setattr(spec, "schema_names", [])
    application = app.create_app()
    application.config.update({"TESTING": True})
    return application


@fixture
def client(application):
    """Test client."""
    return application.test_client()
