"""Schema for Repository model."""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Repository

from ._base import SchemaBase
from .branch import BranchSchema
from .commit import CommitSchema
from .git_request import GitRequestSchema


class RepositorySchema(SQLAlchemyAutoSchema, SchemaBase):
    """Schema for Repository model."""

    class Meta:
        """Configuration."""

        model = Repository
        include_relationships = True

    branches = fields.Nested(BranchSchema, many=True)
    commits = fields.Nested(CommitSchema, many=True)
    git_requests = fields.Nested(GitRequestSchema, many=True)
    team_id = auto_field()
