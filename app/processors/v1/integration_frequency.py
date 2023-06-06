"""Process integration frequency data.

Integration frequency is weekly data that contains
integrations and direct_integrations keys.
Integrations has a list entry for each commit in trunk.
Direct integrations has a list entry for each commit in trunk that wasn't merged.
The values are always 1.
"""
import logging
from typing import List

from app.models import Commit, Team, TeamsMembers

from .types import ChartData, DateValue
from .utils import is_between_dates, values_by_week


def process_integration(integration: Commit) -> DateValue:
    """Get the DateValue for an integration."""
    return DateValue(integration.date, 1)


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


def process_integration_frequency(team: Team, integrations: List[Commit]) -> ChartData:
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

    return {
        "integrations": values_by_week(
            [process_integration(integration) for integration in internal]
        ),
        "direct_integrations": values_by_week(
            [
                process_integration(integration)
                for integration in integrations
                if not integration.is_merged
            ]
        ),
        "external_integrations": values_by_week(
            [process_integration(integration) for integration in external]
        ),
    }
