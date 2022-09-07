"""Processor process_data test."""
from datetime import datetime

from app.processors import cumulative_flow, effort
from app.processors.process_data import (
    OrganizationMetrics,
    TeamMetrics,
    ValuestreamMetrics,
    process_organization,
)
from tests.mocks import MockDateTime
from tests.testdata import (
    branches,
    builds,
    git_requests,
    mock_organizations,
    mock_teams,
    mock_valuestreams,
)

mock_dt = MockDateTime(datetime(year=2000, month=1, day=16))


def test_process_organization(monkeypatch):
    """Integration testing for the overall process organization."""
    monkeypatch.setattr(cumulative_flow, "datetime", mock_dt)
    monkeypatch.setattr(effort, "datetime", mock_dt)
    org, vs, team = mock_organizations[0], mock_valuestreams[0], mock_teams[0]
    expected_team_metrics = [
        TeamMetrics(
            name=team.name,
            team_size=team.team_size,
            branches=branches,
            merge_requests=git_requests,
            wip_load_data=1,
            repos_build_data=[builds[1]],
            weekly_data={
                "2000_01": {
                    "effort_hours": {
                        "feature": [1.0],
                        "defect_effort": [1.0],
                        "unplanned": [],
                        "maintenance": [],
                    },
                    "effort_costs": {
                        "feature": [1.0],
                        "defect_effort": [1.0],
                        "unplanned": [],
                        "maintenance": [],
                    },
                    "lead_time_throughput": {
                        "story_lead_time": [],
                        "throughput": [],
                    },
                    "cycle_time_defect": {
                        "dev_cycle_time": [],
                        "defect_rate": [1],
                        "highest_defects": [1],
                        "high_defects": [],
                        "medium_defects": [],
                        "low_defects": [],
                        "lowest_defects": [],
                    },
                    "integration_frequency": {
                        "integrations": [1, 1],
                        "direct_integrations": [1],
                    },
                    "cumulative_flow": {
                        "backlog": [4.0],
                        "wip": [5.0, 1.0],
                    },
                    "deploy_frequency": {
                        "deploys": [1, 1],
                    },
                },
                "2000_02": {
                    "effort_hours": {
                        "feature": [5.0],
                        "defect_effort": [],
                        "unplanned": [],
                        "maintenance": [],
                    },
                    "effort_costs": {
                        "feature": [5.0],
                        "defect_effort": [],
                        "unplanned": [],
                        "maintenance": [],
                    },
                    "lead_time_throughput": {
                        "story_lead_time": [],
                        "throughput": [],
                    },
                    "cycle_time_defect": {
                        "dev_cycle_time": [],
                        "defect_rate": [],
                        "highest_defects": [],
                        "high_defects": [],
                        "medium_defects": [],
                        "low_defects": [],
                        "lowest_defects": [],
                    },
                    "integration_frequency": {
                        "integrations": [],
                        "direct_integrations": [],
                    },
                    "cumulative_flow": {
                        "backlog": [],
                        "wip": [5.0, 6.0],
                    },
                    "deploy_frequency": {
                        "deploys": [],
                    },
                },
            },
            data_quality_issues={},
            last_updated={"build": datetime(2020, 5, 17),"feature": datetime(2020, 6, 17),"scm": datetime(2020, 7, 17)},
        )
    ]
    expected = OrganizationMetrics(
        name=org.name,
        valuestreams=[
            ValuestreamMetrics(
                name=vs.name, teams=expected_team_metrics, last_updated={'build': datetime(2020, 5, 17),'feature': datetime(2020, 6, 17),'scm': datetime(2020, 7, 17)}
            )
        ],
        last_updated={'build': datetime(2020, 5, 17),'feature': datetime(2020, 6, 17),'scm': datetime(2020, 7, 17)},
    )

    actual = process_organization(org)

    assert (
        actual.valuestreams[0].teams[0].weekly_data["2000_01"]
        == expected_team_metrics[0].weekly_data["2000_01"]
    )
    assert (
        actual.valuestreams[0].teams[0].weekly_data["2000_02"]
        == expected_team_metrics[0].weekly_data["2000_02"]
    )
    assert actual == expected
