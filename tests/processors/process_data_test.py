"""Processor process_data test."""
from datetime import datetime

from app.processors import cumulative_flow, effort, process_data
from app.processors.process_data import (
    OrganizationMetrics,
    TeamMetrics,
    ValuestreamMetrics,
    get_latest_time,
    get_tickets_with_sorted_history,
    process_organization,
    process_team,
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
from tests.testdata.teams import mock_team_last_collected

mock_dt = MockDateTime(datetime(year=2000, month=1, day=16))


def test_get_tickets_with_sorted_history():
    """Testing get_tickets_with_sorted_history."""
    team = mock_teams[0]
    tickets_with_sorted_status_histories = get_tickets_with_sorted_history(team)
    for t in tickets_with_sorted_status_histories:
        assert all(
            t.status_history[i].date <= t.status_history[i + 1].date
            for i in range(len(t.status_history) - 1)
        )


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
                        "backlog": [],
                        "wip": [4.0, -1],
                    },
                    "deploy_frequency": {
                        "deploys": [1, 1],
                    },
                    "code_review_trend": {
                        "age_in_days_review_was_open": [],
                    },
                    "team_size_histories": {"team_size": []},
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
                        "wip": [6.0],
                    },
                    "deploy_frequency": {
                        "deploys": [],
                    },
                    "code_review_trend": {
                        "age_in_days_review_was_open": [],
                    },
                    "team_size_histories": {"team_size": []},
                },
            },
            data_quality_issues={},
            last_updated={
                "build": datetime(2020, 5, 17).timestamp(),
                "feature": datetime(2020, 6, 17).timestamp(),
                "scm": datetime(2020, 7, 17).timestamp(),
            },
        )
    ]
    expected = OrganizationMetrics(
        name=org.name,
        valuestreams=[
            ValuestreamMetrics(
                name=vs.name,
                teams=expected_team_metrics,
                last_updated={
                    "build": int(datetime(2020, 5, 17).timestamp()),
                    "feature": datetime(2020, 6, 17).timestamp(),
                    "scm": datetime(2020, 7, 17).timestamp(),
                },
            )
        ],
        last_updated={
            "build": datetime(2020, 5, 17).timestamp(),
            "feature": datetime(2020, 6, 17).timestamp(),
            "scm": datetime(2020, 7, 17).timestamp(),
        },
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


def test_process_team_last_collected(monkeypatch):
    """Test finding the most recent last_collected time."""
    process_effort = {"hours": 1, "costs": 2}
    monkeypatch.setattr(process_data, "process_cumulative_flow", lambda x: {})
    monkeypatch.setattr(process_data, "process_deploy_frequency", lambda x: {})
    monkeypatch.setattr(process_data, "process_effort", lambda x: process_effort)
    monkeypatch.setattr(process_data, "process_lead_time", lambda x: {})
    monkeypatch.setattr(process_data, "get_latest_builds", lambda x: {})
    monkeypatch.setattr(process_data, "process_cycle_time_defect", lambda x: {})
    monkeypatch.setattr(process_data, "process_wip_load", lambda x: {})
    monkeypatch.setattr(process_data, "process_integration_frequency", lambda x: {})
    monkeypatch.setattr(process_data, "build_weekly_data", lambda x: None)

    test_team = mock_team_last_collected
    result = process_team(test_team)

    assert (
        result.last_updated["feature"] == datetime(2022, 2, 2).timestamp()
        and result.last_updated["scm"] == datetime(2022, 3, 3).timestamp()
        and result.last_updated["build"] == datetime(2022, 1, 1).timestamp()
    )


def test_get_latest_time():
    """Test to see if the maximum unix time is returned."""
    time_stamps = [10000000000, 30000000000, 20000000000]
    expected = time_stamps[1]
    assert expected == get_latest_time(time_stamps)


def test_get_latest_time_empty_list():
    """Test to see if -1 is returned from an empty array input."""
    time_stamps = []
    expected = -1
    assert expected == get_latest_time(time_stamps)
