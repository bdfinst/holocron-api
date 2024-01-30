"""Processor process_data test."""

from datetime import datetime, timezone

from app.processors.v2 import cumulative_flow, effort, process_data, utils
from app.processors.v2.cumulative_flow import CumulativeFlowChartData
from app.processors.v2.cycle_time_defect import CycleTimeDefectChartData
from app.processors.v2.effort import EffortChartData
from app.processors.v2.integration_frequency import IntegrationChartData
from app.processors.v2.lead_time import LeadTimeThroughputChartData
from app.processors.v2.process_data import (
    HistoricalData,
    TeamMetrics,
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
    issues,
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
    monkeypatch.setattr(
        utils,
        "datetime",
        MockDateTime(datetime(year=2000, month=1, day=16).replace(tzinfo=timezone.utc)),
    )
    monkeypatch.setattr(
        process_data, "FEATURE_FLAGS", {"FEATURE_DEPLOY_FREQUENCY": True}
    )
    monkeypatch.setattr(process_data, "datetime", mock_dt)
    org, vs, team = mock_organizations[0], mock_valuestreams[0], mock_teams[0]
    expected = [
        TeamMetrics(
            name=team.name,
            id=team.id,
            team_size=team.team_size,
            wip_tickets=1,
            is_view=False,
            organization_name=org.name,
            organization_id=org.id,
            value_stream_name=vs.name,
            value_stream_id=vs.id,
            stale_backlog_tickets=0,
            stale_git_requests=git_requests,
            stale_branches=branches,
            latest_builds=[builds[1]],
            active_issues=[issues[1], issues[2], issues[3], issues[4]],
            historical_data=[
                HistoricalData(
                    week="2000-01-03",
                    days_spent_on_features=1.0,
                    days_spent_on_defects=1.0,
                    days_spent_on_maintenance=0,
                    days_spent_on_unplanned=0,
                    amount_spent_on_features=1.0,
                    amount_spent_on_defects=1.0,
                    amount_spent_on_maintenance=0,
                    amount_spent_on_unplanned=0,
                    total_internal_integrations=2,
                    total_direct_integrations=1,
                    total_external_integrations=0,
                    average_team_size=5.0,
                    average_age_in_days_code_review_was_open=0,
                    total_tickets_in_backlog=0,
                    total_tickets_in_progress=2,
                    total_throughput=0,
                    ticket_lead_times=[],
                    total_deploys=2,
                    ticket_development_cycle_times=[],
                    defects_created=1,
                    highest_priority_defects_created=1,
                    high_priority_defects_created=0,
                    medium_priority_defects_created=0,
                    low_priority_defects_created=0,
                    lowest_priority_defects_created=0,
                    maintainability_issues=1,
                    maintainability_high_severity_issues=0,
                    maintainability_medium_severity_issues=0,
                    maintainability_low_severity_issues=1,
                    vulnerabilities=1,
                    high_severity_vulnerabilities=0,
                    medium_severity_vulnerabilities=0,
                    low_severity_vulnerabilities=1,
                ),
                HistoricalData(
                    week="2000-01-10",
                    days_spent_on_features=5.0,
                    days_spent_on_defects=0,
                    days_spent_on_maintenance=0,
                    days_spent_on_unplanned=0,
                    amount_spent_on_features=5.0,
                    amount_spent_on_defects=0,
                    amount_spent_on_maintenance=0,
                    amount_spent_on_unplanned=0,
                    total_internal_integrations=0,
                    total_direct_integrations=0,
                    total_external_integrations=0,
                    average_team_size=5.0,
                    average_age_in_days_code_review_was_open=0,
                    total_tickets_in_backlog=0,
                    total_tickets_in_progress=1,
                    total_throughput=0,
                    ticket_lead_times=[],
                    total_deploys=0,
                    ticket_development_cycle_times=[],
                    defects_created=0,
                    highest_priority_defects_created=0,
                    high_priority_defects_created=0,
                    medium_priority_defects_created=0,
                    low_priority_defects_created=0,
                    lowest_priority_defects_created=0,
                    maintainability_issues=2,
                    maintainability_high_severity_issues=0,
                    maintainability_medium_severity_issues=1,
                    maintainability_low_severity_issues=1,
                    vulnerabilities=3,
                    high_severity_vulnerabilities=1,
                    medium_severity_vulnerabilities=1,
                    low_severity_vulnerabilities=1,
                ),
            ],
            age_of_tickets_in_backlog=[],
            last_updated={
                "build": datetime(2020, 5, 17).timestamp(),
                "workflow": datetime(2020, 6, 17).timestamp(),
                "scm": datetime(2020, 7, 17).timestamp(),
                "project_analysis": datetime(2020, 8, 17).timestamp(),
            },
        )
    ]

    actual = process_organization(org)

    assert actual[0].historical_data[0] == expected[0].historical_data[0]
    assert actual[0].historical_data[1] == expected[0].historical_data[1]

    assert actual == expected


def test_process_team_last_collected(monkeypatch):
    """Test finding the most recent last_collected time."""
    monkeypatch.setattr(
        process_data,
        "process_cumulative_flow",
        lambda x: CumulativeFlowChartData({}, {}),
    )
    monkeypatch.setattr(process_data, "process_deploy_frequency", lambda x: {})
    monkeypatch.setattr(
        process_data,
        "process_effort",
        lambda x: EffortChartData({}, {}, {}, {}, {}, {}, {}, {}),
    )
    monkeypatch.setattr(
        process_data, "process_lead_time", lambda x: LeadTimeThroughputChartData({}, {})
    )
    monkeypatch.setattr(process_data, "get_latest_builds", lambda x: {})
    monkeypatch.setattr(
        process_data,
        "process_cycle_time_defect",
        lambda x: CycleTimeDefectChartData({}, {}, {}, {}, {}, {}, {}),
    )
    monkeypatch.setattr(process_data, "process_wip_load", lambda x: {})
    monkeypatch.setattr(
        process_data,
        "process_integration_frequency",
        lambda x, y: IntegrationChartData({}, {}, {}),
    )
    monkeypatch.setattr(process_data, "build_historical_data", lambda x, y: None)

    test_team = mock_team_last_collected
    test_org, test_vs = mock_organizations[0], mock_valuestreams[0]
    result = process_team(test_team, test_vs, test_org)

    assert (
        result.last_updated["workflow"] == datetime(2022, 2, 2).timestamp()
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
