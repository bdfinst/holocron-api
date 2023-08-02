"""Feature Flags routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.config import FEATURE_FLAGS


def list_feature_flags() -> Tuple[Any, int]:
    """Get all feature flags.

    ---
    get:
      description: Get all feature flags
      responses:
        200:
          description: Get all feature flags
          content:
            application/json:
              schema:
                properties:
                  feature_flag:
                    type: boolean
    """
    return jsonify(FEATURE_FLAGS), 200


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("featureflags", __name__, url_prefix="/featureflags")
    router.route("", methods=["GET"])(list_feature_flags)
    return router
