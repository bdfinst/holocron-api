"""BaseCRUD extension and instance for Member model."""
import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import HolocronIntegrityError
from app.models import Member, TeamsMembers

from ._base import BaseCRUD


class MembersCRUD(BaseCRUD[Member]):
    """Base CRUD extension for Member model."""

    def create_entity(self, session: Session, json: Dict[str, Any]) -> Member:
        """Insert member in database."""
        new_member = Member(
            name=json["name"],
            username=json["username"],
        )
        try:
            session.add(new_member)
        except IntegrityError as err:
            session.rollback()
            if "psycopg2.errors.UniqueViolation" in str(err):
                raise HolocronIntegrityError("username", "already in use") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        session.commit()
        session.refresh(new_member)
        return new_member

    def find_entity_by_username(
        self, session: Session, username: str
    ) -> Optional[Member]:
        """Get member with given username, or None if doesn't exist."""
        return session.scalars(
            select(Member).where(Member.username == username)
        ).first()


class TeamsMembersCRUD(BaseCRUD[TeamsMembers]):
    """Base CRUD extension for TeamsMembers model."""

    @staticmethod
    def create_entities(
        session: Session, json: List[Dict[str, Any]], team_id: int
    ) -> List[TeamsMembers]:
        """Insert multiple TeamsMembers in database."""
        members = (get_or_create_member(session, item) for item in json)
        new_teams_members = [
            TeamsMembers(
                member_id=next(members).id,
                team_id=team_id,
                start_date=item["start_date"],
                end_date=item.get("end_date"),
            )
            for item in json
        ]
        try:
            for new_entity in new_teams_members:
                session.add(new_entity)
        except IntegrityError as err:
            session.rollback()
            if "pscopg2.errors.ForeignKeyViolation" in str(err):
                raise HolocronIntegrityError("team_id", "not found") from err
            logging.error(str(err))
            raise HolocronIntegrityError("unknown", "unknown, see logs") from err

        session.commit()
        for teams_members in new_teams_members:
            session.refresh(teams_members)
        return new_teams_members


def get_or_create_member(session: Session, json: Dict[str, Any]) -> Member:
    """Retrieve member based on username, inserting into database if necessary."""
    member = members_crud.find_entity_by_username(session, json["username"])
    if member is None:
        member = members_crud.create_entity(session, json)
    return member


members_crud = MembersCRUD(Member)
teams_members_crud = TeamsMembersCRUD(TeamsMembers)
