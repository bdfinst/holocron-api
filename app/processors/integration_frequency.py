"""Process integration frequency data.

Integration frequency is weekly data that contains
integrations and direct_integrations keys.
Integrations has a list entry for each commit in trunk.
Direct integrations has a list entry for each commit in trunk that wasn't merged.
The values are always 1.
"""
from typing import List

from app.models import Commit

from .types import ChartData, DateValue
from .utils import values_by_week


def process_integration(integration: Commit) -> DateValue:
    """Get the DateValue for an integration."""
    return DateValue(integration.date, 1)


def process_integration_frequency(integrations: List[Commit]) -> ChartData:
    """Process commits into integration frequency data."""
    return {
        "integrations": values_by_week(
            [process_integration(integration) for integration in integrations]
        ),
        "direct_integrations": values_by_week(
            [
                process_integration(integration)
                for integration in integrations
                if not integration.is_merged
            ]
        ),
    }
