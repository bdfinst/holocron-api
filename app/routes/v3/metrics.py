"""Metric routes."""

from typing import Any, Tuple

from flask import Blueprint, jsonify

from app.crud import teams_crud, value_streams_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import (
    SchemaCacheNotReady,
    organizations_cache_v2,
    requires_admin,
    requires_org_access,
    requires_security,
    requires_team_access,
    requires_vs_access,
)
from app.security import get_sanitized_id

RESOURCE_NOT_FOUND = "Resource not found"
PROCCESSING_NOT_COMPLETED = "Processing not completed"


@requires_security([requires_admin, requires_org_access])
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
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/MetricsV3'
        202:
          description: Metrics are still being processed
        404:
          description: Organization not found
    """
    try:
        metrics = organizations_cache_v2.get_entity(get_sanitized_id(org_id))
    except HolocronIntegrityError:
        return RESOURCE_NOT_FOUND, 404
    except SchemaCacheNotReady:
        return PROCCESSING_NOT_COMPLETED, 202
    result = {"result": metrics}
    response = jsonify(result)
    return response, 200


@requires_security([requires_admin, requires_vs_access])
def get_value_stream_metrics(value_stream_id: str) -> Tuple[Any, int]:
    """Get organization metrics by id route.

    ---
    get:
      description: Get value stream metrics in format for easy chart consumption
      parameters:
        - in: path
          name: value_stream_id
          schema:
            type: integer
          required: true
          description: ID of the value stream
      responses:
        200:
          description: Get value stream metrics
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/MetricsV3'
        202:
          description: Value streams are still being processed
        404:
          description: Resource not found
    """
    database_id = get_sanitized_id(value_stream_id)
    with generate_session() as session:
        try:
            raw_value_stream = value_streams_crud.get_entity(session, database_id)
            organization_data = organizations_cache_v2.get_entity(
                raw_value_stream.organization_id
            )
        except HolocronIntegrityError:
            return RESOURCE_NOT_FOUND, 404
        except SchemaCacheNotReady:
            return PROCCESSING_NOT_COMPLETED, 202
    if organization_data is not None:
        metrics = [
            team_metrics
            for team_metrics in organization_data
            if team_metrics["valueStreamId"] == database_id
        ]
        result = {"result": metrics}
        response = jsonify(result)
        return response, 200
    return RESOURCE_NOT_FOUND, 404


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
          description: ID of the team or team view to get metrics for
      responses:
        200:
          description: Get team metrics
          content:
            application/json:
              schema: MetricsV3Schema
        202:
          description: Metrics are still being processed
        404:
          description: Resource not found
    """
    database_id = get_sanitized_id(team_id)
    with generate_session() as session:
        try:
            raw_team = teams_crud.get_entity(session, database_id)
            raw_value_stream = value_streams_crud.get_entity(
                session, raw_team.value_stream_id
            )
            organization_data = organizations_cache_v2.get_entity(
                raw_value_stream.organization_id
            )
        except HolocronIntegrityError:
            return RESOURCE_NOT_FOUND, 404
        except SchemaCacheNotReady:
            return PROCCESSING_NOT_COMPLETED, 202
    if organization_data is not None:
        for team_metrics in organization_data:
            if team_metrics["id"] == database_id:
                response = jsonify(team_metrics)
                return response, 200
    return RESOURCE_NOT_FOUND, 404


def create_router() -> Blueprint:
    """Router factory."""
    router = Blueprint("metrics", __name__, url_prefix="/metrics")
    router.route("/organization/<org_id>", methods=["GET"])(get_organization_metrics)
    router.route("/value-stream/<value_stream_id>", methods=["GET"])(
        get_value_stream_metrics
    )
    router.route("/team/<team_id>", methods=["GET"])(get_team_metrics)
    return router
