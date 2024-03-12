"""OpenAPI spec tests."""

from flask import Flask
from openapi_spec_validator import validate_spec

from app import config
from app.routes.v2 import create_v2_router
from app.spec import generate_spec, patch_flasgger


def test_spec_is_valid():
    """Validate the generated spec."""
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(create_v2_router())
    spec2 = generate_spec(app, "v2")
    spec3 = generate_spec(app, "v3")

    assert validate_spec(spec2.to_dict()) is None
    assert validate_spec(spec3.to_dict()) is None
