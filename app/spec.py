"""API Spec."""

import re
from typing import List

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec.ext.marshmallow.common import resolve_schema_cls
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flask import Flask
from marshmallow import Schema

from app.config import FEATURE_FLAGS

schema_names: List[str] = []


def resolve_schema_name(schema: type[Schema]) -> str:
    """Append '-num' for conflicting schema names."""
    schema_name = resolve_schema_cls(schema).__name__  # type: ignore
    schema_name = schema_name.removesuffix("Schema")
    while schema_name in schema_names:
        existing_suffix = re.search(r"-\d+$", schema_name)
        num = (
            int(schema_name[existing_suffix.start() + 1 : existing_suffix.end()]) + 1
            if existing_suffix is not None
            else 1
        )
        suffix = f"-{num}"
        name_without_suffix = (
            f"{schema_name[:existing_suffix.start()]}"
            if existing_suffix is not None
            else schema_name
        )
        schema_name = f"{name_without_suffix}{suffix}"
    schema_names.append(schema_name)
    return schema_name


def generate_spec(app: Flask, version: str) -> APISpec:
    """Generate the API spec."""
    spec = APISpec(
        title="Holocron",
        version=version,
        openapi_version=app.config["SWAGGER"]["openapi"],
        plugins=[
            FlaskPlugin(),
            MarshmallowPlugin(schema_name_resolver=resolve_schema_name),
        ],
    )

    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if version not in rule.endpoint:
                continue
            spec.path(view=app.view_functions[rule.endpoint])

    spec = overwrite_spec_error(spec, version.upper())
    return spec


def serve_spec(app: Flask, spec: APISpec, version: str):
    """Serve the API spec."""
    template = spec.to_flasgger(
        app,
    )
    swagger_config = {
        "headers": [],
        "specs_route": f"/api/{version}",
        "endpoint": f"flasgger-{version}",
        "specs": [
            {
                "endpoint": f"apispec_{version}",
                "route": f"/apispec_{version}.json",
                "rule_filter": lambda rule: version in rule.endpoint,
                "model_filter": lambda tag: True,
            }
        ],
    }
    Swagger(
        app,
        template=template,
        config=swagger_config,
    )


def overwrite_spec_error(spec: APISpec, version: str) -> APISpec:
    """Overwrite the team's collector_targets field to be an array of integers.

    There is an issue to allow functionality within Marshmallow that will
    allow openapi to properly read the field type:
    https://github.com/marshmallow-code/marshmallow/issues/513
    """
    print(f"{spec.components.schemas=}")
    spec.components.schemas[f"Team{version}"]["properties"]["collectorTargets"] = {
        "readOnly": True,
        "type": "array",
        "items": {"type": "integer"},
    }
    if FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        spec.components.schemas[f"Team{version}-1"]["properties"][
            "collectorTargets"
        ] = {
            "readOnly": True,
            "type": "array",
            "items": {"type": "integer"},
        }
    return spec


# HACK - This bit of code should be replaced as soon as possible.
# This function will monkeypatch flasgger to fix an issue with serving multiple specs.
# Remove if https://github.com/flasgger/flasgger/pull/573 is merged.
# Or remove if https://github.com/flasgger/flasgger/issues/571 is resolved another way.
def patch_flasgger():
    """Monkeypatch flasgger to allow serving multiple specs."""
    # pylint: disable=import-outside-toplevel
    import json

    from flasgger import __version__
    from flasgger.base import APIDocsView
    from flask import jsonify, render_template, request, url_for

    def patched_get(self):
        """Get data under /apidocs json or Swagger UI."""
        base_endpoint = self.config.get("endpoint", "flasgger")
        specs = [
            {
                "url": url_for(".".join((base_endpoint, spec["endpoint"]))),
                "title": spec.get("title", "API Spec 1"),
                "name": spec.get("name", None),
                "version": spec.get("version", "0.0.1"),
                "endpoint": spec.get("endpoint"),
            }
            for spec in self.config.get("specs", [])
        ]
        urls = [
            {"name": spec["name"], "url": spec["url"]} for spec in specs if spec["name"]
        ]
        data = {
            "specs": specs,
            "urls": urls,
            "title": self.config.get("title", "Flasgger"),
        }
        if request.args.get("json"):
            return jsonify(data)
        data["flasgger_config"] = self.config
        data["json"] = json
        data["flasgger_version"] = __version__
        data["favicon"] = self.config.get(
            "favicon",
            url_for(f"{base_endpoint}.static", filename="favicon-32x32.png"),
        )
        data["swagger_ui_bundle_js"] = self.config.get(
            "swagger_ui_bundle_js",
            url_for(f"{base_endpoint}.static", filename="swagger-ui-bundle.js"),
        )
        data["swagger_ui_standalone_preset_js"] = self.config.get(
            "swagger_ui_standalone_preset_js",
            url_for(
                f"{base_endpoint}.static",
                filename="swagger-ui-standalone-preset.js",
            ),
        )
        data["jquery_js"] = self.config.get(
            "jquery_js",
            url_for(f"{base_endpoint}.static", filename="lib/jquery.min.js"),
        )
        data["swagger_ui_css"] = self.config.get(
            "swagger_ui_css",
            url_for(f"{base_endpoint}.static", filename="swagger-ui.css"),
        )
        return render_template("flasgger/index.html", **data)

    APIDocsView.get = patched_get
