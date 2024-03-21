"""Test Data for value streams."""

from app.models import ValueStream

from .teams import mock_teams
from .users import mock_users


def create_value_stream(
    id=1,
    name="mock_value_stream",
    organization_id=1,
    users=mock_users,
    teams=mock_teams,
):
    """Create mock value stream object with default values."""
    value_stream = ValueStream(
        name=name, organization_id=organization_id, users=users, teams=teams
    )
    value_stream.id = id
    return value_stream


mock_value_streams = [create_value_stream()]
