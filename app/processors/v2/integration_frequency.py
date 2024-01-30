"""Process integration frequency data.

Integration frequency is weekly data that contains
integrations and direct_integrations keys.
Integrations has a list entry for each commit in trunk.
Direct integrations has a list entry for each commit in trunk that wasn't merged.
The values are always 1.
"""

import logging
from typing import List, NamedTuple

from app.models import Commit, Team, TeamsMembers

from .types import ChartData, DateValue
from .utils import get_monday_string, is_between_dates


def process_integration(integration: Commit) -> DateValue:
    """Get the DateValue for an integration."""
    return DateValue(get_monday_string(integration.date), 1)


def is_internal(integration: Commit, teams_members: List[TeamsMembers]) -> bool:
    """Return boolean representing if integration is from an internal team member."""
    assignments = (
        team_member
        for team_member in teams_members
        if team_member.member.username == integration.author_username
    )
    try:
        result = any(
            is_between_dates(
                integration.date, assignment.start_date, assignment.end_date
            )
            for assignment in assignments
        )
    except ValueError:
        logging.critical(f"Error comparing dates for {integration.author_username}")
        return True
    return result


class IntegrationChartData(NamedTuple):
    """Type of chart data for integration frequency."""

    internal: ChartData
    external: ChartData
    direct: ChartData


def process_integration_frequency(
    team: Team, integrations: List[Commit]
) -> IntegrationChartData:
    """Process commits into integration frequency data."""
    internal, external = [], []
    if team.members:
        for integration in integrations:
            if is_internal(integration, team.members):
                internal.append(integration)
            else:
                external.append(integration)
    else:
        internal = integrations

    internal_integration_values = [
        process_integration(integration) for integration in internal
    ]
    external_integration_values = [
        process_integration(integration) for integration in external
    ]
    direct_integration_values = [
        process_integration(integration)
        for integration in integrations
        if not integration.is_merged
    ]

    result = IntegrationChartData({}, {}, {})
    for item in internal_integration_values:
        result.internal.setdefault(item.date, []).append(item.value)
    for item in external_integration_values:
        result.external.setdefault(item.date, []).append(item.value)
    for item in direct_integration_values:
        result.direct.setdefault(item.date, []).append(item.value)
    return result
