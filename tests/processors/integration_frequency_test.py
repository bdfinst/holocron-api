"""Testing integration frequency."""
from datetime import datetime

from app.models import Commit
from app.processors.integration_frequency import process_integration_frequency


def test_process_integration_frequency():
    """Testing process_integration_frequency."""
    cases = [
        (
            """Should collect direct integration and integrations""",
            [
                Commit(
                    repository_id=1,
                    sha="1234",
                    is_merged=True,
                    date=datetime(year=2000, month=1, day=3),
                    author_username="test",
                ),
                Commit(
                    repository_id=1,
                    sha="4321",
                    is_merged=False,
                    date=datetime(year=2000, month=1, day=3),
                    author_username="test",
                ),
            ],
            {
                "integrations": {"2000_01": [1, 1]},
                "direct_integrations": {"2000_01": [1]},
            },
        )
    ]

    for case in cases:
        _, input_case, expected = case
        actual = process_integration_frequency(input_case)
        assert expected == actual
