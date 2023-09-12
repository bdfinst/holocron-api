"""Application entrypoint."""
import atexit
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from app import config
from app.database import Database
from app.middleware import (
    circuit_breaker_check,
    circuit_breaker_validation,
    limiter,
    log_request,
    organizations_cache_v2,
    return_user,
    set_csp,
    set_user,
    validate_text,
)
from app.processors.v2 import team_history
from app.routes.v2 import create_v2_router
from app.security import on_unexpected_http_methods
from app.spec import generate_spec, patch_flasgger, serve_spec


def register_background_tasks() -> None:
    """Create and start background tasks for app to run."""
    scheduler = BackgroundScheduler()
    # adding metrics calculation job for the scheduler
    scheduler.add_job(
        organizations_cache_v2.run,
        "interval",
        minutes=10,
        name="Calculate metrics for organizations. (v2)",
    )
    scheduler.add_job(
        team_history.delete_outdated_team_history,
        "interval",
        days=7,
        name="Delete outdated team history data",
    )
    scheduler.start()

    def on_scheduler_shutdown():
        logging.info("---Shutting Down Scheduler.---")
        scheduler.shutdown()

    atexit.register(on_scheduler_shutdown)

    for job in scheduler.get_jobs():
        job.modify(next_run_time=datetime.now())


def create_app() -> Flask:
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
    patch_flasgger()

    app.register_blueprint(create_v2_router())
    v2_spec = generate_spec(app, "v2")
    serve_spec(app, v2_spec, "v2")

    limiter.init_app(app)
    Database.establish_connection()
    register_background_tasks()

    return app
