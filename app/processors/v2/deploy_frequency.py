"""Process deploy frequency data.

Deploy frequency is weekly data represented by the deploys key.
One list entry is for each deployment made during the week.
The value is always 1.
"""
from typing import List

from app import config
from app.models import Build

from .types import ChartData, DateValue
from .utils import get_monday_string


def process_build(build: Build) -> DateValue:
    """Get the DateValue for a deployment."""
    deploy = 0
    if build.is_deployed is True and build.build_status is config.PIPLINE_PASSED_STATUS:
        deploy = 1

    return DateValue(get_monday_string(build.end_time), deploy)


def process_deploy_frequency(builds: List[Build]) -> ChartData:
    """Process builds into deploy frequency data."""
    deploy_values = [process_build(build) for build in builds]

    result: ChartData = {}
    for item in deploy_values:
        result.setdefault(item.date, []).append(item.value)
    return result
