"""Application Configuration."""
import os

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
