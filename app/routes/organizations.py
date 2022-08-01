"""Organization routes."""
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.crud import organizations_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.middleware import requires_admin
from app.schemas import OrganizationMetricsSchema, OrganizationSchema

router = Blueprint("organizations", __name__, url_prefix="/organizations")

schema = OrganizationSchema()
metric_schema = OrganizationMetricsSchema()


@router.route("", methods=["GET"])
def list_organizations():
    """List organizations route.

    ---
    get:
      description: List organizations
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
                      $ref: '#/components/schemas/Organization'
    """
    with generate_session() as session:
        raw_organizations = organizations_crud.get_entities(session)
        organizations = [
            schema.dump(organization) for organization in raw_organizations
        ]
    result = {"result": organizations}
    return jsonify(result), 200


@router.route("", methods=["POST"])
def create_organization():
    """Create organization route.

    ---
    post:
      description: Create organization
      requestBody:
        content:
          application/json:
            schema: OrganizationSchema
      responses:
        201:
          description: The organization was successfully created
          content:
            application/json:
              schema: OrganizationSchema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorSchema
    """
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_organization = organizations_crud.create_entity(session, data)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_organization)
    return jsonify(result), 201


@router.route("/<org_id>", methods=["GET"])
def get_organization(org_id: int):
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
              schema: OrganizationMetricsSchema
        404:
          description: Organization not found
    """
    with generate_session() as session:
        try:
            raw_organization = organizations_crud.get_entity(session, org_id)
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = metric_schema.dump(raw_organization)
    return jsonify(result), 200


@router.route("/<org_id>", methods=["PUT"])
@requires_admin
def update_organization(org_id: int):
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
            schema: OrganizationSchema
      responses:
        200:
          description: The organization was successfully updated
          content:
            application/json:
              schema: OrganizationSchema
        400:
          description: Failure due to an invalid request
          content:
            application/json:
              schema: ValidationErrorSchema
    """
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return err.messages, 400
    with generate_session() as session:
        try:
            raw_organization = organizations_crud.update_entity(session, data, org_id)
        except HolocronIntegrityError as err:
            return err.messages, 400
        result = schema.dump(raw_organization)
    return jsonify(result), 200


@router.route("/<org_id>", methods=["DELETE"])
@requires_admin
def delete_organization(org_id: int):
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
        organizations_crud.delete_entity(session, org_id)
    return "", 204
