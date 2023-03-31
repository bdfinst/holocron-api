"""Routes."""
from flask import Blueprint

from .branches import router as branch_router
from .builds import router as build_router
from .commits import router as commit_router
from .feature_flags import router as feature_flags_router
from .git_requests import router as git_request_router
from .metrics import router as metrics_router
from .organizations import router as organization_router
from .pay_rates import router as pay_rate_router
from .pipelines import router as pipeline_router
from .repositories import router as repository_router
from .teams import router_factory as team_router_factory
from .ticket_boards import router as ticket_board_router
from .tickets import router as ticket_router
from .users import router as user_router
from .valuestreams import router as valuestream_router


def router_factory():
    """Return router."""
    router = Blueprint("v1", __name__, url_prefix="/api/v1")
    router.register_blueprint(branch_router)
    router.register_blueprint(build_router)
    router.register_blueprint(commit_router)
    router.register_blueprint(git_request_router)
    router.register_blueprint(metrics_router)
    router.register_blueprint(organization_router)
    router.register_blueprint(pay_rate_router)
    router.register_blueprint(pipeline_router)
    router.register_blueprint(repository_router)
    router.register_blueprint(team_router_factory())
    router.register_blueprint(ticket_board_router)
    router.register_blueprint(ticket_router)
    router.register_blueprint(user_router)
    router.register_blueprint(valuestream_router)
    router.register_blueprint(feature_flags_router)
    return router
