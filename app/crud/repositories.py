"""BaseCRUD extension and instance for Repository model."""

from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import CollectorTargetType, Repository

from ._base import BaseCRUD
from .teams import teams_crud


class RepositoriesCRUD(BaseCRUD[Repository]):
    """Base CRUD extension for Repository model."""

    def get_count(self, session: Session) -> int:
        """Override get_count to only count repositories."""
        query = (
            # pylint: disable-next=E1102; false positive
            session.query(func.count())
            .select_from(Repository)
            .where(Repository.type == CollectorTargetType.SCM)
        )
        return query.scalar()

    def get_count_for_team(self, session: Session, team_id: int) -> int:
        """Override get_count_for_team to only count repositories."""
        team = teams_crud.get_entity(session, team_id)
        query = (
            session.query(
                # pylint: disable-next=E1102; false positive
                func.count()
            )
            .select_from(Repository)
            .where(Repository.team_id == team.id)
            .where(Repository.type == CollectorTargetType.SCM)
        )

        return query.scalar()

    def get_entity(self, session: Session, id_: int) -> Repository:
        """Override get_entity to return only repository."""
        result = session.scalars(
            select(Repository)
            .where(Repository.type == CollectorTargetType.SCM)
            .where(Repository.id == id_)
        ).first()
        if result is None:
            raise HolocronIntegrityError(
                f"{Repository.__name__} id", f"Invalid id: {id_}"
            )
        return result

    def get_entities(self, session: Session) -> Sequence[Repository]:
        """Override get_entities to return only repositories."""
        return session.scalars(
            select(Repository).where(Repository.type == CollectorTargetType.SCM)
        ).all()

    def get_entities_paginated(
        self, session: Session, offset=0, limit=100
    ) -> Sequence[Repository]:
        """Override get_entities_paginated to return only repositories."""
        return session.scalars(
            select(Repository)
            .where(Repository.type == CollectorTargetType.SCM)
            .offset(offset)
            .limit(limit)
        ).all()

    @staticmethod
    def get_entities_for_team(session: Session, team_id: int) -> Sequence[Repository]:
        """Get all repositories for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(Repository)
            .where(Repository.team_id == team.id)
            .where(Repository.type == CollectorTargetType.SCM)
        ).all()

    @staticmethod
    def get_entities_for_team_paginated(
        session: Session, team_id: int, offset=0, limit=100
    ) -> Sequence[Repository]:
        """Get paginated repositories for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(Repository)
            .where(Repository.team_id == team.id)
            .where(Repository.type == CollectorTargetType.SCM)
            .offset(offset)
            .limit(limit)
        ).all()


repositories_crud = RepositoriesCRUD(Repository)
