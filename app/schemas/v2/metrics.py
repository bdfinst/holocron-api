"""Metric schema objects."""
from marshmallow import Schema
from marshmallow.fields import Boolean, Dict, Field, Int, List, Nested, Number, String

from app.config import FEATURE_FLAGS
from app.schemas.v1 import (
    BranchV1Schema,
    BuildV1Schema,
    GitRequestV1Schema,
    ProjectIssueV1Schema,
)
from app.schemas.v1._base import camelcase


class MetricsSchemaBase(Schema):
    """Base schema for metric and chart schemas."""

    def on_bind_field(self, field_name: str, field_obj: Field):
        """Convert schema fields to camelCase from snake_case."""
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class HistoricalDataV2Schema(MetricsSchemaBase):
    """Schema for historical data of team metrics."""

    week = String()
    days_spent_on_features = Number()
    days_spent_on_defects = Number()
    days_spent_on_maintenance = Number()
    days_spent_on_unplanned = Number()
    if FEATURE_FLAGS["FEATURE_COST_METRICS"]:
        amount_spent_on_features = Number()
        amount_spent_on_defects = Number()
        amount_spent_on_maintenance = Number()
        amount_spent_on_unplanned = Number()
    total_internal_integrations = Number()
    total_direct_integrations = Number()
    average_team_size = Number()
    if FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        total_external_integrations = Number()
    average_age_in_days_code_review_was_open = Number()
    total_tickets_in_backlog = Number()
    total_tickets_in_progress = Number()
    average_age_in_days_of_backlog_tickets = Number()
    total_stale_backlog_tickets = Number()
    total_throughput = Number()
    lead_times_for_week_in_days = List(Number())
    if FEATURE_FLAGS["FEATURE_DEPLOY_FREQUENCY"]:
        total_deploys = Number()
    development_cycle_times_for_week_in_days = List(Number())
    defects_created = Number()
    highest_priority_defects_created = Number()
    high_priority_defects_created = Number()
    medium_priority_defects_created = Number()
    low_priority_defects_created = Number()
    if FEATURE_FLAGS["FEATURE_PROJECT_ANALYSIS"]:
        maintainability_score = Number()


class MetricsV2Schema(MetricsSchemaBase):
    """Schema for team metrics."""

    name = String()
    id = Number()
    team_size = Number()
    wip_tickets = Number()
    is_view = Boolean()
    organization_name = String()
    organization_id = Number()
    value_stream_name = String()
    value_stream_id = Number()
    stale_merge_requests = Nested(GitRequestV1Schema, many=True)
    stale_branches = Nested(BranchV1Schema, many=True)
    latest_builds = Nested(BuildV1Schema, many=True)
    if FEATURE_FLAGS["FEATURE_PROJECT_ANALYSIS"]:
        active_issues = Nested(ProjectIssueV1Schema, many=True)
    historical_data = Nested(HistoricalDataV2Schema, many=True)
    last_updated = Dict(keys=String(), values=Int())
