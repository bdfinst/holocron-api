"""Application Configuration."""

import logging
import os
from importlib.metadata import PackageNotFoundError, version

try:
    VERSION = version("app")
except PackageNotFoundError as err:
    logging.error(str(err))
    VERSION = "0.0.0"

DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")
DB_HOST = os.environ.get("DB_HOST", "database")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "postgres")

SSO_ENABLED = os.environ.get("SSO_ENABLED", "false").lower() != "false"
SSO_ADMIN_GROUP = os.environ.get("SSO_ADMIN_GROUP", "admin")
SSO_LEADERSHIP_GROUP = os.environ.get("SSO_LEADERSHIP_GROUP", "leadership")
SSO_GROUPS_KEY = os.environ.get("SSO_GROUPS_KEY", "groups")
SSO_USERNAME_KEY = os.environ.get("SSO_USERNAME_KEY", "username")

SWAGGER = {
    "openapi": os.environ.get("OPENAPI_VERSION", "3.0.2"),
    "static_url_path": "/api/flasgger_static",
}

MAX_CONTENT_LENGTH = 100 * 1000
MODE = os.environ.get("MODE", "production")

REQUEST_IP_HEADER = os.environ.get("REQUEST_IP_HEADER", "X-Forwarded-For")
CIRCUIT_BREAKER_ENABLED = (
    os.environ.get("CIRCUIT_BREAKER_ENABLED", "true").lower() == "true"
)
RATE_LIMITER_ENABLED = os.environ.get("RATE_LIMITER_ENABLED", "true").lower() == "true"
RATE_LIMITS = os.environ.get("RATE_LIMITS", "300/day,50/hour")
RATE_LIMITING_IP_WHITELIST = os.environ.get("RATE_LIMITING_IP_WHITELIST", "")

MIN_EXPECTED_CYCLE_TIME_HOURS = 1 / 12
PIPLINE_PASSED_STATUS = "success"


def feature_enable_check(feature_name: str) -> bool:
    """Check if feature is enabled according to environment variables."""
    return os.environ.get(feature_name, "false").lower() == "true"


FEATURE_FLAGS = {
    feature_name: feature_enable_check(feature_name)
    for feature_name in (
        "FEATURE_TEAM_VIEWS",
        "FEATURE_COST_METRICS",
        "FEATURE_DEPLOY_FREQUENCY",
        "FEATURE_EXTERNAL_CONTRIBUTORS",
        "FEATURE_COLLECTOR_CONFIGURATION",
        "FEATURE_API_V3",
    )
}

FEATURE_FLAGS["FEATURE_API_V3"] = True
FEATURE_FLAGS["FEATURE_TEAM_VIEWS"] = True
