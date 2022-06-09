"""BaseCRUD extension and instance for Team model."""
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.models import Team

from ._base import BaseCRUD
from .collector_targets import collector_targets_crud
from .users import users_crud


class TeamsCRUD(BaseCRUD[Team]):
    """Base CRUD extension for Team model."""

    @staticmethod
    def create_entity(session: Session, json: Dict[str, Any]) -> Team:
        """Insert team in database."""
        new_team = Team(
            name=json.get("name"),
            team_size=json.get("team_size"),
            valuestream_id=json.get("valuestream_id"),
        )

        new_team.users = [
            users_crud.get_entity(session, user_id)
            for user_id in json.get("user_ids", [])
        ]
        new_team.collector_targets = [
            collector_targets_crud.get_entity(session, target_id)
            for target_id in json.get("collector_target_ids", [])
        ]

        session.add(new_team)
        session.commit()
        session.refresh(new_team)

        return new_team

    def update_entity(self, session: Session, json: Dict[str, Any], id_: int) -> Team:
        """Update team in database."""
        team = self.get_entity(session, id_)
        team.name = json.get("name")
        team.team_size = json.get("team_size")
        team.valuestream_id = json.get("valuestream_id")

        team.users = [
            users_crud.get_entity(session, user_id)
            for user_id in json.get("user_ids", [])
        ]
        team.collector_targets = [
            collector_targets_crud.get_entity(session, target_id)
            for target_id in json.get("collector_target_ids", [])
        ]

        session.add(team)
        session.commit()
        session.refresh(team)

        return team


teams_crud = TeamsCRUD(Team)
