"""Mock configuration."""


class MockConfig:
    """Mock config class."""

    SSO_GROUPS_KEY = "groups"
    SSO_USERNAME_KEY = "username"
    SSO_ADMIN_GROUP = "admin"
    SSO_LEADERSHIP_GROUP = "leadership"
    MIN_EXPECTED_CYCLE_TIME_HOURS = 1
    REQUEST_IP_HEADER = "X-Forwarded-For"
    FEATURE_FLAGS = {
        "FALSE_FEATURE": False,
        "TRUE_FEATURE": True,
    }

    def reset(self):
        """Cleanup mock function."""
        self.SSO_GROUPS_KEY = "groups"
        self.SSO_USERNAME_KEY = "username"
        self.SSO_ADMIN_GROUP = "admin"
        self.SSO_LEADERSHIP_GROUP = "leadership"
        self.MIN_EXPECTED_CYCLE_TIME_HOURS = 1
        self.REQUEST_IP_HEADER = "X-Forwarded-For"
        self.FEATURE_FLAGS = {
            "FALSE_FEATURE": False,
            "TRUE_FEATURE": True,
        }


config = MockConfig()
