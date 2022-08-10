"""Mock configuration."""


class MockConfig:
    """Mock config class."""

    SSO_GROUPS_KEY = "groups"
    SSO_USERNAME_KEY = "username"
    SSO_ADMIN_GROUP = "admin"
    SSO_LEADERSHIP_GROUP = "leadership"
    MIN_EXPECTED_CYCLE_TIME_HOURS = 1

    def reset(self):
        """Cleanup mock function."""
        self.SSO_GROUPS_KEY = "groups"
        self.SSO_USERNAME_KEY = "username"
        self.SSO_ADMIN_GROUP = "admin"
        self.SSO_LEADERSHIP_GROUP = "leadership"
        self.MIN_EXPECTED_CYCLE_TIME_HOURS = 1


config = MockConfig()
