"""Metric schema objects."""
from marshmallow import Schema
from marshmallow.fields import Boolean, Dict, Field, Int, Nested, Number, String

from app.config import FEATURE_FLAGS

from ._base import camelcase
from .branch import BranchV2Schema
from .build import BuildV2Schema
from .git_request import GitRequestV2Schema
from .project_issue import ProjectIssueV2Schema


class MetricsSchemaBase(Schema):
    """Base schema for metric and chart schemas."""

    def on_bind_field(self, field_name: str, field_obj: Field):
        """Convert schema fields to camelCase from snake_case."""
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class AgeV2Schema(MetricsSchemaBase):
    """Schema for item age in days."""

    days = Number()


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
    if FEATURE_FLAGS["FEATURE_EXTERNAL_CONTRIBUTORS"]:
        total_external_integrations = Number()
    average_team_size = Number()
    average_age_in_days_code_review_was_open = Number()
    total_tickets_in_backlog = Number()
    total_tickets_in_progress = Number()
    total_throughput = Number()
    ticket_lead_times = Nested(AgeV2Schema, many=True)
    if FEATURE_FLAGS["FEATURE_DEPLOY_FREQUENCY"]:
        total_deploys = Number()
    ticket_development_cycle_times = Nested(AgeV2Schema, many=True)
    defects_created = Number()
    highest_priority_defects_created = Number()
    high_priority_defects_created = Number()
    medium_priority_defects_created = Number()
    low_priority_defects_created = Number()
    lowest_priority_defects_created = Number()
    maintainability_issues = Number()
    maintainability_low_severity_issues = Number()
    maintainability_medium_severity_issues = Number()
    maintainability_high_severity_issues = Number()
    vulnerabilities = Number()
    high_severity_vulnerabilities = Number()
    medium_severity_vulnerabilities = Number()
    low_severity_vulnerabilities = Number()


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
    stale_backlog_tickets = Number()
    stale_git_requests = Nested(GitRequestV2Schema, many=True)
    stale_branches = Nested(BranchV2Schema, many=True)
    latest_builds = Nested(BuildV2Schema, many=True)
    active_issues = Nested(ProjectIssueV2Schema, many=True)
    historical_data = Nested(HistoricalDataV2Schema, many=True)
    age_of_tickets_in_backlog = Nested(AgeV2Schema, many=True)

    last_updated = Dict(keys=String(), values=Int())
