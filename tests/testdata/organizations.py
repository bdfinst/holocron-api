"""Test data for organizations."""

from app.models import Organization

from .users import mock_users
from .valuestreams import mock_valuestreams


def create_organization(
    id=1, name="test", valuestreams=mock_valuestreams, users=mock_users
):
    """Create mock organization object with default values."""
    organization = Organization(name=name, valuestreams=valuestreams, users=users)
    organization.id = id
    return organization


mock_organizations = [create_organization()]
