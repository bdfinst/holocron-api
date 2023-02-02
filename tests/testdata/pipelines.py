"""Test data for pipelines."""
from datetime import datetime

from app.models import Build, Pipeline

builds = [
    Build(
        pipeline_id=1,
        build_url="https://test-build/asf.com/-/1",
        build_status="success",
        start_time=datetime(year=2000, month=1, day=3, minute=30),
        end_time=datetime(year=2000, month=1, day=3, minute=45),
        is_deployed=True,
        passed_with_warnings=True,
    ),
    Build(
        pipeline_id=1,
        build_url="https://test-build/asf.com/-/2",
        build_status="success",
        start_time=datetime(year=2000, month=1, day=5, minute=30),
        end_time=datetime(year=2000, month=1, day=5, minute=45),
        is_deployed=True,
        passed_with_warnings=True,
    ),
]


def create_pipeline(
    id=1,
    collector_id=1,
    name="test",
    url="https://test.com",
    builds=builds,
    last_collected=datetime(2020, 5, 17).timestamp(),
    pipeline_id=1,
    team_id=None,
):
    """Create mock pipeline object with default values."""
    pipeline = Pipeline(
        collector_id=collector_id,
        name=name,
        url=url,
        builds=builds,
        last_collected=last_collected,
        pipeline_id=pipeline_id,
        team_id=team_id,
    )
    pipeline.id = id
    return pipeline


mock_pipelines = [create_pipeline()]
mock_pipelines_last_collected = [
    create_pipeline(builds=[], last_collected=datetime(1999, 1, 1).timestamp()),
    create_pipeline(builds=[], last_collected=datetime(2010, 1, 1).timestamp()),
    create_pipeline(builds=[], last_collected=datetime(2022, 1, 1).timestamp()),
]
