"""Schema for Team model."""

from marshmallow import fields, validate

from app import config
from app.utils.input_validation import input_name_validator

from ._base import SchemaBase
from .collector_target import CollectorTargetV3Schema
from .member import TeamMemberV3Schema
from .user import UserV3Schema


class TeamHistoryV3Schema(SchemaBase):
    """Team history schema."""

    team_size = fields.Integer()
    team_id = fields.Integer()


class TeamV3Schema(SchemaBase):
    """Team schema."""

    if config.FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        members = fields.Nested(
            TeamMemberV3Schema, many=True, exclude=("team",), dump_only=True
        )
    users = fields.Nested(UserV3Schema, many=True, dump_only=True)
    collector_targets = fields.List(
        fields.Pluck(CollectorTargetV3Schema, "id"), dump_only=True
    )
    value_stream_id = fields.Integer(required=True)
    name = fields.String(required=True, validate=input_name_validator)
    user_ids = fields.List(
        fields.Integer(), required=True, validate=validate.Length(min=1), load_only=True
    )
    team_size = fields.Integer(required=True, validate=validate.Range(min=1))
    collector_target_ids = fields.List(fields.Integer(), required=True, load_only=True)
    is_workflow_only = fields.Boolean(dump_only=True)
    team_history = fields.Nested(TeamHistoryV3Schema, many=True, dump_only=True)
