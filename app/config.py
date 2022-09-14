"""Application Configuration."""
import os
from typing import Any, Dict, List

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
RELEASE_STAGE_NAME = "Deploy"
STAGE_PASSED_STATUS = "success"
SECURITY_SETTINGS: Dict[str, Any] = {
    "MAX_INPUT_CHAR_LEN": 50,
    "VALID_NAME_CHARS": "^[a-zA-Z0-9][ a-zA-Z0-9_-]*[a-zA-Z0-9]$",
}
