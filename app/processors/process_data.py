"""Process metrics data."""
from typing import Any, Dict, List, NamedTuple

from app.models import (
    Branch,
    Build,
    GitRequest,
    Organization,
    Team,
    Ticket,
    Valuestream,
)

from .code_review_trend import process_code_review_trend
from .cumulative_flow import process_cumulative_flow
from .cycle_time_defect import process_cycle_time_defect
from .deploy_frequency import process_deploy_frequency
from .effort import process_effort
from .integration_frequency import process_integration_frequency
from .lead_time import process_lead_time
from .repo_build import get_latest_builds
from .types import ChartData
from .utils import flat_map
from .wip_load import process_wip_load


class Metrics(NamedTuple):
    """Metrics type."""

    cumulative_flow: ChartData
    deploy_frequency: ChartData
    effort_hours: ChartData
    effort_costs: ChartData
    lead_time_throughput: ChartData
    cycle_time_defect: ChartData
    integration_frequency: ChartData
    code_review_trend: ChartData


class TeamMetrics(NamedTuple):
    """Team metrics type."""

    name: str
    team_size: int
    branches: List[Branch]
    merge_requests: List[GitRequest]
    wip_load_data: int
    repos_build_data: List[Build]
    weekly_data: Dict[str, Dict[str, Dict[str, List[int]]]]
    data_quality_issues: Dict[str, Any]
    last_updated: Dict[str, Any]


class ValuestreamMetrics(NamedTuple):
    """Valuestream metrics type."""

    name: str
    teams: List[TeamMetrics]
    last_updated: Dict[str, Any]


class OrganizationMetrics(NamedTuple):
    """Organization metrics type."""

    name: str
    valuestreams: List[ValuestreamMetrics]
    last_updated: Dict[str, Any]


def create_empty_week_object() -> Dict[str, Dict[str, List[int]]]:
    """Create an empty week object so the keys exist during processing."""
    return {
        "effort_hours": {
            "feature": [],
            "defect_effort": [],
            "unplanned": [],
            "maintenance": [],
        },
        "effort_costs": {
            "feature": [],
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
            "wip": [],
        },
        "deploy_frequency": {
            "deploys": [],
        },
        "code_review_trend": {
            "age_in_days_review_was_open": [],
        },
    }


def get_latest_time(time_stamps: List[int]) -> int:
    """Return -1 if team/org/valueStream has no active collector targets."""
    return max(time_stamps, default=-1)


def build_weekly_data(metrics: Metrics) -> Dict[str, Dict[str, Dict[str, List[int]]]]:
    """Build the weekly data using the metrics type."""
    weekly_data: Dict[str, Dict[str, Dict[str, List[int]]]] = {}
    # _asdict() is to satisfy type hinting through using named tuple
    for key, value in metrics._asdict().items():
        for chart, data in value.items():
            for week, week_data in data.items():
                weekly_data.setdefault(week, create_empty_week_object())
                weekly_data[week][key][chart] = week_data
    return weekly_data


def get_tickets_with_sorted_history(team: Team) -> List[Ticket]:
    """Return the tickets for team with sorted status histories."""
    tickets = flat_map(team.ticket_boards, lambda board: board.tickets)
    for ticket in tickets:
        ticket.status_history.sort(key=lambda history: history.date)
    return tickets


def process_team(team: Team) -> TeamMetrics:
    """Run processors on one team to build its metrics."""
    # scm team repos
    # features ticket board
    # build pipeline
    # next( iterator
    tickets = get_tickets_with_sorted_history(team)
    builds = flat_map(team.pipelines, lambda pipeline: pipeline.builds)
    integrations = flat_map(team.repositories, lambda repo: repo.commits)
    branches = flat_map(team.repositories, lambda repo: repo.branches)
    git_requests = flat_map(team.repositories, lambda repo: repo.git_requests)

    cumulative_flow = process_cumulative_flow(tickets)
    deploy_frequency = process_deploy_frequency(builds)
    effort = process_effort(tickets)
    lead_time = process_lead_time(tickets)
    repo_builds = get_latest_builds(team.pipelines)
    cycle_time_defect = process_cycle_time_defect(tickets)
    wip_load = process_wip_load(tickets)
    integration_frequency = process_integration_frequency(integrations)

    weekly_data = build_weekly_data(
        Metrics(
            cumulative_flow,
            deploy_frequency,
            effort["hours"],
            effort["costs"],
            lead_time,
            cycle_time_defect,
            integration_frequency,
            process_code_review_trend(git_requests),
        )
    )
    return TeamMetrics(
        team.name,
        team.team_size,
        branches,
        git_requests,
        wip_load,
        repo_builds,
        weekly_data,
        {},
        {
            "feature": get_latest_time(
                [board.last_collected for board in team.ticket_boards]
            ),
            "scm": get_latest_time([repo.last_collected for repo in team.repositories]),
            "build": get_latest_time([pipe.last_collected for pipe in team.pipelines]),
        },
    )


def process_valuestream(valuestream: Valuestream) -> ValuestreamMetrics:
    """Process valuestream metrics."""
    if len(valuestream.teams) == 0:
        return ValuestreamMetrics(
            valuestream.name, [], {"feature": -1, "scm": -1, "build": -1}
        )

    team_metrics = [process_team(team) for team in valuestream.teams]

    return ValuestreamMetrics(
        valuestream.name,
        team_metrics,
        {
            "feature": get_latest_time(
                [t.last_updated["feature"] for t in team_metrics]
            ),
            "scm": get_latest_time([t.last_updated["scm"] for t in team_metrics]),
            "build": get_latest_time([t.last_updated["build"] for t in team_metrics]),
        },
    )


def process_organization(organization: Organization) -> OrganizationMetrics:
    """Process organization metrics."""
    if len(organization.valuestreams) == 0:
        return OrganizationMetrics(
            organization.name, [], {"feature": -1, "scm": -1, "build": -1}
        )

    valuestream_metrics = [
        process_valuestream(valuestream) for valuestream in organization.valuestreams
    ]
    return OrganizationMetrics(
        organization.name,
        valuestream_metrics,
        {
            "feature": get_latest_time(
                [t.last_updated["feature"] for t in valuestream_metrics]
            ),
            "scm": get_latest_time(
                [t.last_updated["scm"] for t in valuestream_metrics]
            ),
            "build": get_latest_time(
                [t.last_updated["build"] for t in valuestream_metrics]
            ),
        },
    )
