"""Test process_code_review_trend."""
from datetime import datetime

from app.models import GitRequest
from app.processors.code_review_trend import process_code_review_trend


def test_process_code_review_trend(monkeypatch):
    """Test process_code_review_trend function."""
    test_cases = [
        (
            """should ignore GitRequests with no merged_at.""",
            [
                GitRequest(
                    id=1,
                    title="test",
                    is_open=True,
                    merged_at=None,
                    first_created=datetime(year=2000, month=1, day=25),
                )
            ],
            {
                "age_in_days_review_was_open": {},
            },
        ),
        (
            """should calculate the days difference between merged_at
            and first_created, and include that calculation on the
            week of the merged_at date.""",
            [
                # ignored
                GitRequest(
                    id=1,
                    title="test",
                    is_open=True,
                    merged_at=None,
                    first_created=datetime(year=2000, month=1, day=25),
                ),
                # week { "2000_01": 5 }
                GitRequest(
                    id=2,
                    title="test2",
                    is_open=False,
                    merged_at=datetime(year=2000, month=1, day=9),
                    first_created=datetime(year=2000, month=1, day=4),
                ),
                # week { "2000_02": 11 }
                GitRequest(
                    id=3,
                    title="test3",
                    is_open=False,
                    merged_at=datetime(year=2000, month=1, day=15),
                    first_created=datetime(year=2000, month=1, day=4),
                ),
                # week { "2000_01": 0.5 }
                GitRequest(
                    id=4,
                    title="test4",
                    is_open=False,
                    merged_at=datetime(year=2000, month=1, day=5, hour=12),
                    first_created=datetime(year=2000, month=1, day=5),
                ),
            ],
            {
                "age_in_days_review_was_open": {
                    "2000_01": [5, 0.5],
                    "2000_02": [11],
                },
            },
        ),
    ]
    for test_case in test_cases:
        description, input_case, expected_output = test_case
        assert expected_output == process_code_review_trend(input_case), description
