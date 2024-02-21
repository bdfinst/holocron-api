"""BaseCRUD extension and instance for Pipeline model."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import CollectorTargetType, Project

from ._base import BaseCRUD
from .teams import teams_crud


class ProjectsCRUD(BaseCRUD[Project]):
    """Base CRUD extension for Project model."""

    def get_entity(self, session, id_: int) -> Project:
        """Override get_entity to return only project."""
        result = session.scalars(
            select(Project)
            .where(Project.type == CollectorTargetType.PROJECT_ANALYSIS)
            .where(Project.id == id_)
        ).first()
        if result is None:
            raise HolocronIntegrityError(f"{Project.__name__} id", f"Invalid id: {id_}")
        return result

    def get_entities(self, session: Session) -> Sequence[Project]:
        """Override get_entities to return only projects."""
        return session.scalars(
            select(Project).where(Project.type == CollectorTargetType.PROJECT_ANALYSIS)
        ).all()

    def get_entities_paginated(
        self, session: Session, offset=0, limit=100
    ) -> Sequence[Project]:
        """Override get_entities_paginated to return only projects."""
        return session.scalars(
            select(Project)
            .where(Project.type == CollectorTargetType.PROJECT_ANALYSIS)
            .offset(offset)
            .limit(limit)
        ).all()

    @staticmethod
    def get_entities_for_team(session: Session, team_id: int) -> Sequence[Project]:
        """Get all projects for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(Project)
            .where(Project.team_id == team.id)
            .where(Project.type == CollectorTargetType.PROJECT_ANALYSIS)
        ).all()

    @staticmethod
    def get_entities_for_team_paginated(
        session: Session, team_id: int, offset=0, limit=100
    ) -> Sequence[Project]:
        """Get paginated projects for a given team."""
        team = teams_crud.get_entity(session, team_id)
        return session.scalars(
            select(Project)
            .where(Project.team_id == team.id)
            .where(Project.type == CollectorTargetType.PROJECT_ANALYSIS)
            .offset(offset)
            .limit(limit)
        ).all()


projects_crud = ProjectsCRUD(Project)
