"""Test data for organizations."""
from app.models import Organization

from .valuestreams import mock_valuestreams

mock_organizations = [Organization(name="test", valuestreams=mock_valuestreams)]
