"""OpenAPI spec tests."""
from unittest.mock import MagicMock

from flask import Flask
from openapi_spec_validator import decorators, validate_v3_spec, validators

from app import config
from app.routes.v1 import create_v1_router
from app.spec import generate_spec


def test_spec_is_valid(monkeypatch):
    """Validate the generated spec."""
    monkeypatch.setattr(validators.log, "debug", MagicMock())
    monkeypatch.setattr(decorators.log, "debug", MagicMock())

    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(create_v1_router())
    spec = generate_spec(app, "v1")

    assert validate_v3_spec(spec.to_dict()) is None
