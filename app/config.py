"""Application Configuration."""
import os
from typing import Dict, List

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

JIRA_TICKET_TYPE_BUCKETS: Dict[str, List[str]] = {
    "defect_effort": ["Bug", "Anomaly"],
    "unplanned": ["Unplanned"],
    "maintenance": ["Maintenance"],
    "feature": [],
}
TICKET_PRIORITIES = {
    "HIGHEST": "Highest",
    "HIGH": "High",
    "MEDIUM": "Medium",
    "LOW": "Low",
    "LOWEST": "Lowest",
}
JIRA_PRIORITY_MAPPINGS = {
    TICKET_PRIORITIES["HIGHEST"]: TICKET_PRIORITIES["HIGHEST"],
    TICKET_PRIORITIES["HIGH"]: TICKET_PRIORITIES["HIGH"],
    TICKET_PRIORITIES["MEDIUM"]: TICKET_PRIORITIES["MEDIUM"],
    TICKET_PRIORITIES["LOW"]: TICKET_PRIORITIES["LOW"],
    TICKET_PRIORITIES["LOWEST"]: TICKET_PRIORITIES["LOWEST"],
    1: TICKET_PRIORITIES["HIGHEST"],
    2: TICKET_PRIORITIES["HIGH"],
    3: TICKET_PRIORITIES["MEDIUM"],
    4: TICKET_PRIORITIES["LOW"],
    5: TICKET_PRIORITIES["LOWEST"],
    "Critical": TICKET_PRIORITIES["HIGHEST"],
}
DEFAULT_TICKET_PRIORITY = TICKET_PRIORITIES["LOWEST"]
MIN_EXPECTED_CYCLE_TIME_HOURS = 1 / 12
PIPLINE_PASSED_STATUS = "success"

FEATURE_FLAGS = {
    "FEATURE_TEAM_VIEWS": os.environ.get("FEATURE_TEAM_VIEWS", "false").lower()
    == "true",
    "FEATURE_COST_METRICS": os.environ.get("FEATURE_COST_METRICS", "false").lower()
    == "true",
    "FEATURE_DEPLOY_FREQUENCY": os.environ.get(
        "FEATURE_DEPLOY_FREQUENCY", "false"
    ).lower()
    == "true",
}
