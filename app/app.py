"""Application entrypoint."""
from flask import Flask

from app import config
from app.database import Database
from app.middleware import (
    circuit_breaker_check,
    circuit_breaker_validation,
    limiter,
    log_request,
    organizations_cache,
    return_user,
    set_csp,
    set_user,
)
from app.routes import router
from app.spec import generate_spec, serve_spec


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config)

    app.before_request(log_request)
    app.before_request(circuit_breaker_check)
    app.after_request(set_csp)
    app.after_request(circuit_breaker_validation)

    if config.SSO_ENABLED:
        app.before_request(set_user)
        app.after_request(return_user)

    app.register_blueprint(router)
    spec = generate_spec(app)
    serve_spec(app, spec)
    limiter.init_app(app)
    Database.establish_connection()
    organizations_cache.start()

    return app
