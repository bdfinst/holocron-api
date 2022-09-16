"""BaseCRUD extension and instance for Repository model."""
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Repository

from ._base import BaseCRUD
from .teams import teams_crud


class RepositoriesCRUD(BaseCRUD[Repository]):
    """Base CRUD extension for Repository model."""

    def get_entities(self, session: Session) -> List[Repository]:
        """Override get_entities to return only repositories."""
        return session.scalars(
            select(Repository).where(Repository.repository_id.is_not(None))
        ).all()

    @staticmethod
    def get_entities_for_team(session: Session, team_id: int) -> List[Repository]:
        """Get all repositories for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(Repository)
            .where(Repository.team_id == team.id)
            .where(Repository.repository_id.is_not(None))
        ).all()


repositories_crud = RepositoriesCRUD(Repository)
