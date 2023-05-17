"""Test fixtures and configuration."""
import warnings
from unittest.mock import MagicMock

from pytest import MonkeyPatch, fixture

import app
from tests.mocks import mock_delete, mock_select, session


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
    session_patch.setattr(app.crud._base_metric, "select", mock_select)


@fixture
def mock_session():
    """Yield mock database session."""
    yield session
    session.reset()


@fixture
def application(monkeypatch):
    """Run application factory."""
    warnings.filterwarnings("ignore", message="Multiple schemas resolved to the name")
    monkeypatch.setattr(app.app.Database, "establish_connection", MagicMock())
    monkeypatch.setattr(app.app, "organizations_cache", MagicMock())
    monkeypatch.setattr(app.app, "set_user", MagicMock())
    monkeypatch.setattr(app.app, "atexit", MagicMock())
    monkeypatch.setattr(app.app, "BackgroundScheduler", MagicMock())
    monkeypatch.setattr(app.routes.teams, "FEATURE_FLAGS", {"FEATURE_TEAM_VIEWS": True})
    monkeypatch.setattr(
        app.routes,
        "FEATURE_FLAGS",
        {"FEATURE_COST_METRICS": True, "FEATURE_EXTERNAL_CONTRIBUTORS": True},
    )
    application = app.create_app()
    application.config.update({"TESTING": True})
    return application


@fixture
def client(application):
    """Test client."""
    return application.test_client()
