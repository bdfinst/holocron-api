"""Application entrypoint."""
import atexit
import logging

from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
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
    validate_text,
)
from app.routes import router
from app.security import on_unexpected_http_methods
from app.spec import generate_spec, serve_spec


def register_background_tasks():
    """Create and start background tasks for app to run."""
    scheduler = BackgroundScheduler()
    # adding metrics calculation job for the scheduler
    scheduler.add_job(
        organizations_cache.run,
        "interval",
        minutes=1,
        name="Calculate metrics for organizations.",
    )
    scheduler.start()

    def on_scheduler_shutdown():
        logging.info("---Shutting Down Scheduler.---")
        scheduler.shutdown()

    atexit.register(on_scheduler_shutdown)


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_error_handler(405, on_unexpected_http_methods)
    app.before_request(log_request)
    app.before_request(circuit_breaker_check)
    app.before_request(validate_text)
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
    register_background_tasks()

    return app
