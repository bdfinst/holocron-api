"""V3 routes."""

from flask import Blueprint

from app.config import FEATURE_FLAGS
from app.routes.v2.feature_flags import create_router as create_feature_flag_router
from app.routes.v2.members import create_router as create_member_router
from app.routes.v2.metrics import create_router as create_metrics_router
from app.routes.v2.organizations import create_router as create_organization_router
from app.routes.v2.pay_rates import create_router as create_pay_rate_router
from app.routes.v2.pipelines import create_router as create_pipeline_router
from app.routes.v2.project_issues import create_router as create_project_issue_router
from app.routes.v2.projects import create_router as create_project_router
from app.routes.v2.repositories import create_router as create_repository_router
from app.routes.v2.teams import create_router as create_team_router
from app.routes.v2.ticket_boards import create_router as create_ticket_board_router
from app.routes.v2.tickets import create_router as create_ticket_router
from app.routes.v2.users import create_router as create_user_router
from app.routes.v2.valuestreams import create_router as create_valuestream_router

from .branches import create_router as create_branch_router
from .builds import create_router as create_build_router
from .collectors import create_router as create_collector_router
from .commits import create_router as create_commit_router
from .git_requests import create_router as create_git_request_router


def create_v3_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("v3", "v3", url_prefix="/api/v3")
    router.register_blueprint(create_branch_router())
    router.register_blueprint(create_build_router())
    if FEATURE_FLAGS["FEATURE_COLLECTOR_CONFIGURATION"]:
        router.register_blueprint(create_collector_router())
    router.register_blueprint(create_commit_router())
    router.register_blueprint(create_feature_flag_router())
    router.register_blueprint(create_git_request_router())
    if FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        router.register_blueprint(create_member_router())
    router.register_blueprint(create_metrics_router())
    router.register_blueprint(create_organization_router())
    if FEATURE_FLAGS["FEATURE_COST_METRICS"]:
        router.register_blueprint(create_pay_rate_router())
    router.register_blueprint(create_pipeline_router())
    router.register_blueprint(create_project_issue_router())
    router.register_blueprint(create_project_router())
    router.register_blueprint(create_repository_router())
    router.register_blueprint(create_team_router())
    router.register_blueprint(create_ticket_board_router())
    router.register_blueprint(create_ticket_router())
    router.register_blueprint(create_user_router())
    router.register_blueprint(create_valuestream_router())
    return router
