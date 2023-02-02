"""Test Data for valuestreams."""
from app.models import Valuestream

from .teams import mock_teams
from .users import mock_users


def create_valuestream(
    id=1, name="mock_valuestream", organization_id=1, users=mock_users, teams=mock_teams
):
    """Create mock valuestream object with default values."""
    valuestream = Valuestream(
        name=name, organization_id=organization_id, users=users, teams=teams
    )
    valuestream.id = id
    return valuestream


mock_valuestreams = [create_valuestream()]
