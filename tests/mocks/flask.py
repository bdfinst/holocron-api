"""Mocks for Flask objects."""


class MockRequest:
    """Mock Request class."""

    headers = {
        "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.rTCH8cLoGxAm_xw68z-zXVKi9ie6xJn9tnVWjd_9ftE"
    }


request = MockRequest()
