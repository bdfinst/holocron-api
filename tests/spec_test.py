"""OpenAPI spec tests."""

from flask import Flask
from openapi_spec_validator import validate_spec

from app import config, spec
from app.routes.v2 import create_v2_router
from app.routes.v3 import create_v3_router
from app.spec import generate_spec, patch_flasgger, resolve_schema_name


def test_spec_is_valid():
    """Validate the generated spec."""
    app = Flask(__name__)
    app.config.from_object(config)
    patch_flasgger()
    app.register_blueprint(create_v2_router())
    app.register_blueprint(create_v3_router())
    spec2 = generate_spec(app, "v2")
    spec3 = generate_spec(app, "v3")

    assert validate_spec(spec2.to_dict()) is None
    assert validate_spec(spec3.to_dict()) is None


class MockSchema:
    """Mock Schema object for resolve_schema_cls mock."""

    def __init__(self, name: str):
        """Initialize."""
        self.__name__ = name


def test_resolve_schema_name(monkeypatch):
    """Test resolve_schema_name function."""
    monkeypatch.setattr(spec, "resolve_schema_cls", lambda x: MockSchema(x))
    test_cases = [
        ("test", "test"),
        ("test", "test-1"),
        ("test", "test-2"),
        ("test-test", "test-test"),
        ("test-test", "test-test-1"),
        ("test-test", "test-test-2"),
        ("forced-10", "forced-10"),
        ("forced-10", "forced-11"),
    ]

    for case in test_cases:
        assert resolve_schema_name(case[0]) == case[1]
