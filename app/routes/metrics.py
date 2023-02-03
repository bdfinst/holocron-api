"""Metric routes."""
from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import teams_crud, valuestreams_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import (
    SchemaCacheNotReady,
    organizations_cache,
    requires_admin,
    requires_org_access,
    requires_org_leadership,
    requires_security,
    requires_team_access,
    requires_vs_access,
)
from app.security import get_sanitized_id

router = Blueprint("metrics", __name__, url_prefix="/metrics")


@router.route("/<org_id>", methods=["GET"])
def get_organization_metrics(org_id: str) -> Tuple[Any, int]:
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


@router.route("/organization/<org_id>", methods=["GET"])
@requires_security([requires_admin, requires_org_access, requires_org_leadership])
def get_organization_metrics_temp(org_id: str) -> Tuple[Any, int]:
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


@router.route("/valuestream/<valuestream_id>", methods=["GET"])
@requires_security([requires_admin, requires_vs_access])
def get_valuestream_metrics(valuestream_id: str) -> Tuple[Any, int]:
    """Get organization metrics by id route.

    ---
    get:
      description: Get valuestream metrics in format for easy chart consumption
      parameters:
        - in: path
          name: valuestream_id
          schema:
            type: integer
          required: true
          description: ID of the valuestream
      responses:
        200:
          description: Get valuestream metrics
          content:
            application/json:
              schema: ValuestreamMetricsSchema
        202:
          description: Valuestreams are still being processed
        404:
          description: Resource not found
    """
    with generate_session() as session:
        try:
            raw_valuestream = valuestreams_crud.get_entity(
                session, get_sanitized_id(valuestream_id)
            )
            organization_data = organizations_cache.get_entity(
                raw_valuestream.organization_id
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        except SchemaCacheNotReady:
            return "Processing not completed", 202
    if organization_data is not None:
        for valuestream in organization_data["valuestreams"]:
            if valuestream["name"] == raw_valuestream.name:
                return jsonify(valuestream), 200
    return "Resource not found", 404


@router.route("/team/<team_id>", methods=["GET"])
@requires_security([requires_admin, requires_team_access])
def get_team_metrics(team_id: str) -> Tuple[Any, int]:
    """Get team metrics by id route.

    ---
    get:
      description: Get team metrics in format for easy chart consumption
      parameters:
        - in: path
          name: team_id
          schema:
            type: integer
          required: true
          description: ID of the team
      responses:
        200:
          description: Get team metrics
          content:
            application/json:
              schema: TeamMetricsSchema
        202:
          description: Metrics are still being processed
        404:
          description: Resource not found
    """
    with generate_session() as session:
        try:
            raw_team = teams_crud.get_entity(session, get_sanitized_id(team_id))
            raw_valuestream = valuestreams_crud.get_entity(
                session, raw_team.valuestream_id
            )
            organization_data = organizations_cache.get_entity(
                raw_valuestream.organization_id
            )
        except HolocronIntegrityError:
            return "Resource not found", 404
        except SchemaCacheNotReady:
            return "Processing not completed", 202
    if organization_data:
        for valuestream in organization_data["valuestreams"]:
            for team in valuestream["teams"]:
                if team["name"] == raw_team.name:
                    return jsonify(team), 200
    return "Resource not found", 404
