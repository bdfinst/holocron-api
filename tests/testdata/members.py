"""Test data for members."""
from app.models import Member


def create_member(id=1, name="test", username="test"):
    """Create mock member object with default values."""
    member = Member(name=name, username=username)
    member.id = id
    return member
