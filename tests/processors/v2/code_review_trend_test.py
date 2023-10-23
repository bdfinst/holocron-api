"""Test process_code_review_trend."""
from datetime import datetime

from app.models import GitRequest
from app.processors.v2.code_review_trend import process_code_review_trend


def test_process_code_review_trend():
    """Test process_code_review_trend function."""
    test_cases = [
        (
            """should ignore GitRequests with no merged_at.""",
            [
                GitRequest(
                    title="test",
                    url="https://test.com",
                    is_open=True,
                    merged_at=None,
                    first_opened=datetime(year=2000, month=1, day=25),
                    last_updated=datetime(year=2000, month=1, day=25),
                    collector_target_id=1,
                    author_username="test username",
                )
            ],
            {},
        ),
        (
            """should calculate the days difference between merged_at
            and first_opened, and include that calculation on the
            week of the merged_at date.""",
            [
                # ignored
                GitRequest(
                    title="test",
                    url="https://test.com",
                    is_open=True,
                    merged_at=None,
                    first_opened=datetime(year=2000, month=1, day=25),
                    last_updated=datetime(year=2000, month=1, day=25),
                    collector_target_id=1,
                    author_username="test username",
                ),
                # week { "2000-01-03": 5 }
                GitRequest(
                    title="test2",
                    url="https://test.com",
                    is_open=False,
                    merged_at=datetime(year=2000, month=1, day=9),
                    first_opened=datetime(year=2000, month=1, day=4),
                    last_updated=datetime(year=2000, month=1, day=25),
                    collector_target_id=1,
                    author_username="test username",
                ),
                # week { "2000-01-10": 11 }
                GitRequest(
                    title="test3",
                    url="https://test.com",
                    is_open=False,
                    merged_at=datetime(year=2000, month=1, day=15),
                    first_opened=datetime(year=2000, month=1, day=4),
                    last_updated=datetime(year=2000, month=1, day=25),
                    collector_target_id=1,
                    author_username="test username",
                ),
                # week { "2000-01-03": 0.5 }
                GitRequest(
                    title="test4",
                    url="https://test.com",
                    is_open=False,
                    merged_at=datetime(year=2000, month=1, day=5, hour=12),
                    first_opened=datetime(year=2000, month=1, day=5),
                    last_updated=datetime(year=2000, month=1, day=25),
                    collector_target_id=1,
                    author_username="test username",
                ),
            ],
            {
                "2000-01-03": [5, 0.5],
                "2000-01-10": [11],
            },
        ),
    ]
    for test_case in test_cases:
        description, input_case, expected_output = test_case
        assert expected_output == process_code_review_trend(input_case), description
