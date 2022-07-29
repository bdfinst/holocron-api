"""Schema for Valuestream model."""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Valuestream

from ._base import SchemaBase
from .team import ExistingTeamSchema, TeamMetricsSchema


class ValuestreamSchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Valuestream model."""

    class Meta:
        """Configuration."""

        model = Valuestream
        include_relationships = True

    organization_id = auto_field()
    teams = fields.Nested(ExistingTeamSchema, many=True)


class ValuestreamMetricsSchema(ValuestreamSchema):
    """Schema for Valuestream model with metric objects."""

    teams = fields.Nested(TeamMetricsSchema, many=True)
