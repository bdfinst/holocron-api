"""Test data for users."""

from app.models import User


def create_user(
    id=1, username="test", sso_id="test", is_org_leadership=False, is_admin=False
):
    """Create mock user object with default values."""
    user = User(
        username=username,
        sso_id=sso_id,
        is_org_leadership=is_org_leadership,
        is_admin=is_admin,
    )
    user.id = id
    return user


mock_users = [create_user()]
