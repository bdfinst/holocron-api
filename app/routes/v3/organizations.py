"""Organization routes."""

from typing import Any, Mapping, Tuple, cast

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud import organizations_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin, requires_org_access, requires_security
from app.schemas.v3 import OrganizationV3Schema
from app.security import MALFORMED_REQ_PARAMS_MSG, get_sanitized_id, log_security_event
from app.utils.pagination import get_pagination_info, set_pagination_header

schema = OrganizationV3Schema()


def list_organizations() -> Tuple[Any, int]:
    """List organizations route.

    ---
    get:
      description: List organizations
      parameters:
        - in: query
          name: per_page
          schema:
            type: integer
          required: false
          description: The maximum number of items to return
        - in: query
          name: page
          schema:
            type: integer
          required: false
          description: The page of the data set to retrieve
      responses:
        200:
          description: List organizations
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/OrganizationV3'
    """
    with generate_session() as session:
        page_info = get_pagination_info(
            request.args, organizations_crud.get_count(session)
        )
        raw_organizations = organizations_crud.get_entities_paginated(
            session, offset=page_info.offset, limit=page_info.limit
        )
        organizations = schema.dump(raw_organizations, many=True)
    result = {"result": organizations}
    response = jsonify(result)
    response = set_pagination_header(response, request.url, page_info)
    return response, 200


@requires_security([requires_admin])
def create_organization() -> Tuple[Any, int]:
    """Create organization route.

    ---
    post:
      description: Create organization
      requestBody:
        content:
          application/json:
            schema: OrganizationV3Schema
      responses:
        201:
          description: The organization was successfully created
          content:
            application/json:
              schema: OrganizationV3Schema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorV2Schema
    """
    try:
        data = schema.load(cast(Mapping[str, Any], request.json))
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_organization = organizations_crud.create_entity(session, data)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_organization)
    response = jsonify(result)
    return response, 201


def get_organization(org_id: str) -> Tuple[Any, int]:
    """Get organization by id route.

    ---
    get:
      description: Get organization
      parameters:
        - in: path
          name: org_id
          schema:
            type: integer
          required: true
          description: ID of the organization
      responses:
        200:
          description: Get organization
          content:
            application/json:
              schema: OrganizationV3Schema
        404:
          description: Organization not found
    """
    with generate_session() as session:
        try:
            raw_org = organizations_crud.get_entity(session, get_sanitized_id(org_id))
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_org)
    response = jsonify(result)
    return response, 200


@requires_security([requires_admin, requires_org_access])
def update_organization(org_id: str) -> Tuple[Any, int]:
    """Update organization route.

    ---
    put:
      description: Update organization
      parameters:
        - in: path
          name: org_id
          schema:
            type: integer
          required: true
          description: ID of the organization
      requestBody:
        content:
          application/json:
            schema: OrganizationV3Schema
      responses:
        200:
          description: The organization was successfully updated
          content:
            application/json:
              schema: OrganizationV3Schema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorV2Schema
    """
    try:
        data = schema.load(cast(Mapping[str, Any], request.json))
    except ValidationError as err:
        log_security_event(MALFORMED_REQ_PARAMS_MSG)
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_organization = organizations_crud.update_entity(
                session, data, get_sanitized_id(org_id)
            )
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_organization)
    response = jsonify(result)
    return response, 200


@requires_security([requires_admin, requires_org_access])
def delete_organization(org_id: str) -> Tuple[Any, int]:
    """Delete organization route.

    ---
    delete:
      description: Delete organization
      parameters:
        - in: path
          name: org_id
          schema:
            type: integer
          required: true
          description: ID of the organization
      responses:
        204:
          description: The organization was successfully deleted
    """
    with generate_session() as session:
        organizations_crud.delete_entity(session, get_sanitized_id(org_id))
    return "", 204


def create_router() -> Blueprint:
    """Router factory."""
    organization_id_route = "/<org_id>"
    router = Blueprint("organizations", __name__, url_prefix="/organizations")
    router.route("", methods=["GET"])(list_organizations)
    router.route("", methods=["POST"])(create_organization)
    router.route(organization_id_route, methods=["GET"])(get_organization)
    router.route(organization_id_route, methods=["PUT"])(update_organization)
    router.route(organization_id_route, methods=["DELETE"])(delete_organization)
    return router
