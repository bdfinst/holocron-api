"""Metric routes."""
from flask import Blueprint, jsonify

from app.exceptions import HolocronIntegrityError
from app.middleware import SchemaCacheNotReady, organizations_cache
from app.security import get_sanitized_id

router = Blueprint("metrics", __name__, url_prefix="/metrics")


@router.route("/<org_id>", methods=["GET"])
def get_organization_metrics(org_id: str):
    """Get organization metrics by id route.

    ---
    get:
      description: Get organization metrics in format for easy chart consumption
      parameters:
        - in: path
          name: org_id
          schema:
            type: integer
          required: true
          description: ID of the organization
      responses:
        200:
          description: Get organization metrics
          content:
            application/json:
              schema: MetricsSchema
        202:
          description: Metrics are still being processed
        404:
          description: Organization not found
    """
    try:
        result = organizations_cache.get_entity(get_sanitized_id(org_id))
    except HolocronIntegrityError:
        return "Resource not found", 404
    except SchemaCacheNotReady:
        return "Processing not completed", 202
    return jsonify(result), 200
