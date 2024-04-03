"""Schema for Team model."""

from marshmallow import fields, validate

from app import config
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .collector_target import CollectorTargetV2Schema
from .member import TeamMemberV2Schema
from .user import UserV2Schema


class TeamHistoryV2Schema(SchemaBase):
    """Team history schema."""

    team_size = fields.Integer()
    team_id = fields.Integer()


class TeamV2Schema(SchemaBase):
    """Team schema."""

    if config.FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        members = fields.Nested(
            TeamMemberV2Schema, many=True, exclude=("team",), dump_only=True
        )
    users = fields.Nested(UserV2Schema, many=True, dump_only=True)
    collector_targets = fields.List(
        fields.Pluck(CollectorTargetV2Schema, "id"), dump_only=True
    )
    value_stream_id = fields.Integer(required=True, data_key="valuestreamId")
    name = fields.String(required=True, validate=input_name_validator)
    user_ids = fields.List(
        fields.Integer(), required=True, validate=validate.Length(min=1), load_only=True
    )
    team_size = fields.Integer(required=True, validate=validate.Range(min=1))
    collector_target_ids = fields.List(fields.Integer(), required=True, load_only=True)
    is_workflow_only = fields.Boolean(dump_only=True)
    team_history = fields.Nested(TeamHistoryV2Schema, many=True, dump_only=True)
