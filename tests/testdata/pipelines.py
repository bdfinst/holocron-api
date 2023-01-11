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

mock_pipelines = [
    Pipeline(
        collector_id=1,
        url="https://test-pipeline.com",
        builds=builds,
        last_collected=datetime(2020, 5, 17).timestamp(),
    )
]
mock_pipelines_last_collected = [
    Pipeline(
        collector_id=1,
        url="https://url1",
        builds=[],
        last_collected=datetime(1999, 1, 1).timestamp(),
    ),
    Pipeline(
        collector_id=1,
        url="https://url2",
        builds=[],
        last_collected=datetime(2010, 1, 1).timestamp(),
    ),
    Pipeline(
        collector_id=1,
        url="https://url3",
        builds=[],
        last_collected=datetime(2022, 1, 1).timestamp(),
    ),
]
