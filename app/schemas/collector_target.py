"""Schema for CollectorTarget models."""
from marshmallow import Schema

from .pipelines import PipelineMetricsSchema
from .repository import RepositoryMetricsSchema
from .ticket_board import TicketBoardMetricsSchema


class CollectorTargetSchema(Schema):
    """Schema which dynamically chooses appropriate collector target schema."""

    type_schemas = {
        "Pipeline": (PipelineMetricsSchema, "pipeline_id"),
        "Repository": (RepositoryMetricsSchema, "repository_id"),
        "TicketBoard": (TicketBoardMetricsSchema, "board_id"),
    }

    # pylint: disable=arguments-renamed,unused-argument
    def dump(self, data, **kwargs):
        """Dump override which assumes many=True."""
        result = []
        for obj in data:
            json = self._dump(obj)
            if json is not None:
                result.append(json)

        return result

    def _dump(self, obj):
        """Private method to grab correct schema and validate it."""
        schema_info = self.type_schemas.get(obj.__class__.__name__)
        if getattr(obj, schema_info[1]) is None:
            return None
        return schema_info[0]().dump(obj, many=False)
