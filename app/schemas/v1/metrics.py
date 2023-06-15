"""Metric schema objects."""
from marshmallow import Schema
from marshmallow.fields import Boolean, Dict, Field, Int, List, Nested, Number, String

from app import config

from ._base import camelcase
from .branch import BranchV1Schema
from .build import BuildV1Schema
from .git_request import GitRequestV1Schema


class MetricsSchemaBase(Schema):
    """Base schema for metric and chart schemas."""

    def on_bind_field(self, field_name: str, field_obj: Field):
        """Convert schema fields to camelCase from snake_case."""
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class DeployFrequencyV1Schema(MetricsSchemaBase):
    """Schema for deploy frequency chart data."""

    deploys = List(Number())


class CumulativeFlowV1Schema(MetricsSchemaBase):
    """Schema for cumulative flow chart data."""

    backlog = List(Number())
    wip = List(Number())


class IntegrationFrequencyV1Schema(MetricsSchemaBase):
    """Schema for integration frequency chart data."""

    integrations = List(Number())
    direct_integrations = List(Number())
    if config.FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        external_integrations = List(Number())


class CycleTimeDefectV1Schema(MetricsSchemaBase):
    """Schema for cycle time and defect chart data."""

    dev_cycle_time = List(Number())
    defect_rate = List(Number())
    highest_defects = List(Number())
    high_defects = List(Number())
    medium_defects = List(Number())
    low_defects = List(Number())
    lowest_defects = List(Number())


class LeadTimeThroughPutV1Schema(MetricsSchemaBase):
    """Schema for lead time and throughput chart data."""

    story_lead_time = List(Number())
    throughput = List(Number())


class EffortV1Schema(MetricsSchemaBase):
    """Schema for effort chart data."""

    feature = List(Number())
    defect_effort = List(Number())
    unplanned = List(Number())
    maintenance = List(Number())


class CodeReviewTrendV1Schema(MetricsSchemaBase):
    """Schema for code review trend data."""

    age_in_days_review_was_open = List(Number())


class TeamHistoryV1Schema(MetricsSchemaBase):
    """Schema for team size histories data."""

    team_size = List(Number())


class WeeklyDataV1Schema(MetricsSchemaBase):
    """Schema for weekly data of team metrics."""

    effort_hours = Nested(EffortV1Schema)
    if config.FEATURE_FLAGS["FEATURE_COST_METRICS"]:
        effort_costs = Nested(EffortV1Schema)
    lead_time_throughput = Nested(LeadTimeThroughPutV1Schema)
    cycle_time_defect = Nested(CycleTimeDefectV1Schema)
    integration_frequency = Nested(IntegrationFrequencyV1Schema)
    cumulative_flow = Nested(CumulativeFlowV1Schema)
    if config.FEATURE_FLAGS["FEATURE_DEPLOY_FREQUENCY"]:
        deploy_frequency = Nested(DeployFrequencyV1Schema)
    code_review_trend = Nested(CodeReviewTrendV1Schema)
    team_history = Nested(TeamHistoryV1Schema)


class TeamMetricsV1Schema(MetricsSchemaBase):
    """Schema for team metrics."""

    name = String()
    team_size = Number()
    branches = Nested(BranchV1Schema, many=True)
    merge_requests = Nested(GitRequestV1Schema, many=True)
    wip_load_data = Number()
    repos_build_data = Nested(BuildV1Schema, many=True)
    data_quality_issues = Dict(keys=String(), values=String())
    last_updated = Dict(keys=String(), values=Int())
    weekly_data = Dict(keys=String(), values=Nested(WeeklyDataV1Schema))
    is_view = Boolean()


class ValuestreamMetricsV1Schema(MetricsSchemaBase):
    """Schema for valuestream metrics."""

    name = String()
    last_updated = Dict(keys=String(), values=Int())
    teams = Nested(TeamMetricsV1Schema, many=True)


class MetricsV1Schema(MetricsSchemaBase):
    """Schema for organization metrics."""

    name = String()
    last_updated = Dict(keys=String(), values=Int())
    valuestreams = Nested(ValuestreamMetricsV1Schema, many=True)
