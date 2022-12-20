"""Metric schema objects."""
from marshmallow import Schema
from marshmallow.fields import Dict, Field, Int, List, Nested, Number, String

from ._base import camelcase
from .branch import BranchSchema
from .build import BuildSchema
from .git_request import GitRequestSchema


class MetricsSchemaBase(Schema):
    """Base schema for metric and chart schemas."""

    def on_bind_field(self, field_name: str, field_obj: Field):
        """Convert schema fields to camelCase from snake_case."""
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class DeployFrequencySchema(MetricsSchemaBase):
    """Schema for deploy frequency chart data."""

    deploys = List(Number())


class CumulativeFlowSchema(MetricsSchemaBase):
    """Schema for cumulative flow chart data."""

    backlog = List(Number())
    wip = List(Number())


class IntegrationFrequencySchema(MetricsSchemaBase):
    """Schema for integration frequency chart data."""

    integrations = List(Number())
    direct_integrations = List(Number())


class CycleTimeDefectSchema(MetricsSchemaBase):
    """Schema for cycle time and defect chart data."""

    dev_cycle_time = List(Number())
    defect_rate = List(Number())
    highest_defects = List(Number())
    high_defects = List(Number())
    medium_defects = List(Number())
    low_defects = List(Number())
    lowest_defects = List(Number())


class LeadTimeThroughPutSchema(MetricsSchemaBase):
    """Schema for lead time and throughput chart data."""

    story_lead_time = List(Number())
    throughput = List(Number())


class EffortSchema(MetricsSchemaBase):
    """Schema for effort chart data."""

    feature = List(Number())
    defect_effort = List(Number())
    unplanned = List(Number())
    maintenance = List(Number())


class CodeReviewTrendSchema(MetricsSchemaBase):
    """Schema for code review trend data."""

    age_in_days_review_was_open = List(Number())


class TeamSizeHistoriesSchema(MetricsSchemaBase):
    """Schema for team size histories data."""

    team_size = List(Number())


class WeeklyDataSchema(MetricsSchemaBase):
    """Schema for weekly data of team metrics."""

    effort_hours = Nested(EffortSchema)
    effort_costs = Nested(EffortSchema)
    lead_time_throughput = Nested(LeadTimeThroughPutSchema)
    cycle_time_defect = Nested(CycleTimeDefectSchema)
    integration_frequency = Nested(IntegrationFrequencySchema)
    cumulative_flow = Nested(CumulativeFlowSchema)
    deploy_frequency = Nested(DeployFrequencySchema)
    code_review_trend = Nested(CodeReviewTrendSchema)
    team_size_histories = Nested(TeamSizeHistoriesSchema)


class TeamMetricsSchema(MetricsSchemaBase):
    """Schema for team metrics."""

    name = String()
    team_size = Number()
    branches = Nested(BranchSchema, many=True)
    merge_requests = Nested(GitRequestSchema, many=True)
    wip_load_data = Number()
    repos_build_data = Nested(BuildSchema, many=True)
    data_quality_issues = Dict(keys=String(), values=String())
    last_updated = Dict(keys=String(), values=Int())
    weekly_data = Dict(keys=String(), values=Nested(WeeklyDataSchema))


class ValuestreamMetricsSchema(MetricsSchemaBase):
    """Schema for valuestream metrics."""

    name = String()
    last_updated = Dict(keys=String(), values=Int())
    teams = Nested(TeamMetricsSchema, many=True)


class MetricsSchema(MetricsSchemaBase):
    """Schema for organization metrics."""

    name = String()
    last_updated = Dict(keys=String(), values=Int())
    valuestreams = Nested(ValuestreamMetricsSchema, many=True)
