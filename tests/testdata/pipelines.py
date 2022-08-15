"""Test data for pipelines."""
from datetime import datetime

from app.models import Build, Job, Pipeline

successful_job = [
    Job(
        build_id=1,
        name="unit-test",
        status="success",
        stage="tests",
        job_id=1,
        job_url="https://test-build/-/asf/job/1",
    ),
    Job(
        build_id=1,
        name="scan",
        status="success",
        stage="scans",
        job_id=2,
        job_url="https://test-build/-/asf/job/2",
    ),
    Job(
        build_id=1,
        name="deploy",
        status="success",
        stage="Deploy",
        job_id=3,
        job_url="https://test-build/-/asf/job/3",
    ),
]

builds = [
    Build(
        pipeline_id=1,
        build_url="https://test-build/asf.com/-/1",
        build_status="success",
        start_time=datetime(year=2000, month=1, day=3, minute=30),
        end_time=datetime(year=2000, month=1, day=3, minute=45),
        jobs=successful_job,
    ),
    Build(
        pipeline_id=1,
        build_url="https://test-build/asf.com/-/2",
        build_status="success",
        start_time=datetime(year=2000, month=1, day=5, minute=30),
        end_time=datetime(year=2000, month=1, day=5, minute=45),
        jobs=successful_job,
    ),
]

mock_pipelines = [
    Pipeline(collector_id=1, url="https://test-pipeline.com", builds=builds)
]
