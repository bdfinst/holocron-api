"""Test data for members."""

from datetime import datetime

from app.models import Member, TeamsMembers


def create_member(id=1, name="test", username="test"):
    """Create mock member object with default values."""
    member = Member(name=name, username=username)
    member.id = id
    return member


def create_team_member(
    team,
    member,
    id=1,
    start_date=datetime(year=2000, month=1, day=1),
    end_date=None,
):
    """Create mock team_member object with default values."""
    team_member = TeamsMembers(
        start_date=start_date,
        end_date=end_date,
        team_id=team.id,
        member_id=member.id,
    )
    team_member.team = team
    team_member.member = member
    team_member.id = id
    return team_member
