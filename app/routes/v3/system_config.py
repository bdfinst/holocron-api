"""Feature Flags routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.config import FEATURE_FLAGS, SSO_ENABLED, VERSION


def get_system_config() -> Tuple[Any, int]:
    """Get the system configuration.

    ---
    get:
      description: Get system configuration
      responses:
        200:
          description: Get system configuration
          content:
            application/json:
              schema:
                properties:
                  version:
                    type: string
                  ssoEnabled:
                    type: boolean
                  featureFlags:
                    type: object
                    additionalProperties:
                      type: boolean
    """
    return (
        jsonify(
            {
                "version": VERSION,
                "ssoEnabled": SSO_ENABLED,
                "featureFlags": FEATURE_FLAGS,
            }
        ),
        200,
    )


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("system-config", __name__, url_prefix="/system-config")
    router.route("", methods=["GET"])(get_system_config)
    return router
