"""Mock for all CRUD modules."""


class MockCRUD:
    """Mock CRUD class."""

    def get_entities(self, session):
        """Mock get_entities method."""
        return []

    def get_entities_for_team(self, session, id):
        """Mock get_entities_for_team method."""
        return []

    def get_entity(self, session, id):
        """Mock get_entity method."""
        return {"id": id}

    def create_entity(self, session, json):
        """Mock create_entity method."""
        return json

    def update_entity(self, session, json, id):
        """Mock update_entity method."""
        json.update({"id": id})
        return json

    def delete_entity(self, session, id):
        """Mock delete_entity method."""
        return {"id", id}

    def upsert_sso_user(self, session, token):
        """Mock upsert_sso_user method."""
        return {"username": token["sub"]}


crud = MockCRUD()
