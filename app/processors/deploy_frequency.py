"""Process deploy frequency data.

Deploy frequency is weekly data represented by the deploys key.
One list entry is for each deployment made during the week.
The value is always 1.
"""
from typing import List

from app import config
from app.models import Build

from .types import ChartData, DateValue
from .utils import values_by_week


def process_build(build: Build) -> DateValue:
    """Get the DateValue for a deployment."""
    deploy = 0
    for job in build.jobs:
        if (
            job.stage == config.RELEASE_STAGE_NAME
            and job.status == config.STAGE_PASSED_STATUS
        ):
            deploy = 1
    return DateValue(build.end_time, deploy)


def process_deploy_frequency(builds: List[Build]) -> ChartData:
    """Process builds into deploy frequency data."""
    return {
        "deploys": values_by_week(
            [
                date_value
                for date_value in [process_build(build) for build in builds]
                if date_value.value != 0
            ]
        )
    }
