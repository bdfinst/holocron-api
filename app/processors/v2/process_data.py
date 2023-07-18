"""Process metrics data."""
from datetime import datetime, timedelta
from typing import Any, Dict, List, NamedTuple, Set

from app.config import FEATURE_FLAGS
from app.models import (
    Branch,
    Build,
    GitRequest,
    Organization,
    ProjectIssue,
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
from .maintainability import process_maintainability_score
from .team_history import process_team_history
from .types import ChartData
from .utils import average, get_monday_string


class Age(NamedTuple):
    """Age in days type."""

    days: float


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
    total_internal_integrations: int
    total_direct_integrations: int
    total_external_integrations: int
    average_team_size: float
    average_age_in_days_code_review_was_open: float
    total_tickets_in_backlog: int
    total_tickets_in_progress: int
    total_throughput: int
    ticket_lead_times: List[Age]
    total_deploys: int
    ticket_development_cycle_times: List[Age]
    defects_created: int
    highest_priority_defects_created: int
    high_priority_defects_created: int
    medium_priority_defects_created: int
    low_priority_defects_created: int
    lowest_priority_defects_created: int
    maintainability_score: int


class TeamMetrics(NamedTuple):
    """Team metrics type."""

    name: str
    id: int
    team_size: int
    wip_tickets: int
    is_view: bool
    organization_name: str
    organization_id: int
    value_stream_name: str
    value_stream_id: int
    stale_backlog_tickets: int
    stale_git_requests: List[GitRequest]
    stale_branches: List[Branch]
    latest_builds: List[Build]
    active_issues: List[ProjectIssue]
    historical_data: List[HistoricalData]
    age_of_tickets_in_backlog: List[Age]
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
    weeks: Set[str] = set()
    for chart in data.values():
        weeks.update(chart.keys())

    return [
        HistoricalData(
            week=week,
            days_spent_on_features=sum(data["feature_days"].get(week, [])),
            days_spent_on_defects=sum(data["defect_days"].get(week, [])),
            days_spent_on_maintenance=sum(data["maintenance_days"].get(week, [])),
            days_spent_on_unplanned=sum(data["unplanned_days"].get(week, [])),
            amount_spent_on_features=sum(data["feature_costs"].get(week, [])),
            amount_spent_on_defects=sum(data["defect_costs"].get(week, [])),
            amount_spent_on_maintenance=sum(data["maintenance_costs"].get(week, [])),
            amount_spent_on_unplanned=sum(data["unplanned_costs"].get(week, [])),
            total_internal_integrations=len(
                data["internal_integrations"].get(week, [])
            ),
            total_direct_integrations=len(data["direct_integrations"].get(week, [])),
            total_external_integrations=len(
                data["external_integrations"].get(week, [])
            ),
            average_team_size=average(
                data["team_size"].get(week, []), default=team.team_size
            ),
            average_age_in_days_code_review_was_open=average(
                data["review_age"].get(week, [])
            ),
            total_tickets_in_backlog=len(data["backlog"].get(week, [])),
            total_tickets_in_progress=len(data["wip"].get(week, [])),
            maintainability_score=sum(
                data["maintainability_score"].get(week, [])  # type: ignore
            ),
            total_throughput=len(data["throughput"].get(week, [])),
            ticket_lead_times=[Age(age) for age in data["lead_time"].get(week, [])],
            total_deploys=len(data["deploys"].get(week, [])),
            ticket_development_cycle_times=[
                Age(age) for age in data["cycle_time"].get(week, [])
            ],
            defects_created=len(data["defect_rate"].get(week, [])),
            highest_priority_defects_created=len(data["highest_defects"].get(week, [])),
            high_priority_defects_created=len(data["high_defects"].get(week, [])),
            medium_priority_defects_created=len(data["medium_defects"].get(week, [])),
            low_priority_defects_created=len(data["low_defects"].get(week, [])),
            lowest_priority_defects_created=len(data["lowest_defects"].get(week, [])),
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

    issues = flat_map(team.projects, lambda project: project.issues)
    maintainability_score = process_maintainability_score(issues)

    historical_data = build_historical_data(
        team,
        {
            "feature_days": effort.feature_days,
            "defect_days": effort.defect_days,
            "maintenance_days": effort.maintenance_days,
            "unplanned_days": effort.unplanned_days,
            "feature_costs": effort.feature_costs,
            "defect_costs": effort.defect_costs,
            "maintenance_costs": effort.maintenance_costs,
            "unplanned_costs": effort.unplanned_costs,
            "internal_integrations": integration_frequency.internal,
            "direct_integrations": integration_frequency.direct,
            "external_integrations": integration_frequency.external,
            "team_size": team_history,
            "review_age": review_frequency,
            "backlog": cumulative_flow.backlog,
            "wip": cumulative_flow.wip,
            "maintainability_score": maintainability_score,
            "throughput": lead_time.throughput,
            "lead_time": lead_time.lead_time,
            "deploys": deploy_frequency,
            "cycle_time": cycle_time_defect.cycle_time,
            "defect_rate": cycle_time_defect.defect_rate,
            "highest_defects": cycle_time_defect.highest_defects,
            "high_defects": cycle_time_defect.high_defects,
            "medium_defects": cycle_time_defect.medium_defects,
            "low_defects": cycle_time_defect.low_defects,
            "lowest_defects": cycle_time_defect.lowest_defects,
        },
    )

    current_week = get_monday_string(datetime.now())

    return TeamMetrics(
        name=team.name,
        id=team.id,
        team_size=team.team_size,
        wip_tickets=wip_load,
        is_view=team.view_owner_id is not None,
        value_stream_name=valuestream.name,
        value_stream_id=valuestream.id,
        organization_name=organization.name,
        organization_id=organization.id,
        stale_backlog_tickets=len(
            [
                ticket
                for ticket in cumulative_flow.backlog.get(current_week, [])
                if ticket > 30
            ]
        ),
        stale_git_requests=[
            gr
            for gr in git_requests
            if gr.is_open and (datetime.now() - gr.last_updated) > timedelta(hours=1)
        ],
        stale_branches=[
            b for b in branches if (datetime.now() - b.last_updated) > timedelta(days=1)
        ],
        latest_builds=builds,
        active_issues=[i for i in issues if i.closed_date is None],
        historical_data=historical_data,
        age_of_tickets_in_backlog=[
            Age(ticket) for ticket in cumulative_flow.backlog.get(current_week, [])
        ],
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
