"""API Spec."""
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flask import Flask


def generate_spec(app: Flask) -> APISpec:
    """Generate the API spec."""
    spec = APISpec(
        title="Holocron",
        version="1.0.0",
        openapi_version=app.config["SWAGGER"]["openapi"],
        plugins=[
            FlaskPlugin(),
            MarshmallowPlugin(),
        ],
    )

    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint == "static":
                continue
            spec.path(view=app.view_functions[rule.endpoint])

    return spec


def serve_spec(app: Flask, spec: APISpec):
    """Serve the API spec."""
    template = spec.to_flasgger(
        app,
    )
    swagger_config = Swagger.DEFAULT_CONFIG
    swagger_config["specs_route"] = "/api/v1"
    Swagger(
        app,
        template=template,
        config=swagger_config,
    )
