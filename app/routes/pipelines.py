"""Pipeline routes."""
from flask import Blueprint, jsonify

from app.crud import pipelines_crud
from app.database import generate_session
from app.exceptions import HolocronIntegrityError
from app.schemas import PipelineSchema

router = Blueprint("pipelines", __name__, url_prefix="/pipelines")

schema = PipelineSchema()


@router.route("", methods=["GET"])
def list_pipelines():
    """Get pipelines.

    ---
    get:
      description: Get pipelines
      responses:
        200:
          description: Get pipelines
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Pipeline'
    """
    with generate_session() as session:
        raw_pipelines = pipelines_crud.get_entities(session)
        pipelines = [schema.dump(pipeline) for pipeline in raw_pipelines]
    result = {"result": pipelines}
    return jsonify(result), 200


@router.route("/team/<id_>", methods=["GET"])
def list_pipelines_for_team(id_: int):
    """Get pipelines for a given team id.

    ---
    get:
      description: Get pipelines belonging to a team
      parameters:
        - in: path
          name: id_
          schema:
            type: integer
          required: true
          description: ID of the team to get pipelines for
      responses:
        200:
          description: Get pipelines belonging to a team
          content:
            application/json:
              schema:
                properties:
                  result:
                    type: array
                    items:
                      $ref: '#/components/schemas/Pipeline'
        404:
          description: Team not found
    """
    with generate_session() as session:
        try:
            raw_pipelines = pipelines_crud.get_entities_for_team(session, id_)
        except HolocronIntegrityError:
            return "Resource not found", 404
        pipelines = [schema.dump(pipeline) for pipeline in raw_pipelines]
    result = {"result": pipelines}
    return jsonify(result), 200


@router.route("/<id_>", methods=["GET"])
def get_pipeline(id_: int):
    """Get pipeline by id.

    ---
    get:
      description: Get single pipeline by id
      parameters:
        - in: path
          name: id_
          schema:
            type: integer
          required: true
          description: ID of the pipeline
      responses:
        200:
          description: Get single pipeline by id
          content:
            application/json:
              schema: PipelineSchema
        404:
          description: Pipeline not found
    """
    with generate_session() as session:
        try:
            raw_pipeline = pipelines_crud.get_entity(session, id_)
        except HolocronIntegrityError:
            return "Resource not found", 404
        result = schema.dump(raw_pipeline)
    return jsonify(result), 200
