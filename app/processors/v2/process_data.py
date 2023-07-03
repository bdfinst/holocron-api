"""Process metrics data."""
from datetime import datetime, timedelta
from typing import Any, Dict, List, NamedTuple

from app.config import FEATURE_FLAGS
from app.models import (
    Branch,
    Build,
    GitRequest,
    Organization,
    Team,
    Ticket,
    Valuestream,
)
from app.processors.v1.repo_build import get_latest_builds
from app.processors.v1.utils import flat_map
from app.processors.v1.wip_load import process_wip_load

from .code_review_trend import process_code_review_trend
from .cumulative_flow import process_cumulative_flow
from .cycle_time_defect import process_cycle_time_defect
from .deploy_frequency import process_deploy_frequency
from .effort import process_effort
from .integration_frequency import process_integration_frequency
from .lead_time import process_lead_time
from .team_history import process_team_history
from .types import ChartData
from .utils import average


class HistoricalData(NamedTuple):
    """Historical data type."""

    week: str
    days_spent_on_features: float
    days_spent_on_defects: float
    days_spent_on_maintenance: float
    days_spent_on_unplanned: float
    amount_spent_on_features: float
    amount_spent_on_defects: float
    amount_spent_on_maintenance: float
    amount_spent_on_unplanned: float
    total_integrations: int
    total_direct_integrations: int
    total_external_integrations: int
    average_team_size: float
    average_age_in_days_code_review_was_open: float
    total_issues_in_backlog: int
    total_issues_in_progress: int
    average_age_in_days_of_backlog_issues: float
    total_stale_backlog_issues: int
    total_throughput: int
    lead_times_for_week_in_days: List[float]
    total_deploys: int
    development_cycle_times_for_week_in_days: List[float]
    defects_created: int
    highest_priority_defects_created: int
    high_priority_defects_created: int
    medium_priority_defects_created: int
    low_priority_defects_created: int


class TeamMetrics(NamedTuple):
    """Team metrics type."""

    name: str
    id: int
    team_size: int
    wip_issues: int
    is_view: bool
    organization_name: str
    organization_id: int
    value_stream_name: str
    value_stream_id: int
    stale_merge_requests: List[GitRequest]
    stale_branches: List[Branch]
    latest_builds: List[Build]
    historical_data: List[HistoricalData]
    last_updated: Dict[str, Any]


def get_latest_time(time_stamps: List[int]) -> int:
    """Return -1 if team/org/valueStream has no active collector targets."""
    return max(time_stamps, default=-1)


def get_tickets_with_sorted_history(team: Team) -> List[Ticket]:
    """Return the tickets for team with sorted status histories."""
    tickets = flat_map(team.ticket_boards, lambda board: board.tickets)
    for ticket in tickets:
        ticket.status_history.sort(key=lambda history: history.date)
    return tickets


def build_historical_data(
    team: Team, data: Dict[str, ChartData]
) -> List[HistoricalData]:
    """Build the historical data from the chart data."""
    weeks = set()
    for chart in data.values():
        for weekly_data in chart.values():
            for week in weekly_data:
                weeks.add(week)

    def type_fixed_sum(numbers: List) -> int:
        """Sum function.

        Using builtin 'sum' with list of floats was causing an error.
        `Argument 1 to "sum" has incompatible type "List[float]";
        expected "Iterable[bool]"  [arg-type]`
        This function is used to replace it.
        """
        return sum(numbers)

    return [
        HistoricalData(
            week=week,
            days_spent_on_features=type_fixed_sum(
                data["effort_hours"]["feature"].get(week, [])
            ),
            days_spent_on_defects=type_fixed_sum(
                data["effort_hours"]["defect_effort"].get(week, [])
            ),
            days_spent_on_maintenance=type_fixed_sum(
                data["effort_hours"]["maintenance"].get(week, [])
            ),
            days_spent_on_unplanned=type_fixed_sum(
                data["effort_hours"]["unplanned"].get(week, [])
            ),
            amount_spent_on_features=type_fixed_sum(
                data["effort_cost"]["feature"].get(week, [])
            ),
            amount_spent_on_defects=type_fixed_sum(
                data["effort_cost"]["defect_effort"].get(week, [])
            ),
            amount_spent_on_maintenance=type_fixed_sum(
                data["effort_cost"]["maintenance"].get(week, [])
            ),
            amount_spent_on_unplanned=type_fixed_sum(
                data["effort_cost"]["unplanned"].get(week, [])
            ),
            total_integrations=len(
                data["integration_frequency"]["integrations"].get(week, [])
            ),
            total_direct_integrations=len(
                data["integration_frequency"]["direct_integrations"].get(week, [])
            ),
            total_external_integrations=len(
                data["integration_frequency"]["external_integrations"].get(week, [])
            ),
            average_team_size=average(
                data["team_history"]["team_size"].get(week, []), default=team.team_size
            ),
            average_age_in_days_code_review_was_open=average(
                data["review_frequency"]["age_in_days_review_was_open"].get(week, [])
            ),
            total_issues_in_backlog=len(
                data["cumulative_flow"]["backlog"].get(week, [])
            ),
            total_issues_in_progress=len(data["cumulative_flow"]["wip"].get(week, [])),
            average_age_in_days_of_backlog_issues=average(
                [
                    issue
                    for issue in data["cumulative_flow"]["backlog"].get(week, [])
                    if issue >= 0
                ]
            ),
            total_stale_backlog_issues=len(
                [
                    issue
                    for issue in data["cumulative_flow"]["backlog"].get(week, [])
                    if issue > 30
                ]
            ),
            total_throughput=len(
                data["lead_time_throughput"]["throughput"].get(week, [])
            ),
            lead_times_for_week_in_days=data["lead_time_throughput"][
                "story_lead_time"
            ].get(week, []),
            total_deploys=len(data["deploy_frequency"]["deploys"].get(week, [])),
            development_cycle_times_for_week_in_days=data["cycle_time_defect"][
                "dev_cycle_time"
            ].get(week, []),
            defects_created=len(data["cycle_time_defect"]["defect_rate"].get(week, [])),
            highest_priority_defects_created=len(
                data["cycle_time_defect"]["highest_defects"].get(week, [])
            ),
            high_priority_defects_created=len(
                data["cycle_time_defect"]["high_defects"].get(week, [])
            ),
            medium_priority_defects_created=len(
                data["cycle_time_defect"]["medium_defects"].get(week, [])
            ),
            low_priority_defects_created=len(
                data["cycle_time_defect"]["low_defects"].get(week, [])
            ),
        )
        for week in sorted(weeks)
    ]


def process_team(
    team: Team, valuestream: Valuestream, organization: Organization
) -> TeamMetrics:
    """Run processors on one team to build its metrics."""
    # max-locals
    # pylint: disable=R0914

    team_history = process_team_history(team.team_history)

    builds = get_latest_builds(team.pipelines)
    deploy_frequency = (
        process_deploy_frequency(
            flat_map(team.pipelines, lambda pipeline: pipeline.builds)
        )
        if FEATURE_FLAGS["FEATURE_DEPLOY_FREQUENCY"]
        else {}
    )

    integrations = flat_map(team.repositories, lambda repo: repo.commits)
    integration_frequency = process_integration_frequency(team, integrations)

    branches = flat_map(team.repositories, lambda repo: repo.branches)

    git_requests = flat_map(team.repositories, lambda repo: repo.git_requests)
    review_frequency = process_code_review_trend(git_requests)

    tickets = get_tickets_with_sorted_history(team)
    cumulative_flow = process_cumulative_flow(tickets)
    effort = process_effort(tickets)
    lead_time = process_lead_time(tickets)
    cycle_time_defect = process_cycle_time_defect(tickets)
    wip_load = process_wip_load(tickets)

    historical_data = build_historical_data(
        team,
        {
            "cumulative_flow": cumulative_flow,
            "effort_hours": effort["hours"],
            "effort_cost": effort["costs"],
            "lead_time_throughput": lead_time,
            "cycle_time_defect": cycle_time_defect,
            "integration_frequency": integration_frequency,
            "deploy_frequency": deploy_frequency,
            "review_frequency": review_frequency,
            "team_history": team_history,
        },
    )

    return TeamMetrics(
        name=team.name,
        id=team.id,
        team_size=team.team_size,
        wip_issues=wip_load,
        is_view=team.view_owner_id is not None,
        value_stream_name=valuestream.name,
        value_stream_id=valuestream.id,
        organization_name=organization.name,
        organization_id=organization.id,
        stale_merge_requests=[
            gr
            for gr in git_requests
            if gr.is_open and (datetime.now() - gr.last_updated) > timedelta(hours=1)
        ],
        stale_branches=[
            b for b in branches if (datetime.now() - b.last_updated) > timedelta(days=1)
        ],
        latest_builds=builds,
        historical_data=historical_data,
        last_updated={
            "workflow": get_latest_time(
                [
                    board.last_collected
                    for board in team.ticket_boards
                    if board.last_collected is not None
                ]
            ),
            "scm": get_latest_time(
                [
                    repo.last_collected
                    for repo in team.repositories
                    if repo.last_collected is not None
                ]
            ),
            "build": get_latest_time(
                [
                    pipe.last_collected
                    for pipe in team.pipelines
                    if pipe.last_collected is not None
                ]
            ),
            "project_analysis": get_latest_time(
                [
                    project.last_collected
                    for project in team.projects
                    if project.last_collected is not None
                ]
            ),
        },
    )


def process_organization(organization: Organization) -> List[TeamMetrics]:
    """Process organization metrics."""
    result: List[TeamMetrics] = []
    for valuestream in organization.valuestreams:
        result.extend(
            process_team(team, valuestream, organization) for team in valuestream.teams
        )
    return result
