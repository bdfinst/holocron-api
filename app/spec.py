"""API Spec."""

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flask import Flask


def generate_spec(app: Flask, version: str) -> APISpec:
    """Generate the API spec."""
    spec = APISpec(
        title="Holocron",
        version=version,
        openapi_version=app.config["SWAGGER"]["openapi"],
        plugins=[
            FlaskPlugin(),
            MarshmallowPlugin(),
        ],
    )

    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if version not in rule.endpoint:
                continue
            spec.path(view=app.view_functions[rule.endpoint])

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
