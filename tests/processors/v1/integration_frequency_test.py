"""Testing integration frequency."""
from datetime import datetime

from app.models import Commit
from app.processors.v1.integration_frequency import process_integration_frequency
from tests.testdata import create_member, create_team_member, mock_teams


def test_process_integration_frequency():
    """Testing process_integration_frequency."""
    team = mock_teams[0]
    member = create_member()
    team.members = [
        create_team_member(
            team,
            member,
            start_date=datetime(year=2000, month=1, day=3),
            end_date=datetime(year=2000, month=1, day=3),
        )
    ]
    cases = [
        (
            """Should collect direct integration and integrations""",
            {
                "integrations": [
                    Commit(
                        repository_id=1,
                        sha="1234",
                        is_merged=True,
                        date=datetime(year=2000, month=1, day=3),
                        author_username=member.username,
                    ),
                    Commit(
                        repository_id=1,
                        sha="4321",
                        is_merged=False,
                        date=datetime(year=2000, month=1, day=3),
                        author_username=member.username,
                    ),
                    Commit(
                        repository_id=1,
                        sha="4132",
                        is_merged=True,
                        date=datetime(year=2000, month=1, day=3),
                        author_username="external",
                    ),
                    Commit(
                        repository_id=1,
                        sha="1423",
                        is_merged=True,
                        date=datetime(year=2000, month=1, day=4),
                        author_username=member.username,
                    ),
                ],
                "team": team,
            },
            {
                "integrations": {"2000_01": [1, 1]},
                "direct_integrations": {"2000_01": [1]},
                "external_integrations": {"2000_01": [1, 1]},
            },
        )
    ]

    for case in cases:
        _, input_case, expected = case
        actual = process_integration_frequency(
            input_case["team"], input_case["integrations"]
        )
        assert expected == actual
