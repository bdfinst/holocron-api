"""Test Data for valuestreams."""
from app.models import Valuestream

from .teams import mock_teams

mock_valuestreams = [Valuestream(name="mock_valuestream", teams=mock_teams)]
