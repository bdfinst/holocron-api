"""Test data for organizations."""

from app.models import Organization

from .users import mock_users
from .value_streams import mock_value_streams


def create_organization(
    id=1, name="test", value_streams=mock_value_streams, users=mock_users
):
    """Create mock organization object with default values."""
    organization = Organization(name=name, value_streams=value_streams, users=users)
    organization.id = id
    return organization


mock_organizations = [create_organization()]
