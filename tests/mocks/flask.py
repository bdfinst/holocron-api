"""Mocks for Flask objects."""


class MockRequest:
    """Mock Request class."""

    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.rTCH8cLoGxAm_xw68z-zXVKi9ie6xJn9tnVWjd_9ftE",
        "X-Forwarded-For": "0.0.0.0",
    }
    path = "/test"
    json = '{"key": "value"}'
    mimetype = "application/json"
    args = {"per_page": "100", "page": "1"}
    url = "myurl/endpoint?per_page=100&page=1"

    def reset(self):
        """Reset the mocks."""
        self.headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.rTCH8cLoGxAm_xw68z-zXVKi9ie6xJn9tnVWjd_9ftE",
            "X-Forwarded-For": "0.0.0.0",
        }
        self.path = "/test"
        self.json = '{"key": "value"}'
        self.mimetype = "application/json"
        self.args = {"per_page": "100", "page": "1"}
        self.url = "myurl/endpoint?per_page=100&page=1"
        if hasattr(self, "user"):
            del self.user


request = MockRequest()
