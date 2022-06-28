"""Application entrypoint."""
from flask import Flask, Response

from app import config
from app.database import Database
from app.middleware import return_user, set_csp, set_user
from app.routes import router
from app.spec import generate_spec, serve_spec


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config)

    if config.SSO_ENABLED:

        @app.before_request
        def authentication_middleware():
            """Use Authentication Middleware."""
            set_user()

        @app.after_request
        def user_response_middleware(response: Response) -> Response:
            """Use User response Middleware."""
            return return_user(response)

    @app.after_request
    def csp_middleware(response: Response) -> Response:
        """Use CSP Middleware."""
        return set_csp(response)

    app.register_blueprint(router)
    spec = generate_spec(app)
    serve_spec(app, spec)
    Database.establish_connection()

    return app
